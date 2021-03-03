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
Scaling operational activities is critical to sustaining efficient security ecosystem workflows in modern-day environments. If our tools don't help you scale your operational capabilities, let us know and we'll fix it. 


- **FLEXIBILITY**
Blackbot Labs builds and delivers open source tools with the flexibility and intent for security professionals to improve their trade-craft and scale security testing initiatives in IT, OT, cloud-native and hybrid workspaces.


- **RAPID DEPLOYMENT**
Facilitating rapid deployment models is important to us. We'll do our best to deliver practical deployment frameworks that facilitate advanced security eco-systems and data-driven pipelines. 

# CAPABILITIES

ARTi-C2 Core features and capabilities are sourced from SILENTTRINITY and atomic tests executed through Boo are from [ATOMIC-RED-TEAM](https://github.com/redcanaryco/atomic-red-team). All other feature enhancements were built to ensure operational trade-craft, agility, scalability, and rapid execution is not compromised.


| CAPABILITY | DESCRIPTION |
| ------ | ------ |
| **Rapid Deployment** | Automate and scale testing efforts from single and multi-target breach points located in different regional environments
| **Modern Command & Control** | *Implant and Server Comms:* Uses the power of SILENTRINITY's ECDHE Encrypted C2 Communication capabilities to encrypt all C2 traffic. Implant management capabilities allow security teams to use multi-channel communication techniques mapped to MITRE ATT&CK. </br>*Client and Server Comms*: Uses Asyncio and WebSockets are used by a modern CLI powered by prompt-toolkit. Notable features include:     - Implant location tagging NGROK integration 
| **Standard Signature Header** | JSON `PID: , Date(UTC), IsHighIntegrity, HostName, CurrentUser , IsUserAdmin, IPv4, IPv6`
| **JSON Logging Support** | Streamline, ingest, decode, and analyze evidence with your ELK stack or any Analytics platform ready to parse JSON.| 
||
| **Stageless in Memory Code Execution** |  Execute Atomic Red Team tests from `unmanaged powershell process`. 
| **Dynamic Attack Formations** | Execute attack-chains without the need to recompile or restart ARTi-C2. Currently supports 3 differnt attack functions:</br>    - Attack Chains:</br>- Attack Profiles:</br>- Attack Scenarios:|
| **Modular Payload Delivery** | ARTi-C2 leverages [SILENTRINITY's](https://github.com/byt3bl33d3r/SILENTTRINITY) framework to deliver Red Team Atomic tests "As is" through:</br>- `unmanaged powershell`</br>- `stageless powershell`
| **Operational Management** | Job IDs are included for controller execution and evidence collection. They're great for event  analysis and evidence correlation. `"job_id": "D3l820IWpyi67"`| **Atomic Updates** | The ART port pipeline is triggered by repo updates at [ATOMIC-RED-TEAM](https://github.com/redcanaryco/atomic-red-team)   

## MITRE ATT&CK COVERAGE
- [MITRE ATT&CK Coverage Map](https://attack.blackbot.io)




## USE CASES 
- SOCs need to evaluate and improve EDR solutions in minutes
- Organizations are evaluating different EDR/AV solutions for Windows OS
- Organizations need to simulate APT group tactics, techniques, and procedures without the need to go 'ALL IN" on research and planning.
- Organizations need to know if their assets are protected against common attacks from disk and memory
- Organizations need to execute lightweight test cases mapped to MITRE ATT&CK and prove their assets are protected
- Organizations need to benchmark critical risk profiles against the ATT&CK framework before releasing systems to Corp IT/production
- Organizations need to simulate ransomware tactics without introducing risk in order to develop specific detection and prevention capabilities
- Organizations are required to keep tight margins between mean time to detect \(MTTD\) and mean time to respond \(MTTR\) metrics can demonstrate improvement
- Organizations need to continually improve SOAR workbooks
- Organizations need to evaluate system risk profiles across departments with thousands of systems. We recommend testing one and deploying the risk profile configuration settings based on your organizations' policy/system deployment orchestration framework. 

## GET STARTED

```- In Progress
```

## DOCUMENTATION NOTES:
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
