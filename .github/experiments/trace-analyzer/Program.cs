using System.Text.Json;
using System.Runtime.InteropServices;
using System.Text;
using Microsoft.Diagnostics.Tracing;
using Microsoft.Diagnostics.Tracing.Parsers.Kernel;

var window = JsonDocument.Parse(File.ReadAllText(args[1])).RootElement;
int rootPid = window.GetProperty("pid").GetInt32();
int rootTid = window.GetProperty("thread_id").GetInt32();
DateTime begin = window.GetProperty("start_utc").GetDateTime().ToUniversalTime();
DateTime end = window.GetProperty("end_utc").GetDateTime().ToUniversalTime();
var processes = new Dictionary<int, Proc>();
var images = new Dictionary<int, List<Module>>();
var logical = new Dictionary<(int, string, string), Metric>();
var physical = new Dictionary<(int, string, string), Metric>();
var faults = new Dictionary<(int, string, string), Metric>();
var samples = new Dictionary<(int, string), long>();
var cpu = new Dictionary<int, double>();
var switched = new Dictionary<int, (int pid, double at)>();
var wait = new Dictionary<int, (double at, string reason)>();
var waitTotals = new Dictionary<string, double>();
var pending = new Dictionary<ulong, (int pid, string file, string op, double at)>();
var devices = new Dictionary<string,string>(StringComparer.OrdinalIgnoreCase);
foreach (var drive in DriveInfo.GetDrives()) {
    var device = new StringBuilder(4096);
    if (Native.QueryDosDevice(drive.Name[..2], device, device.Capacity) != 0)
        devices[device.ToString()] = drive.Name[..2];
}
string Normalize(string path) {
    foreach (var item in devices.OrderByDescending(p=>p.Key.Length))
        if (path.StartsWith(item.Key, StringComparison.OrdinalIgnoreCase)) return item.Value + path[item.Key.Length..];
    return string.IsNullOrEmpty(path) ? "<unknown>" : path;
}
string Drive(string path) => path.Length >= 2 && path[1] == ':' ? path[..2].ToUpperInvariant() : "<unmapped>";
bool Inside(TraceEvent e) { var t=e.TimeStamp.ToUniversalTime(); return t >= begin && t <= end; }
Metric Get(Dictionary<(int,string,string),Metric> map, int pid, string file, string op) {
    var key=(pid,Normalize(file),op);
    if (!map.TryGetValue(key,out var metric)) map[key]=metric=new Metric();
    return metric;
}
using var trace = new ETWTraceEventSource(args[0]);
double startMs = (begin-trace.SessionStartTime.ToUniversalTime()).TotalMilliseconds;
double endMs = (end-trace.SessionStartTime.ToUniversalTime()).TotalMilliseconds;
double firstKernel = double.MaxValue, lastKernel=0;
long events=0, reused=0;
void Process(ProcessTraceData e) {
    if (processes.TryGetValue(e.ProcessID,out var p)) {
        if (e.OpcodeName == "Start" && p.Start != e.TimeStampRelativeMSec) reused++;
    } else processes[e.ProcessID]=new Proc(e.ParentID,Normalize(e.ImageFileName), e.CommandLine, e.TimeStampRelativeMSec);
}
trace.Kernel.ProcessStart += Process;
trace.Kernel.ProcessDCStart += Process;
void Image(ImageLoadTraceData e) {
    if (!images.TryGetValue(e.ProcessID,out var modules)) images[e.ProcessID]=modules=new();
    modules.Add(new Module(e.ImageBase, e.ImageBase+(uint)e.ImageSize,Normalize(e.FileName)));
}
trace.Kernel.ImageLoad += Image;
trace.Kernel.ImageDCStart += Image;
trace.Kernel.PerfInfoSample += e => {
    if (!Inside(e)) return;
    string module="<unresolved>";
    foreach (int pid in new[]{e.ProcessID,0,4}) {
        if (images.TryGetValue(pid,out var modules)) {
            var m=modules.LastOrDefault(m=>e.InstructionPointer>=m.Low && e.InstructionPointer<m.High);
            if (m != null) { module=m.Name; break; }
        }
    }
    var key=(e.ProcessID,module); samples[key]=samples.GetValueOrDefault(key)+1;
};
trace.Kernel.ThreadCSwitch += e => {
    double now=e.TimeStampRelativeMSec;
    if (switched.TryGetValue(e.ProcessorNumber,out var old) && old.pid==e.OldProcessID) {
        double duration=Math.Max(0,Math.Min(now,endMs)-Math.Max(old.at,startMs));
        cpu[old.pid]=cpu.GetValueOrDefault(old.pid)+duration;
    }
    switched[e.ProcessorNumber]=(e.ProcessID,now);
    if (e.NewThreadID==rootTid && wait.Remove(rootTid,out var waiting)) {
        double duration=Math.Max(0,Math.Min(now,endMs)-Math.Max(waiting.at,startMs));
        waitTotals[waiting.reason]=waitTotals.GetValueOrDefault(waiting.reason)+duration;
    }
    if (e.OldThreadID==rootTid) wait[rootTid]=(now,e.OldThreadState+":"+e.OldThreadWaitReason);
};
void Disk(DiskIOTraceData e, string op) {
    if (!Inside(e)) return;
    var m=Get(physical,e.ProcessID,e.FileName,op+"/disk"+e.DiskNumber);
    m.Count++; m.Bytes+=e.TransferSize; m.ElapsedMs+=e.ElapsedTimeMSec;
}
trace.Kernel.DiskIORead += e=>Disk(e,"read");
trace.Kernel.DiskIOWrite += e=>Disk(e,"write");
trace.Kernel.MemoryHardFault += e=> {
    if (!Inside(e)) return;
    var m=Get(faults,e.ProcessID,e.FileName,"hard_fault");
    m.Count++; m.Bytes+=e.ByteCount; m.ElapsedMs+=e.ElapsedTimeMSec;
};
void FileOp(TraceEvent e, string file, ulong irp, long bytes=0) {
    if (!Inside(e)) return;
    var m=Get(logical,e.ProcessID,file,e.EventName); m.Count++;m.Bytes+=bytes;
    if(irp!=0) pending[irp]=(e.ProcessID,file,e.EventName,e.TimeStampRelativeMSec);
}
trace.Kernel.FileIOCreate += e=>FileOp(e,e.FileName,e.IrpPtr);
trace.Kernel.FileIORead += e=>FileOp(e,e.FileName,e.IrpPtr,e.IoSize);
trace.Kernel.FileIOWrite += e=>FileOp(e,e.FileName,e.IrpPtr,e.IoSize);
trace.Kernel.FileIOQueryInfo += e=>FileOp(e,e.FileName,e.IrpPtr);
trace.Kernel.FileIOSetInfo += e=>FileOp(e,e.FileName,e.IrpPtr);
trace.Kernel.FileIODirEnum += e=>FileOp(e,e.FileName,e.IrpPtr);
trace.Kernel.FileIOCleanup += e=>FileOp(e,e.FileName,e.IrpPtr);
trace.Kernel.FileIOClose += e=>FileOp(e,e.FileName,e.IrpPtr);
trace.Kernel.FileIOFlush += e=>FileOp(e,e.FileName,e.IrpPtr);
trace.Kernel.FileIOOperationEnd += e=> {
    if (Inside(e) && pending.Remove(e.IrpPtr,out var item)) {
        var m=Get(logical,item.pid,item.file,item.op);
        m.ElapsedMs+=e.TimeStampRelativeMSec-item.at; m.Completed++;
    }
};
trace.Kernel.All += e=> { events++;firstKernel=Math.Min(firstKernel,e.TimeStampRelativeMSec);lastKernel=Math.Max(lastKernel,e.TimeStampRelativeMSec); };
trace.Process();
var tree=new HashSet<int>{rootPid};
bool added=true;
while(added) { added=false;foreach(var p in processes) if(tree.Contains(p.Value.Parent) && tree.Add(p.Key)) added=true; }
string Name(int pid) => processes.TryGetValue(pid,out var p) ? Path.GetFileName(p.Image) : "pid:"+pid;
string Group(int pid) => tree.Contains(pid) ? (pid==rootPid?"test-parent/":"test-child/")+Name(pid) : "other/"+Name(pid);
object Totals(Dictionary<(int,string,string),Metric> map, bool byPath, int limit) => map
    .GroupBy(p=>new {process=Group(p.Key.Item1),drive=Drive(p.Key.Item2),operation=p.Key.Item3,path=byPath?p.Key.Item2:""})
    .Select(g=>new {g.Key.process,g.Key.drive,g.Key.operation,g.Key.path,count=g.Sum(p=>p.Value.Count),bytes=g.Sum(p=>p.Value.Bytes),operation_ms_sum=g.Sum(p=>p.Value.ElapsedMs),completed=g.Sum(p=>p.Value.Completed)})
    .OrderByDescending(g=>g.operation_ms_sum).ThenByDescending(g=>g.count).Take(limit).ToArray();
