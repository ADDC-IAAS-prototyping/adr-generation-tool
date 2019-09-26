# Circuit Breaking - Kong
Health checks in Kong are configured within the [Admin API](https://docs.konghq.com/0.12.x/admin-api/#add-upstream) config file. 

## Passive health checks / Circuit Breaking
[Passive health checking](https://docs.konghq.com/0.12.x/health-checks-circuit-breakers/) in Kong can be enables by specifying its configuration under `healthchecks.passive` in the [upstream configuration](https://docs.konghq.com/0.12.x/admin-api/#upstream-objects) which is materialized in JSON format.

### Example configuration
In the following, an example configuration is given with focus on `healthchecks`. Under `passive`, the rules for the circuit breaker are configured whereas *healty* describes instances which are running well and *unhealthy* observes if instances need to be ejected for recovery.
```json
{
    "name": "service.v1.py",
    "healthchecks": {
        "active": {
            ...
        },
        "passive": {
            "healthy": {
                "http_statuses": [200, 201, ...],
                "successes": 0
            },
            "unhealthy": {
                "tcp_failures": 10,
                "http_failures": 5,
                "timeouts": 5,
                "http_statuses": [500, 429, ...]
            }
        }
    },
    ...
}
```

#### tcp_failures
    Number of failures (TCP-based)
#### http_failures
    Number of failures (HTTP-based)
#### timeouts
    Number of failures (via timeout)
#### http_statuses
    List of HTTP statuses which will be observed and counted as http failures
#### successes (healthy only)
    Number of successes in proxied traffic (as defined by       
    http_statuses) to consider a instance healthy. 