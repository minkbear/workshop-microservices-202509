package main

import (
	"fmt"
	"net/http"
	"time"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	e := echo.New()

	// Middleware log for all requests
	e.Use(middleware.Logger())

	e.GET("/", func(c echo.Context) error {
		return c.String(http.StatusOK, "Hello, Auth service")
	})
	e.GET("/auth", showRequest)
	e.Logger.Fatal(e.Start(":1323"))
}

func showRequest(c echo.Context) error {
	body := echo.Map{}
	if err := c.Bind(&body); err != nil {
		return err
	}
	body["@timestamp"] = time.Now().Format(time.RFC3339)
	fmt.Printf("%v\n", body)
	return c.String(http.StatusOK, "OK")
}
