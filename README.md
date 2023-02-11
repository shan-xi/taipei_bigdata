# taipei_bigdata

## requirement

```
1.以Docker搭建Airflow
2.在Airflow中建立一個daily執行的DAG
3.DAG是將以下網址中，地圖的專案點位(markers)爬下來
https://smartcity.taipei/projmap/0?lang=zh-Hant
將專案點位資料，存到任意RDB的一個table中
4.撰寫一個GO的API，其中有參數可以篩選專案"id"
並以json格式response上述資料
```

## Getting started 

1. initialize ariflow 

`docker-compose up airflow-init`

2. spin up all application

`docker-compose up`


3. run go api application

```
cd /api

go run .

Get marker by project_id API => http://{hostname}:8081/project/:project_id
please refer to https://smartcity.taipei/projmap/0?lang=zh-Hant for project_id information
```

