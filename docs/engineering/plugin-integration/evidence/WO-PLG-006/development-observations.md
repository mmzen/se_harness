# Development observations

Early direct calibration failures are retained here as observations, not native
host acceptance. The first eight-test run had four failures because the isolated
host environment deliberately omitted the `OS` variable. The guard now observes
the actual Windows platform. The second run had three failures because Windows
PowerShell's .NET Framework lacks ProcessStartInfo.StandardInputEncoding; stdin
now uses explicit UTF-8 bytes through the process stream. After review added an
actual interpreter-version probe, a nine-test run had three failures from native
PowerShell stripping embedded Python expression quotes. The fixed expression
requires no embedded quotes. The subsequent nine-test run passed in 17.238 s.

Each failure returned UNREADY or denial; none established host qualification.
These command results were observed during development before durable acceptance
capture. The later focused command/result capture supplies rerunnable evidence.

The C04 readable stdout/stderr projections initially contained doubled CRLF from
writing captured Windows process bytes through text-mode output. Those two text
projections now use LF. Their original structured command captures, including
captured process stdout/stderr strings, remain unchanged in commands.json.
