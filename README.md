# Workshop :: Microservices develop, test and deploy


## 1. API Gateway with [Kong](https://github.com/Kong/kong)

Kong with Database mode
```
$git clone https://github.com/Kong/docker-kong
$cd docker-kong/compose/
$KONG_DATABASE=postgres docker compose --profile database up -d
```
Status of Kong server and database
```
$docker compose ps
NAME             IMAGE          COMMAND                  SERVICE   CREATED          STATUS                    PORTS
compose-db-1     postgres:9.5   "docker-entrypoint.s…"   db        49 seconds ago   Up 49 seconds (healthy)   5432/tcp
compose-kong-1   kong:latest    "/docker-entrypoint.…"   kong      49 seconds ago   Up 44 seconds (healthy)   0.0.0.0:8000-8002->8000-8002/tcp, [::]:8001-8002->8001-8002/tcp, 0.0.0.0:8443-8444->8443-8444/tcp, [::]:8444->8444/tcp
```

### Gateway API's urls :
* http://localhost:8000 - send traffic to your service via Kong
* http://localhost:8001 - configure Kong using Admin API or via [decK](https://github.com/kong/deck)
* http://localhost:8002 - access Kong's management [Web UI (Kong Manager)](https://github.com/Kong/kong-manager)

## 2. Build custom plugin with Kong
```
$cd kong-plugins
$docker image build -t mykong .
```

Start Kong server with `image=mykong`
```
$docker compose --profile database down
$docker volume prune

$export KONG_DOCKER_TAG=mykong
$KONG_DATABASE=postgres docker compose --profile database up -d
$docker compose ps
```

List of plugins in Kong manager
* http://localhost:8002/plugins/select

## 3. Working with Kong API Gateway
* Add service
* Add plugin `demo-auth` to service
  * http/https
  * URl=http://auth-service:1323/auth
* Add route to service


Add service
```
$curl http://127.0.0.1:8001/services \
    -d name=demo-api \
    -d url=https://jsonplaceholder.typicode.com

```
Add route to service
```
$curl http://127.0.0.1:8001/services/demo-api/routes \
    -d name=demo-api \
	-d 'paths[]=/test'
```

Check
* https://jsonplaceholder.typicode.com/users/1
* http://localhost:8000/test/users/1

## 4. Start auth-service
```
$docker compose build auth-service
$docker compose up -d auth-service
```

List of urls
* http://localhost:1323/
* http://localhost:1323/auth

Check from API Gateway
* http://localhost:8000/test/users/1

## 5. Add observability for services
* List of services
  * API gateway with Kong
  * Auth service

Add plugins in Kong with Global scope
* http://localhost:8002/plugins
  * New plugin
    * Metric with [prometheus](https://developer.konghq.com/plugins/prometheus)
      * http://localhost:8001/metrics
    * Trace and Log with [opentelemetry](https://developer.konghq.com/plugins/opentelemetry)
      * traces_endpoint: http://localhost:4318/v1/traces
      * logs_endpoint: http://localhost:4318/v1/logs

## 6. Start [LGTM Stack](https://github.com/grafana/docker-otel-lgtm)
* Log
* Grafana
* Trace
* Metric

```
$docker compose up -d lgtm
$docker compose up ps
```

Edit traces_endpoint
* http://lgtm:4318/v1/traces

Check data in Grafana dashboard
* http://localhost:3000

## 7. Tracing with Python service
* [FastAPI](https://fastapi.tiangolo.com/)
* [OpenTelemetry](https://opentelemetry.io/)

### 7.1 Build and run
```
$docker compose build python-service
$docker compose up -d python-service
```

List of urls
* http://localhost:9001
* http://localhost:9001/health

### 7.2 Add pythin-service to API gateway
* Add service
* Add route to service

Add service
```
$curl http://127.0.0.1:8001/services \
    -d name=python-service \
    -d url=http://python-service:8000

```

Add route to service
```
$curl http://127.0.0.1:8001/services/python-service/routes \
    -d name=python-service \
	-d 'paths[]=/python'
```

Check from API Gateway
* http://localhost:8000/python/
* http://localhost:8000/python/health

    