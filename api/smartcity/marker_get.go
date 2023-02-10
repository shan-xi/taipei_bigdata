package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"

	_ "github.com/lib/pq"
)

func (env Env) getMarkersByProjectID(c *gin.Context) {
	project_id := c.Param("project_id")
	var id, name, address, lat, lng, locname, img, intro, icon, ty string
	q := `SELECT project_id, id, name, address, lat, lng, locname, img, intro, icon, type as ty FROM marker WHERE project_id=$1;`
	rows, err := env.DB.Query(q, project_id)
	if err != nil {
		e := fmt.Sprintf("error: %v occurred while reading the databse for marker record with project_id: %v", err, project_id)
		log.Println(e)
		makeGinResponse(c, http.StatusInternalServerError, err.Error())
	}
	defer rows.Close()

	markers := make([]Marker, 0)
	for rows.Next() {
		err := rows.Scan(&project_id, &id, &name, &address, &lat, &lng, &locname, &img, &intro, &icon, &ty)
		if err != nil {
			e := fmt.Sprintf("error: %v occurred while retrieving data for marker record with project_id: %v", err, project_id)
			log.Println(e)
			makeGinResponse(c, http.StatusInternalServerError, err.Error())
		}
		markers = append(markers, Marker{project_id, id, name, address, lat, lng, locname, img, intro, icon, ty})
	}
	err = rows.Err()
	if err != nil {
		log.Fatal(err)
	}
	c.JSON(http.StatusOK, markers)
}