var result = new {
    schema="exploratory-ownership-trace-v1",root_pid=rootPid,devices,events,
    events_lost=trace.EventsLost,first_kernel_ms=firstKernel,last_kernel_ms=lastKernel,
    window_start_ms=startMs,window_end_ms=endMs,starts_before_test=firstKernel<=startMs,ends_after_test=lastKernel>=endMs,
    pid_reuse_observations=reused,
    processes=processes.Where(p=>tree.Contains(p.Key)).Select(p=>new{pid=p.Key,parent=p.Value.Parent,image=p.Value.Image,command=p.Value.Command}),
    cpu_seconds_by_process=cpu.GroupBy(p=>Group(p.Key)).Select(g=>new{process=g.Key,seconds=g.Sum(p=>p.Value)/1000}).OrderByDescending(g=>g.seconds),
    cpu_samples_by_module=samples.GroupBy(p=>new{process=Group(p.Key.Item1),module=p.Key.Item2}).Select(g=>new{g.Key.process,g.Key.module,samples=g.Sum(p=>p.Value)}).OrderByDescending(g=>g.samples).Take(40),
    parent_off_cpu_seconds_by_prior_state_including_ready_time=waitTotals.ToDictionary(p=>p.Key,p=>p.Value/1000),
    logical_io=Totals(logical,false,300),logical_top_paths=Totals(logical,true,50),
    physical_io=Totals(physical,false,200),physical_top_paths=Totals(physical,true,50),
    hard_faults=Totals(faults,false,100),hard_fault_top_paths=Totals(faults,true,30),
    notes="I/O duration sums may overlap; file I/O is logical, disk I/O is physical; parent cProfile adds overhead; trace analyzed after recording stopped."
};
string json=JsonSerializer.Serialize(result);
File.WriteAllText(args[2],json);
Console.WriteLine("ETW_SUMMARY "+json);
if(trace.EventsLost!=0 || firstKernel>startMs || lastKernel<endMs || !processes.ContainsKey(rootPid)) Environment.Exit(2);

record Proc(int Parent,string Image,string Command,double Start);
record Module(ulong Low,ulong High,string Name);
class Metric { public long Count,Bytes,Completed;public double ElapsedMs; }
static class Native {
    [DllImport("kernel32.dll",CharSet=CharSet.Unicode)] public static extern uint QueryDosDevice(string name,StringBuilder target,int size);
}
