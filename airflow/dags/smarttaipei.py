from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import xmltodict
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import Integer
from sqlalchemy import String

conn_url = 'postgresql+psycopg2://airflow:airflow@postgres:5432/airflow'
engine = create_engine(conn_url)
metadata_obj = MetaData()
marker = Table(
    "marker",
    metadata_obj,
    Column("project_id", Integer),
    Column("id", Integer),
    Column("name", String(100)),
    Column("address", String(200)),
    Column("lat", String(20)),
    Column("lng", String(20)),
    Column("locname", String(20)),
    Column("img", String(500)),
    Column("intro", String(4000)),
    Column("icon", String(500)),
    Column("type", String(20)),
)
metadata_obj.create_all(engine)


def get_smarttaipei_data():
    conn = engine.connect()
    for project_id in range(1, 10):
        response = requests.get(f'https://smartcity.taipei/xml.xml?category={project_id}')
        response.encoding = response.apparent_encoding
        data = xmltodict.parse(response.content, force_list=True)
        for marker_data in data['markers']:
            for point in marker_data['marker']:
                try:
                    ins = marker.insert().values(
                        project_id=project_id,
                        id=point['@id'],
                        name=point['@name'],
                        address=point['@address'],
                        lat=point['@lat'],
                        lng=point['@lng'],
                        locname=point['@locname'],
                        img=point['@img'],
                        intro=point['@intro'],
                        icon=point['@icon'],
                        type=point['@type'],
                    )
                    result = conn.execute(ins)
                except Exception as e:
                    print(f'insert error:project_id={project_id}, id={point["@id"]}, name={point["@name"]}, error msg:{e}')


with DAG(dag_id="smarttaipei_dag",
         start_date=datetime(2023, 2, 8),
         schedule_interval="@daily",
         catchup=False) as dag:
    task1 = PythonOperator(
        task_id="smarttaipei",
        python_callable=get_smarttaipei_data)

task1
