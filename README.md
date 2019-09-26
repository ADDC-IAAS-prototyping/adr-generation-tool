# pattern-config-checking
Repository for some concepts around pattern and configuration checking for service meshes and other fancy microservice tech.

## General
### ADR Support
We embrace the concept of [Architectural Decision Records](https://adr.github.io). This repository works with the [ADR markdown format](https://github.com/npryce/adr-tools/blob/master/doc/adr/0004-markdown-format.md):  
1. First, a design pattern is passed within the CLI
2. Depending of the selected pattern, requests are prompted for relevant metrics of the pattern configuration.
3. After passing the desired parameters for the configuration, an ADR for the pattern configuration is generated and stored in [doc/architecture/decisions](doc/architecture/decisions).
4. In the next step, the now existing ADR is crawled for the **Config Set** which contains a dictionary with the parameter decisions.


### Rate Limits
Currently supported provider formats:  
* Istio - [Memquota](https://istio.io/docs/tasks/policy-enforcement/rate-limiting/)
* Kong - [Rate limiting](https://docs.konghq.com/hub/kong-inc/rate-limiting/)

### Circuit Breaking / Passive health checks
Currently supported provider formats:  

## Getting started
### Prerequisites
* Python 2.7.x or Python 3.7.x
* pip 18.x or pip3 19.0.x
### Install packages
    > pip install -r service-mesh-patterns/requirements.txt

### Generate ADR for a pattern
Make sure that the configuration file which needs to be analyzed is stored as  
    
        service-mesh-patterns/sources/config_template.yaml
1. Navigate to `service-mesh-patterns`:  
    
    > cd service-mesh-patterns
2. Start the **pattern-config-checker**:

    > python init.py
3. A dialog will be displayed which determine the content of the markdown document, e.g.

    * Pattern type (Rate Limit / Circuit Breaker)
    * For Rate Limit:

        * Rate limit interval in seconds
        * Number of allowed requests
        * DestinationID for which the rate limiting will be checked
    * For Circuit Breaker:
4. For the passed configuration, a corresponding ADR will be generated at  

    > service-mesh-patterns/doc/architecture/decisions/PATTERN_TYPE_adr_0001.md

5. The checking script crawls the generated ADR for the desired configuration of the selected pattern and analyzes the stored `config_template.yaml` for the actual configuration state. 
    
The providers for which the script automatically identifies the format of the stored template are listed above.

