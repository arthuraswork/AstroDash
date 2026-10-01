import streamlit as st
import pandas as pd
from dotenv import load_dotenv
import os
from psycopg2 import connect
from database.near_objs_queries import (
select_all_near_earth_objects, select_count_near_earth_objects,
select_dist_near_earth_objects, select_speed_near_earth_objects,

top_big_earth_objects, top_fast_earth_objects,
top_near_earth_objects
)
load_dotenv()

def count():
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_count_near_earth_objects)
            return cursor.fetchone()[0]
    except Exception:
        st.warning('Ошибка, скорее всего проблемы с бд')
    return 0

def avg_dist():
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_dist_near_earth_objects)
            return round(cursor.fetchone()[0])
    except Exception:
        st.warning('Ошибка, скорее всего проблемы с бд')
    return 0

def avg_speed():
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_speed_near_earth_objects)
            return round(cursor.fetchone()[0])
    except Exception:
        st.warning('Ошибка, скорее всего проблемы с бд')
    return 0

def all_objs():
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_all_near_earth_objects)
            return pd.DataFrame(cursor.fetchall(), columns=[
                'nasa_id',
                'name',
                'absolute_magnitude',
                'miss_distance_km',
                'relative_velocity_kmh',
                'diameter_min_m',
                'diameter_max_m'
            ])
    except Exception as e:
        st.warning('Ошибка, скорее всего проблемы с бд')
        st.write(e)
def top_near():
    try:
        with conn.cursor() as cursor:
            cursor.execute(top_near_earth_objects)
            return pd.DataFrame(cursor.fetchall(), columns=['Имя', 'Дистанция'])
    except Exception:
        st.warning('Ошибка, скорее всего проблемы с бд')
    return 0

def top_fast():
    try:
        with conn.cursor() as cursor:
            cursor.execute(top_fast_earth_objects)
            return pd.DataFrame(cursor.fetchall(), columns=['Имя', 'Скорость'])
    except Exception:
        st.warning('Ошибка, скорее всего проблемы с бд')
    return 0

def top_big():
    try:
        with conn.cursor() as cursor:
            cursor.execute(top_big_earth_objects)
            return pd.DataFrame(cursor.fetchall(), columns=['Имя', 'Размер'])
    except Exception:
        st.warning('Ошибка, скорее всего проблемы с бд')
    return 0


conn = connect(os.environ['DBURI'])
st.title('Ближайшие к земле объекты')

columns = st.columns(3)

with columns[0]:
    total = count()
    st.metric('Общее колличество', value=total, border=True)
with columns[1]:
    st.metric('Средняя скорость', value=avg_speed(), border=True)
with columns[2]:
    st.metric('Среднee расстояние от земли', value=avg_dist(), border=True)

topk = st.slider('Показывать', min_value=0, max_value=total, value=5)

st.write('Топ ближайших')
top_near_df = top_near().sort_values('Дистанция', ascending=False).iloc[:topk]
st.bar_chart(data=top_near_df, x=top_near_df.columns[0], y=top_near_df.columns[1], horizontal=True, sort=False)

st.write('Топ быстрых')
top_fast_df = top_fast().sort_values('Скорость', ascending=False).iloc[:topk]
st.bar_chart(data=top_fast_df, x=top_fast_df.columns[0], y=top_fast_df.columns[1], horizontal=True, sort=False)

st.write('Топ больших')
top_size_df = top_big().sort_values('Размер', ascending=False).iloc[:topk]
st.bar_chart(data=top_size_df, x=top_size_df.columns[0], y=top_size_df.columns[1], horizontal=True, sort=False)

st.header('Все объекты')

st.write(all_objs())