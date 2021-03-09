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
| **Dynamic Attack Formations** | Execute attack-chains without the need to recompile or restart ARTi-C2. Currently supports 3 differnt attack functions:</br>    - Attack Chains:</br>- Attack Profiles:</br>- Attack Scenarios:|
| **Modular Payload Delivery** | ARTi-C2 leverages [SILENTRINITY's](https://github.com/byt3bl33d3r/SILENTTRINITY) framework to deliver Red Team Atomic tests "As is" through:</br>- `unmanaged powershell`</br>- `stageless powershell`
| **Operational Management** | Job IDs are included for controller execution and evidence collection. They're great for event  analysis and evidence correlation. `"job_id": "D3l820IWpyi67"`| **Atomic Updates** | The ART port pipeline is triggered by repo updates at [ATOMIC-RED-TEAM](https://github.com/redcanaryco/atomic-red-team)   

## MITRE ATT&CK COVERAGE
- [MITRE ATT&CK Coverage Map](https://attack.blackbot.io)




## USE CASES 
- SOCs need to evaluate and improve EDR solutions in minutes
- Organizations are evaluating different EDR/AV solutions for Windows OS

- Organizations need to: 
- execute APT group tactics in controlled environments
- demonstrate the ability to block common attacks from disk and memory
- execute lightweight atomoics remotely
- benchmark critical risk profiles against MITRE ATT&CK before releasing systems to Corp IT/production
- execute ransomware tactics mapped to ATT&CK safely
- keep tight margins between \(MTTD\) and \(MTTR\) metrics
- continually improve SOAR workbooks
- evaluate host security controls between different business units, and regions.


## DOCUMENTATION:
- In progress. 

## GET INVOLVED
Contribute atomic test cases for the folks at [Red Canary](https://github.com/redcanaryco/) 
-  [Contributing Atomic Test Cases](https://github.com/redcanaryco/atomic-red-team/wiki/Contributing)

- Join the Atomic Red Team Slack Channel
- [https://slack.atomicredteam.io/](https://slack.atomicredteam.io/)

## CODE OF CONDUCT

Blackbot Labs operates under the umbrella of full transparency while ensuring end-user privacy remains a top priority. For more details on how we operate with our community, visit our community page.

[https://blackbot.io/community](https://blackbot.io/community)


## CREDITS & ACKNOWLEDGEMENTS 

- Marcello Salvati [@byt3bl33d3r](https://twitter.com/byt3bl33d3r) and all [SILENTRINITY](https://github.com/byt3bl33d3r/SILENTTRINITY) c2 project contributors
- [Red Canary](https://github.com/redcanaryco) and all [ATOMIC RED TEAM](https://github.com/redcanaryco/atomic-red-team) project contributors
- [Atomic Red Team Community](https://slack.atomicredteam.io/)  
