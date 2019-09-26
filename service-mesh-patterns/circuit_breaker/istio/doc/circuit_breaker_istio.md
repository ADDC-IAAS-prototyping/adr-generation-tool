# Circuit Breaking - Istio
Documentation of relevant properties for circuit breaking with Istio.
In the following, we will focus on the general configuration for connection pools inside a destination rule without consideration of subsets.

## Destination Rules
In Istio, Destination Rules define policies that apply to traffic intended for a service routing has occured. The rules specify configuration for:
* Loadbalancing
* The size of a connection pool from the sidecar
* Outlier detection settings for health checks within the load balancing pool
* TLS/SSL related settings for upstream connections
* Traffic policies that apply to specific ports of the service  

within the `spec` property. 

It is **required** to pass a `host` (name of a service from the service registry) to which these rules will be applied to.

For Circuit Breaking / Health Checks, we focus on the configuration of **ConnectionPools** and **OutlierDetection**.

## ConnectionPoolSettings
Settings for an connection pool for an upstream host. A host is a single instance of a service. Connection pool settings can be applied at TCP and HTTP level:

### TCPSettings
#### maxConnections
    Maximum number of HTTP1/TCP connections to a destination host (defaults to 1024).
#### connectionTimeout
    Timeout limit for connection
#### tcpKeepAlive
    Settings for TcpKeepAlive configurations (optional).

### HTTPSettings
#### http1MaxPendingRequests
    Max. number of pending HTTP requests to a destination (defaults to 1024).
#### http2MaxRequests
    Max. number of requests to a backend (defaults to 1024).
#### maxRequestsPerConnection
    Max. number of requests per connection to a backend (set to 1 to disable keepAlive).
#### maxRetries
    Max. number of retries that can be outstanding to all hosts in a cluster at a given time (defaults to 1024).
#### idleTimeout
    Period in which connection pool idles (no active requests available) after which the connection will be closed. (optional)


## OutlierDetection
This is the actual implementation of the circuit breaker feature. Tracks the status of each individual host in the upstream service, for both TCP and HTTP services.
* HTTP Services: Tracking if the services return 5xx errors for API calls
* TCP Services: Tracking for connection timeouts or connection failures to given host

#### consecutiveErrors
    Number of errors before host is ejected from connection pool (defaults to 5).
#### interval
    Time in which the consecutive errors are counted. Format: 1h/m/s/ms. (inteval >= 1ms)
#### baseEjectionTime
    Timeout duration for an ejected host. Serves as base factor for the actual timeout of the host which is calculated as follows: <#times_host_is_ejected> * baseEjectionTime = ejectionTime(host)
#### maxEjectionPercent
    Max. percentage of hosts in connection pool that can be ejected at a time
#### minHealthPercent
    If percentage of healthy hosts in connection pool drops below minHealtPercent value, outlier detection will be disabled (defaults to 50%).