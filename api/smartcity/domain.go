package main

type Marker struct {
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
