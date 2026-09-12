"""Read-only shell metadata from one already-owned C09 Windows Job Object.

No global process enumeration, launch, write, permission request or termination.
Failure is optional observation unavailability, never a C09 enforcement verdict.
"""
import ctypes
from ctypes import wintypes
import hashlib
from pathlib import PureWindowsPath
import time

SHELLS = {"powershell.exe", "pwsh.exe", "cmd.exe"}
MAX_PIDS = 256
MAX_COMMAND_BYTES = 256 * 1024
MAX_IDENTITIES = 1024
MAX_SHELLS = 16


class WindowsQuery:
    def __init__(self, job_handle):
        self.job_handle = job_handle
        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        self.native = ctypes.WinDLL("ntdll", use_last_error=True)
        k = self.kernel
        k.QueryInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD, ctypes.c_void_p]
        k.QueryInformationJobObject.restype = wintypes.BOOL
        k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
        k.OpenProcess.restype = wintypes.HANDLE
        k.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
        k.IsProcessInJob.restype = wintypes.BOOL
        k.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
        k.GetProcessTimes.restype = wintypes.BOOL
        k.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
        k.QueryFullProcessImageNameW.restype = wintypes.BOOL
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        self.native.NtQueryInformationProcess.argtypes = [wintypes.HANDLE, wintypes.ULONG, ctypes.c_void_p, wintypes.ULONG, ctypes.POINTER(wintypes.ULONG)]
        self.native.NtQueryInformationProcess.restype = ctypes.c_long

    def pids(self):
        buffer = ctypes.create_string_buffer(8 + ctypes.sizeof(ctypes.c_size_t) * MAX_PIDS)
        if not self.kernel.QueryInformationJobObject(self.job_handle, 3, buffer, len(buffer), None):
            raise ctypes.WinError(ctypes.get_last_error())
        assigned = ctypes.c_uint32.from_buffer(buffer, 0).value
        count = ctypes.c_uint32.from_buffer(buffer, 4).value
        if assigned > MAX_PIDS or count > MAX_PIDS or count > assigned:
            raise ValueError("owned Job PID list exceeds the fixed bound")
        return [ctypes.c_size_t.from_buffer(buffer, 8 + index * ctypes.sizeof(ctypes.c_size_t)).value for index in range(count)]

    def open(self, pid):
        handle = self.kernel.OpenProcess(0x1000, False, pid)  # QUERY_LIMITED_INFORMATION only.
        if not handle:
            raise ctypes.WinError(ctypes.get_last_error())
        return handle

    def member(self, handle):
        belongs = wintypes.BOOL()
        if not self.kernel.IsProcessInJob(handle, self.job_handle, ctypes.byref(belongs)):
            raise ctypes.WinError(ctypes.get_last_error())
        return bool(belongs.value)

    def created(self, handle):
        values = [wintypes.FILETIME() for _ in range(4)]
        if not self.kernel.GetProcessTimes(handle, *(ctypes.byref(value) for value in values)):
            raise ctypes.WinError(ctypes.get_last_error())
        return (values[0].dwHighDateTime << 32) | values[0].dwLowDateTime

    def image(self, handle):
        buffer = ctypes.create_unicode_buffer(32768)
        length = wintypes.DWORD(len(buffer))
        if not self.kernel.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(length)):
            raise ctypes.WinError(ctypes.get_last_error())
        return buffer.value

    def command(self, handle):
        needed = wintypes.ULONG()
        self.native.NtQueryInformationProcess(handle, 60, None, 0, ctypes.byref(needed))
        if not 0 < needed.value <= MAX_COMMAND_BYTES:
            raise ValueError("owned shell command-line size unavailable/out of bounds")
        buffer = ctypes.create_string_buffer(needed.value)
        status = self.native.NtQueryInformationProcess(handle, 60, buffer, len(buffer), ctypes.byref(needed))
        if status < 0:
            raise OSError("owned shell command-line query failed with NTSTATUS " + hex(status & 0xFFFFFFFF))
        class UnicodeString(ctypes.Structure):
            _fields_ = [("length", wintypes.USHORT), ("maximum", wintypes.USHORT), ("buffer", ctypes.c_void_p)]
        if len(buffer) < ctypes.sizeof(UnicodeString):
            raise ValueError("owned shell command-line header incomplete")
        value = UnicodeString.from_buffer(buffer)
        start = ctypes.addressof(buffer)
        if (not value.buffer or value.length % 2 or value.length > value.maximum or
                not start + ctypes.sizeof(UnicodeString) <= value.buffer <= start + len(buffer) - value.length):
            raise ValueError("owned shell command-line pointer/length invalid")
        return ctypes.string_at(value.buffer, value.length).decode("utf-16-le", errors="strict")

    def close(self, handle):
        self.kernel.CloseHandle(handle)


class Collector:
    def __init__(self, query, sanitize):
        self.query, self.sanitize = query, sanitize
        self.seen, self.records, self.errors = set(), [], []

    def error(self, stage, error):
        if len(self.errors) < 16:
            # Never retain exception payloads that could contain command text.
            self.errors.append({"stage": stage, "error_type": type(error).__name__, "observed_monotonic": time.monotonic()})

    def poll(self):
        try:
            pids = self.query.pids()
            if len(pids) > MAX_PIDS:
                raise ValueError("too many owned PIDs")
        except Exception as error:
            self.error("owned-job-list", error)
            return
        for pid in pids:
            handle = None
            try:
                if type(pid) is not int or pid <= 0:
                    raise ValueError("invalid owned PID")
                handle = self.query.open(pid)
                if not self.query.member(handle):
                    raise ValueError("PID is no longer in the selected Job")
                created = self.query.created(handle)
                if type(created) is not int or created <= 0:
                    raise ValueError("process creation identity unavailable")
                if (pid, created) in self.seen:
                    continue
                if len(self.seen) >= MAX_IDENTITIES or len(self.records) >= MAX_SHELLS:
                    raise ValueError("optional observation capacity reached")
                image = self.query.image(handle)
                self.seen.add((pid, created))
                if PureWindowsPath(image).name.lower() not in SHELLS:
                    continue
                command = self.query.command(handle)
                if not self.query.member(handle) or self.query.created(handle) != created:
                    raise ValueError("owned shell identity changed during query")
                safe_image, safe_command = self.sanitize(image), self.sanitize(command)
                unchanged = safe_image == image and safe_command == command
                self.records.append({"pid": pid, "creation_filetime": created, "owned_job_verified": True,
                    "executable": safe_image, "command_line": safe_command,
                    "command_line_utf16le_sha256": hashlib.sha256(command.encode("utf-16-le")).hexdigest(),
                    "raw_command_line_retained": unchanged, "selector_eligible": unchanged,
                    "observed_monotonic": time.monotonic()})
            except Exception as error:
                self.error("owned-process-query", error)
            finally:
                if handle is not None:
                    try:
                        self.query.close(handle)
                    except Exception as error:
                        self.error("query-handle-close", error)

    def result(self):
        return {"status": "observed" if self.records else "unavailable", "records": self.records, "errors": self.errors,
            "scope": "Only query handles for PIDs enumerated from this observation's existing outer Job; commands read only for powershell.exe/pwsh.exe/cmd.exe.",
            "limit": "Optional shell-launch metadata, not proof of hook identity until matched to exact registered source/stdin event; no impact on C09 enforcement verdict."}
