from airflow import DAG
from airflow.models import Variable
from airflow.decorators import task
from datetime import datetime, timedelta
from utils.sqls import create_table_starlink_moscow, insert_starlink_moscow
from psycopg2 import connect
from httpx import Client

with DAG(
    dag_id='starlink_moscow',
    start_date=datetime(2026,1,1),
    schedule=timedelta(days=1)
) as dag:
    
    @task
    def init_db():
        conn = connect(Variable.get('dburi'))
        with conn.cursor() as cursor:
            cursor.execute(create_table_starlink_moscow)
        conn.commit()

    @task
    def collect_sputnics():
        apikey = Variable.get('norad-apikey')
        proxy  = Variable.get('proxy')
        url    = 'https://api.n2yo.com/rest/v1/satellite/above/55.7558/37.6173/0/90/52'
        with Client(proxies={"http://": proxy, "https://": proxy}) as request:
            response = request.get(
                url=url,
                params={
                    'apiKey': apikey,
            }
            ).json()
        return response['above']

    @task
    def insert_sputnics(sputnics):
        conn = connect(Variable.get('dburi'))
        with conn.cursor() as cursor:
            for sat in sputnics:
                cursor.execute(insert_starlink_moscow, tuple(sat.values()))
        conn.commit()
    init_db_task = init_db()
    sputnics = collect_sputnics()
    init_db_task >> sputnics.operator
    insert_sputnics(sputnics)