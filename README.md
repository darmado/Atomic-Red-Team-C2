<p><img src="https://blackbot.io/wp-content/uploads/2020/11/artic_c2_logo_red_v1-e1606038603815.png" width="350px" /></p>

# DESCRIPTION

ARTi-C2 is a modern execution framework built to empower security teams to scale attack scenario execution from single and multi-breach point targets with the intent to produce actionable attack intelligence that improves the effectiveness security products and incident response.

# PHILOSOPHY

Blackbot Labs believes in creating tools where vendor solutions and open source can be provisioned and managed together by all organizations with the intent to deliver actionable attack intelligence organizations can use to define clear objectives and drive strategic security program initiatives.

### *Commitment*

- **INTEGRITY** 
We develop tools and frameworks that produce accurate attack intelligence to help security teams evaluate the integrity of their security solutions.

- **TRANSPARENCY**
We work under the umbrella of full transparency during all phases of tool and framework development. From striking up ideas with our community to enhancing the capabilities of tools used by red teams all over the world; if Blackbot Labs is brewing up a new tool or framework, you'll know about it.


- **AGILITY**
We take pride in enabling lean security teams to remain agile and focused on developing a unique trade-craft that's agnostic to certain tools developed by the red team community. Whether you're keeping tight margins between \(MTTD\) and  \(MTTR\) metrics or evaluating security controls, we'll be here building tools to help you get the job done faster.


- **SCALABILITY**
Scaling operational activities is critical to sustaining efficient security ecosystem workflows in modern environments. If our tools don't help you scale your operational capabilities, let us know and we'll fix it. 


- **FLEXIBILITY**
Blackbot Labs builds and delivers open source tools with the flexibility and intent for security professionals to improve their trade-craft and scale security testing initiatives in IT, OT, cloud-native and hybrid workspaces.


- **RAPID DEPLOYMENT**
Facilitating rapid deployment models is important to us. We'll do our best to deliver practical deployment frameworks that facilitate advanced security eco-systems and data-driven pipelines. 

</br>
</br>
</br>

# CAPABILITIES

