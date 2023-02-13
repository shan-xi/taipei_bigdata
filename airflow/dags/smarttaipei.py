from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import xmltodict
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
    import traceback
    import logging
    conn = engine.connect()
    conn.execute(marker.delete())
    project_id_map = {
        '智慧交通':'56',
        '智慧健康':'47',
        '智慧建築':'33' ,
        '智慧教育':'24' ,
        '智慧經濟':'33',
        '智慧政府':'41' ,
        '智慧環境':'35' ,
        '智慧安防':'24' ,
        '其他' :'11'
    }
    for category_id in range(1, 10):
        response = requests.get(f'https://smartcity.taipei/xml.xml?category={category_id}')
        response.encoding = response.apparent_encoding
        data = xmltodict.parse(response.content, force_list=True)
        for marker_data in data['markers']:
            for point in marker_data['marker']:
                try:
                    pid=project_id_map.get(point['@type'].strip())
                    ins = marker.insert().values(
                        project_id=pid,
                        id=point['@id'].strip(),
                        name=point['@name'].strip(),
                        address=point['@address'].strip(),
                        lat=point['@lat'].strip(),
                        lng=point['@lng'].strip(),
                        locname=point['@locname'].strip(),
                        img=point['@img'].strip(),
                        intro=point['@intro'].strip(),
                        icon=point['@icon'].strip(),
                        type=point['@type'].strip(),
                    )
                    result = conn.execute(ins)
                except Exception as e:
                    traceback.print_exc()
                    logging.info(f'insert error:category_id={category_id}, id={point["@id"]}, type={point["@type"]}, error msg:{e}')


with DAG(dag_id="smarttaipei_dag",
         start_date=datetime(2023, 2, 9),
         schedule_interval="@daily",
         catchup=False) as dag:
    task1 = PythonOperator(
        task_id="smarttaipei",
        python_callable=get_smarttaipei_data)

    task1
