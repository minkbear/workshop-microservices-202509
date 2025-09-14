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