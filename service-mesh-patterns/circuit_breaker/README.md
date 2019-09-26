# Comparison of Circuit Breaker for Istio and Kong

## General aspects:
Both Kong and Istio include health check configurations interleaved with load balancing and other pooling configuration for service instances.

## Comparison of the configuration parameters
| Kong                                | Istio                     | Generic           | Description                                                  |
|-------------------------------------|---------------------------|-------------------|--------------------------------------------------------------|
| tcp_failures http_failures timeouts | consecutiveErrors         | failCount         | allowed #failures before circuit breaker ejects service      |
| http_statuses                       | (here this is always 5xx) | failStatus        | HTTP statuses which are observed                             |
| -                                   | interval                  | interval          | period in which #failures are counted                        |
| -                                   | baseEjectionTime          | recoveryTime      | period until circuit is closed again                         |
| -                                   | maxEjectionPercent        | poolRecoveryBound | maximal #hosts/#services allowed in recovery state           |
| -                                   | minHealthPercent          | poolHealthBound   | #hosts/#services allowed before circuit breaking is disabled |

## Checking properties
The following set of properties for checking a given circuit breaker configuration can be considered feasible minimal pattern description set:
* failCount
* interval
* recoveryTime

### Issues / Challenges
#### interval
    In Kong, there is no property for passive health checks that describes the time interval in which the number of allowed failures/timeouts are counted, before the circuit breaker ejects the service/host instance
#### recoveryTime
    In Kong, there is no property for passive health checks that describes the time interval for a service/host instance to be in recovery mode before it gets requests routed to again.
#### http statuses
    In Istio, if the errors are HTTP-based, there are only 5xx statuses considered, whereas in Kong, the HTTP statuses can explicitly be defined to enable passive health checks for, e.g., HTTP 429.
#### Configuration file format
    The Kong config file is written in JSON which leads to the adapter for this pattern checking hard to reuse for other provider formats.