ARTi-C2 Core features and capabilities are sourced from SILENTTRINITY and atomic tests executed through Boo are from [ATOMIC-RED-TEAM](https://github.com/redcanaryco/atomic-red-team). All other feature enhancements were built to ensure operational trade-craft, agility, scalability, and rapid execution is not compromised.


| CAPABILITY | DESCRIPTION |
| ------ | ------ |
| **Rapid Deployment** | Automate and scale testing efforts from single and multi-target breach points located in different regional environments
| **Modern Command & Control** | *Implant and Server Comms:* Uses SILENTRINITY's ECDHE Encrypted C2 Communication capabilities to encrypt C2 traffic over HTTPS. </br>*Client and Server Comms*: Uses Asyncio, WebSockets, and a prompt-toolkit CLI. Notable features include:     *- Implant location tagging: Helpful when managing singals and breachpoints in different regions. NGROK integration* - Great for staging payloads and deploying them with ngrok URLs 
| **Standard Signature Header** | JSON `PID: , Date(UTC), IsHighIntegrity, HostName, CurrentUser , IsUserAdmin, IPv4, IPv6`
| **JSON Logging Support** | Streamline, ingest, decode, and analyze evidence with your ELK stack or any Analytics platform ready to parse JSON.| 
||
| **Stageless in Memory Code Execution** |  Execute Atomic Red Team tests from an `unmanaged powershell process` with low, medium, high integrity. 
| **Dynamic Attack Formations** | Execute attack-chains without the need to recompile or restart ARTi-C2. Currently supports 3 differnt attack functions. `Attack Chains`, `Attack Profiles`, and `Attack Scenarios`|
| **Modular Payload Delivery** | ARTi-C2 leverages [SILENTRINITY's](https://github.com/byt3bl33d3r/SILENTTRINITY) framework uses `unmanaged powershell` and `stageless powershell` stagers to compile and execute Red Team Atomic test payloads in memory,  *"AS IS"*  
| **Operational Management** | Job IDs are included for controller execution and evidence collection. They're great for event  analysis and evidence correlation. `"job_id": "D3l820IWpyi67"`| **Atomic Updates** | The ART port pipeline is triggered by repo updates at [ATOMIC-RED-TEAM](https://github.com/redcanaryco/atomic-red-team)   

## MITRE ATT&CK COVERAGE
- [MITRE ATT&CK Coverage Map](https://attack.blackbot.io)

</br>
</br>


# USE CASES 
- SOCs need to evaluate and improve EDR solutions in minutes
- Organizations are evaluating different EDR/AV solutions for Windows OS

**Organizations need to:** 
- execute APT group tactics in controlled environments
- demonstrate the ability to block common attacks from disk and memory
- execute lightweight atomoics remotely
- benchmark critical risk profiles against MITRE ATT&CK before releasing systems to Corp IT/production
- execute ransomware tactics mapped to ATT&CK safely
- keep tight margins between \(MTTD\) and \(MTTR\) metrics
- continually improve SOAR workbooks
- evaluate host security controls between different business units, and regions.

</br>

# LOGGING CAPABILITIES

By default, ARTIC-C2 logs are written to ARTIC-C2's current working directory in `/Atomic-Red-Team-Intelligence-C2/logs/`.
Session logs include:

</br>

- `utc_timestamp` : UTC timestamp
- `session`: Target session GUID
- `job_id`: Unique Job execution ID
- `ttp_data`: Technique ID
- `evidence`: Base64 encoded evidence collected from breach point target
- `evidence_status`: Status to indicate if the TTP executed was blocked or not. 
    - 1: TTP was not blocked
    - 0: TTP was partially blocked, or failed to execute

</br>
</br>

**EXECUTION SIGNATURE HEADER**

Execution signature headers are used to verify if atomics are blocked by any defenses. In some cases, the actual atomic commands may not return data in STDOUT. However, if the execution signature header returns header information, then this indicates the source code compiled, was loaded into the CLR, and executed on the target breach point. The execution signature header includes:

- `PID`: used during technique execution
- `Date`: UTC time stamp produced from the breach point target
- `IsHighIntegrity`: Process integrity status
- `HostName`:  breach point target host name
- `CurrentUser`: Current user. Great for tracking when users are impersonated
- `IsUserAdmin`: Admin status
- `IPv4`: IPv4 address info
- `IPv6`: IPv6 address info

</br>
</br>

**SAMPLE EXECUTION EVENT LOG**

T1069.001-2 was executed in memory

```
2021-08-21 07:42:21,146 - {"utc_timestamp": "2021-08-21T07:42:21Z", "msg": "Technique executed:", "controller": "Discovery/T1069.001-2", "last_updated_by": "Blackbot, Inc.",
"ttp_id": "T1069.001", "ttp_opts": {"OutString": {"Description": "Appends Out-String to the PowerShellCode", "Required": false, "Value": true}, "BypassLogging": 
{"Description": "Bypasses ScriptBlock and Techniques logging", "Required": false, "Value": true}, "BypassAmsi": {"Description": "Bypasses AMSI", "Required": false, "Value": true}},
 "decompressed_file": "n/a", "file_name": "n/a", "gzip_file": "n/a", "language": "boo", "references": ["System.Management.Automation"], "run_in_thread": "n/a", "job_id": "B5ppBWed5NF6c"}
```

</br>
</br>

**SAMPLE EVIDENCE COLLECTION LOG**

Evidence collected from target breach point after executing T1069.001-2.

```
2021-08-21 07:42:25,076 - {"utc_timestamp": "2021-08-21T07:42:25Z", "session": "17ed378a-8cb9-4690-9087-e894c2b1e0a2", "job_id": "B5ppBWed5NF6c", "ttp_data": "T1069.001", "evidence": "IntQSUQ6IDU1NTYsIERhdGUoVVRDKTogMjAyMS0wOC0yMVQwNzo0MjoyNC45MDczMjQ5WiwgSXNIaWdoSW50ZWdyaXR5OiB0cnVlLCBIb3N0TmFtZTogYWQtZGMxLCBDdXJyZW50VXNlcjogZGVlcHJvb3RcXHJ1c3NlbF9oYW5jb2NrLCBJc1VzZXJBZG1pbjogdHJ1ZSwgSVB2NDogWzEwLjEuMC4xMDAsIDE2OS4yNTQuMTM0LjExMV0sIElQdjY6IFtmZTgwOjpkZGUxOjIyYTo3YmEzOmZlMGIlNSwgZmU4MDo6YjhmODpiNDIxOjI3Yzg6ODY2ZiUxMV19XHJcbk5hbWUgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBEZXNjcmlwdGlvbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIFxyXG4tLS0tICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLS0tLS0tLS0tLS0gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBcclxuQ2VydCBQdWJsaXNoZXJzICAgICAgICAgICAgICAgICAgICAgICAgIE1lbWJlcnMgb2YgdGhpcyBncm91cCBhcmUgcGVybWl0dGVkIHRvIHB1Ymxpc2ggY2VydGlmaWNhdGVzIHRvIHRoZSBkaXJlY3RvcnkgICAgXHJcblJBUyBhbmQgSUFTIFNlcnZlcnMgICAgICAgICAgICAgICAgICAgICBTZXJ2ZXJzIGluIHRoaXMgZ3JvdXAgY2FuIGFjY2VzcyByZW1vdGUgYWNjZXNzIHByb3BlcnRpZXMgb2YgdXNlcnMgICAgICAgICAgICAgIFxyXG5BbGxvd2VkIFJPREMgUGFzc3dvcmQgUmVwbGljYXRpb24gR3JvdXAgTWVtYmVycyBpbiB0aGlzIGdyb3VwIGNhbiBoYXZlIHRoZWlyIHBhc3N3b3JkcyByZXBsaWNhdGVkIHRvIGFsbCByZWFkLW9ubHkgZG8uLi5cclxuRGVuaWVkIFJPREMgUGFzc3dvcmQgUmVwbGljYXRpb24gR3JvdXAgIE1lbWJlcnMgaW4gdGhpcyBncm91cCBjYW5ub3QgaGF2ZSB0aGVpciBwYXNzd29yZHMgcmVwbGljYXRlZCB0byBhbnkgcmVhZC1vbmx5Li4uXHJcbiI=",
"evidence_status": "1"}
```

<br/>
<br/>

**SAMPLE HEADER SIGNATURE**

```
"{PID: 5556, Date(UTC): 2020-01-02T06:55:47Z, IsHighIntegrity: true, HostName: ad-dc1, CurrentUser: artic\\c2operator, IsUserAdmin: true,
IPv4: [10.1.0.100, 169.254.134.111], IPv6: [fe80::dde1:22a:7ba3:fe0b%5, fe80::b8f8:b421:27c8:866f%11]}
```

</br>
</br>

**SAMPLE BASE64 DECODED EVIDENCE LOG**

```
"{PID: 5556, Date(UTC): 2021-08-21T07:42:24.9073249Z, IsHighIntegrity: true, HostName: ad-dc1, CurrentUser: deeproot\\russel_hancock, IsUserAdmin: true,
IPv4: [10.1.0.100, 169.254.134.111], IPv6: [fe80::dde1:22a:7ba3:fe0b%5, fe80::b8f8:b421:27c8:866f%11]}
Name                                    Description
----                                    -----------
Cert Publishers                         Members of this group are permitted to publish certificates to the directory
RAS and IAS Servers                     Servers in this group can access remote access properties of users
Allowed RODC Password Replication Group Members in this group can have their passwords replicated to all read-only do...
Denied RODC Password Replication Group  Members in this group cannot have their passwords replicated to any read-only...
"
```

# GENERAL REQUIREMENTS

#### Listeners

By default, listeners bind to the system's interface with HTTPS:443 and HTTP:80. Listeners must be accessible from tbe assumbed breach point target. Set your Callback URLs in the `:> listeners` context prior to generating any stager. 

</br>
</br>


## BASIC INSTALL

1. `git clone https://github.com/blackbotinc/Atomic-Red-Team-Intelligence-C2.git`
2. `cd ./Atomic-Red-Team-Intelligence-C2`
3. `./install.sh install`

</br>
</br>


**DEPLOYMENT OPTIONS**

ARTIC-C2 enables flexible deployment models to suit all atomic test case execution requirements. While there are a few client-side console dependencies relative caching, the client console is not required to run on the same system as the team server. Soon, we'll package and release a dedicated client.

**NOTE:** The examples provided below assume ARTIC-C2 will be started from the same instance.

**Start WSS on the default port and produce an adhoc log**
- server: `artic2.py wss 127.0.0.1 Art1.c25rvr >> /var/log/artic2.log &`
- client: `artic2.py client wss://operator:Art1.c25rvr@127.0.0.1:5000`

</br>
</br>

**Start WSS on the default port in foreground**
- server: `artic2.py wss 127.0.0.1 Art1.c25rvr`
- client: `artic2.py client wss://operator:Art1.c25rvr@127.0.0.1:5000`

</br>
</br>

**Start WSS on port 5443, bind to 10.0.0.43, produce adhoc log and connect two clients**
- server: `artic2.py wss 10.0.0.43:5443 Art1.c25rvr >> /var/log/artic2.log &`
- client1: `artic2.py client wss://operator1:Art1.c25rvr@10.0.0.43:5443`
- client2: `artic2.py client wss://operator2:Art1.c25rvr@10.0.0.43:5443`

</br>
</br>

### DOCUMENTATION:

- In progress. 

</br>


## GET INVOLVED

Contribute atomic test cases for the folks at [Red Canary](https://github.com/redcanaryco/) 
-  [Contributing Atomic Test Cases](https://github.com/redcanaryco/atomic-red-team/wiki/Contributing)

- Join the Atomic Red Team Slack Channel
- [https://slack.atomicredteam.io/](https://slack.atomicredteam.io/)

</br>

## CODE OF CONDUCT

Blackbot Labs operates under the umbrella of full transparency while ensuring end-user privacy remains a top priority. For more details on how we operate with our community, visit our community page.

[https://blackbot.io/community]()

</br>

## CREDITS & ACKNOWLEDGEMENTS 

- Marcello Salvati [@byt3bl33d3r](https://twitter.com/byt3bl33d3r) and all [SILENTRINITY](https://github.com/byt3bl33d3r/SILENTTRINITY) c2 project contributors
- [Red Canary](https://github.com/redcanaryco) and all [ATOMIC RED TEAM](https://github.com/redcanaryco/atomic-red-team) project contributors
- [Atomic Red Team Community](https://slack.atomicredteam.io/)  
