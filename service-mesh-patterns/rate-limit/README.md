# Comparison of Rate Limit YAML models for Istio and Kong

## General aspects:
Both Kong and Istio support usage of **Redis** and a **Custom** policy.

For the comparison, we will focus on the custom policy within both models. Also Istios configuration files are more blown-up with Rate-Limit-Rules consisting of:
* **handler:** Here the actual configuration for the rate limiting policies is defined
* **instance:** Defines how quota is dimensioned by Istio Mixer
* **QuotaSpec:** Defines quota name and amount that the client should request
* **QuotaSpecBinding:** Conditionally associates **QuotaSpec** with one or more services
* **rule:** Defines when an **instance** is dispatched to the memquota adapter (binds an instance to an handler).

We will focus on the configuration of the **handler** in Istio and the declarative configuration **plugin** in Kong.

## Key properties for generic rate limiting configuration
* **Target:** ID of the service or entity, which will be the target of the requests, observed in this rate limiting policy.
* **Source / Origin:** ID of the endpoint that sends requests to the target service. This could be an IP or an registered service in the mesh itself.
* **#Requests:** Number of tolerated requests (from a predefined source / origin) in a certain time interval.
* **Interval:** Time interval for counting requests from origin / source to target service.
* **WindowType:** Type of the windowing with the predefined interval.


## Model comparison

| **Property**        	| **Kong**                  	| **Istio**                                                                                            	|
|-----------------	|-----------------------	|--------------------------------------------------------------------------------------------------	|
| Target          	| `service_id` / `route_id` 	|                     `spec.params.quotas.overrides.dimensionsEntry.destination`                     	|
| Source / Origin 	|      `consumer_id`      	|                        `spec.params.quotas.overrides.dimensionsEntry.source`                       	|
| #Requests       	| `config.<time>.value()` 	|    `spec.params.quotas.overrides.dimensionsEntry.maxAmount`  else  `spec.params.quotas.maxAmount`    	|
| Interval        	|  `config.<time>.key()`  	| `spec.params.quotas.overrides.dimensionsEntry.validDuration` else `spec.params.quotas.validDuration` 	|
| WindowType      	|     Fixed "normal"    	|                        `SLIDING_WINDOW` else `ROLLING_WINDOW` or `FIXED_WINDOW`                        	|

## Challenges
1. *Time window / Interval:*  
    **Istio:** `validDuration` can be passed any desired time interval value in seconds  
    **Kong:** Pass tolerated `#Requests` for `second`, 60 seconds (`minute`), 3600 seconds (`hour`), for `day` and/or for a `year`. However, there is nothing between those time interval configurations supported.

2. *Algorithm:*  
    **Istio:** `SLIDING_WINDOW` for custom policy (memquota) or `ROLLING/FIXED_WINDOW` for redisquota.  
    **Kong:** No algorithm selection.

3. *Conditional expressions:*  
    **Istio:** User can formulate expressions that must be matched to enable this rate limiting policy (such as "user must not be logged-in")  
    **Kong:** Only one boolean expression `enabled`

4. *Fault-tolerance handling:*  
    **Istio:** No fault-tolerance  
    **Kong:** Fault-tolerance acceptance rule if some troubles with connecting to third-party databases come up.

5. *Location of YAML file:*  
    **Istio:** Could be located anywhere  
    **Kong:** Typically a section in the global declarative configuration file

6. *Different models wrt. overrides of rules:*  
    **Istio:** A general quota handler with maxAmount and validDuration is created in the first place. After that, overrides define further refined quotas for specific use-cases. These refined quotas can differ in their targets and sources so generally more effort is necessary to figure out if a given rate limiting policy is implemented in the Istio quota handler.  
    **Kong:** Very straightforward since there is one target per plugin.


### Note:
    Most of the properties that are unique for the corresponding meshes are optional or get an default value passed if not set explicitly. In conclusion, focusing on the mentioned **Key Properties** will most probably be feasible to track down if the configuration is done right.