# pattern-config-checking
Repository for some concepts around pattern and configuration checking for service meshes and other fancy microservice tech.

## ADR Support
We embrace the concept of [Architectural Decision Records](https://adr.github.io). This repository works with the [ADR markdown format](https://github.com/npryce/adr-tools/blob/master/doc/adr/0004-markdown-format.md):  
1. First, a design pattern is passed within the CLI
2. Depending of the selected pattern, requests are prompted for relevant metrics of the pattern configuration.
3. After passing the desired parameters for the configuration, an ADR for the pattern configuration is generated and stored in [doc/architecture/decisions](doc/architecture/decisions).
4. In the next step, the now existing ADR is crawled for the **Config Set** which contains a dictionary with the parameter decisions.


## Rate Limits
Currently supported provider formats:  
* Istio - [Memquota](https://istio.io/docs/tasks/policy-enforcement/rate-limiting/)
* Kong - [Rate limiting](https://docs.konghq.com/hub/kong-inc/rate-limiting/)

## Circuit Breaking / Passive health checks
Currently supported provider formats:  

