package main

import (
	"log"

	"github.com/gin-gonic/gin"
)

func main() {

	env := new(Env)
	var err error
	env.DB, err = ConnectDB()
	if err != nil {
		log.Fatalf("failed to start the server: %v", err)
	}

	router := gin.Default()
	router.GET("/project/:project_id", env.getMarkersByProjectID)

	router.Run("192.168.117.104:8081")
}
