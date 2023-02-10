package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"

	_ "github.com/lib/pq"
)

type marker struct {
	Project_id string `json:"project_id"`
	ID         string `json:"id"`
	Name       string `json:"name"`
	Address    string `json:"address"`
	Lat        string `json:"lat"`
	Lng        string `json:"lng"`
	Locname    string `json:"locname"`
	Img        string `json:"img"`
	Intro      string `json:"intro"`
	Icon       string `json:"icon"`
	Type       string `json:"type"`
}

func (env Env) getMarkersByProjectID(c *gin.Context) {
	project_id := c.Param("project_id")
	log.Print(project_id)
	var name, address string
	q := "SELECT project_id, name, address FROM marker WHERE project_id=2"
	row := env.DB.QueryRow(q)
	err := row.Scan(&project_id, &name, &address)
	switch err {
	case sql.ErrNoRows:
		log.Printf("no rows are present for marker with project_id: %v", project_id)
		makeGinResponse(c, http.StatusBadRequest, err.Error())
	default:
		e := fmt.Sprintf("error: %v occurred while reading the databse for marker record with id: %v", err, project_id)
		log.Println(e)
		makeGinResponse(c, http.StatusInternalServerError, err.Error())
	}
}
