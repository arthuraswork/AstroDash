from airflow import DAG
from airflow.decorators import task
from airflow.models import Variable
from httpx import Client
from utils.sqls import create_table_near_earth_objects, insert_one_near_earth_objects
from datetime import datetime, timedelta
import psycopg2


with DAG(
    dag_id='near_earth_objects',
    start_date=datetime(2026,1,1),
    schedule=timedelta(days=1)
) as dag:

    @task
    def init_table():
        conn = psycopg2.connect(Variable.get('dburi'))
        with conn.cursor() as cursor:
            cursor.execute(create_table_near_earth_objects)
            conn.commit()

    @task
    def api_request():
        apikey = Variable.get('nasa-apikey')
        dtime = datetime.now()
        url = 'https://api.nasa.gov/neo/rest/v1/feed'
        proxy = Variable.get('proxy')
        with Client(proxies={"http://": proxy, "https://": proxy}) as request:
            result = request.get(
                url=url,
                params={
                    'api_key': apikey,
                    'start_date':  (dtime - timedelta(days=7)).date().isoformat(),
                    'end_date':  dtime.now().isoformat()
                }
            )
            return result.json()

    @task
    def clean_and_upload(struct: dict):
        conn = psycopg2.connect(Variable.get('dburi'))
        with conn.cursor() as cursor:
            dates = struct['near_earth_objects']
            for date in dates:
                asteroids = struct['near_earth_objects'][date]
                for asteroid in asteroids:
                    absolute_magnitude = asteroid['absolute_magnitude_h']
                    dist = asteroid['close_approach_data'][0]['miss_distance']['kilometers']
                    relative_velocity = asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour']
                    diameter_max, diameter_min = asteroid['estimated_diameter']['meters'].values()
                    nasa_id = asteroid['id']
                    name = asteroid['name']
                    obj = [nasa_id, name, absolute_magnitude, dist, relative_velocity, diameter_min, diameter_max]
                    with conn.cursor() as cursor:
                        cursor.execute(insert_one_near_earth_objects, obj)
            conn.commit()
    init_table_task = init_table()
    api_request_struct = api_request()

    init_table_task >> api_request_struct.operator
    clean_and_upload(api_request_struct)
    

