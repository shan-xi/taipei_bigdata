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

1. airflow setup 

```
cd /airflow

#initialize ariflow 

docker-compose up airflow-init

#spin up all application

docker-compose up
```

2. run go api application

```
cd /api/smartcity

go run .

#use ngrok to expose the localhost port to the internet

ngrok http 8081

example: 
Get marker by project_id API => hhttps://8d2a-2001-b400-e403-9be-90e9-378e-37b6-ed12.jp.ngrok.io/project/:project_id
please refer to https://smartcity.taipei/projmap/0?lang=zh-Hant for project_id information
```

