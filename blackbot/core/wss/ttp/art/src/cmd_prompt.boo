import System
import System.Diagnostics
import System.Security.Principal
import System.Globalization
import System.Net

/*Original Code from: https://github.com/byt3bl33d3r/SILENTTRINITY*/
/*Adversaries may abuse the at.exe utility to perform task scheduling for initial or recurring execution of malicious code. The [at](https://attack.mitre.org/software/S0110) utility exists as an executable within Windows for scheduling tasks at a specified time and date. Using [at](https://attack.mitre.org/software/S0110) requires that the Task Scheduler service be running, and the user to be logged on as a member of the local Administrators group.

An adversary may use at.exe in Windows environments to execute programs at system startup or on a scheduled basis for persistence. at can also be abused to conduct remote Execution as part of Lateral Movement and or to run a process under the context of a specified account (such as SYSTEM).
*/

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

public static def Header():
    currentProcess = Process.GetCurrentProcess()

    culture = CultureInfo("en-US")
    dateTime = DateTime().UtcNow.ToString("o", culture)

    user = WindowsIdentity.GetCurrent().Name
    hostname = Dns.GetHostName()

    ipAddressList = Dns.GetHostAddresses(hostname)

    allIPv4 = []
    allIPv6 = []
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

    Console.WriteLine("{{PID: {1}, Date(UTC): {0}, IsHighIntegrity: {6}, HostName: {2}, CurrentUser: {3}, IsUserAdmin: {7}, IPv4: [{4}], IPv6: [{5}]}}", dateTime, currentProcess.Id, hostname.ToLower(), user.ToLower(), allipsv4, allipsv6, integrity, isAdmin())

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
    Header()
    lines = CmdPromptScript.Split(('\n', ), StringSplitOptions.None)
    
    command_list = []
    commands = false
    cleanup = false
    prereq = false
    get_prereq = false
    for line in lines:
        if line[0:9] == '#commands':
            commands = true
            cleanup = false
            prereq = false
            get_prereq = false
            continue

        elif line[0:17] == '#cleanup_commands':
            commands = false
            cleanup = true
            prereq = false
            get_prereq = false
            continue
 
        elif line[:19] == '#get_prereq_comands':
            commands = false
            cleanup = false
            prereq = false
            get_prereq = true
            continue
        
        elif line[:16] == '#prereq_commands':
            commands = false
            cleanup = false
            prereq = true
            get_prereq = false
            continue
        
        if commands:
            if len(line) > 0:
                command_list.Add(line)
        
        elif cleanup:
            if len(line) > 0:
                command_list.Add(line)
        
        elif prereq:
            if len(line) > 0:
                command_list.Add(line)
        
        elif get_prereq:
            if len(line) > 0:
                command_list.Add(line)

    return command_list
	
public static def Main():

    command_list = Parser(`CMD_TTP`)
    for c in command_list:
        print(c)

    try:
        Serialization(command_list)
    except:
        Console.WriteLine(' * [!] Atomic test failed. ')
