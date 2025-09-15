# Auth service with [Go](https://go.dev/)

## 1. Run project with Go
```
$cd auth-service
$go mod tidy
$go run main.go
```

List of urls
* http://localhost:1323/
* http://localhost:1323/auth
* http://localhost:1323/metrics

## 2. Run project with Docker 
```
$docker image build -t auth-service .
```