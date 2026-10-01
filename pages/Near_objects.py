import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from psycopg2 import connect

from database.near_objs_queries import (
    select_all_near_earth_objects,
    select_count_near_earth_objects,
    select_dist_near_earth_objects,
    select_speed_near_earth_objects,
    top_big_earth_objects,
    top_fast_earth_objects,
    top_near_earth_objects,
)

load_dotenv()

DB_ERROR_MSG = 'Ошибка, скорее всего проблемы с бд'

conn = connect(os.environ['DBURI'])


def scalar(sql_script, round_result=False):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
            value = cursor.fetchone()[0]
            return round(value) if round_result else value
    except Exception:
        conn.rollback()
        st.warning(DB_ERROR_MSG)
        return 0


def all_objs():
    columns = [
        'nasa_id',
        'name',
        'absolute_magnitude',
        'miss_distance_km',
        'relative_velocity_kmh',
        'diameter_min_m',
        'diameter_max_m',
    ]
    try:
        with conn.cursor() as cursor:
            cursor.execute(select_all_near_earth_objects)
            return pd.DataFrame(cursor.fetchall(), columns=columns)
    except Exception as e:
        conn.rollback()
        st.warning(DB_ERROR_MSG)
        st.write(e)
        return pd.DataFrame(columns=columns)


def topk(sql_script, columns, x_column, y_column):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
            df = pd.DataFrame(cursor.fetchall(), columns=columns)
    except Exception:
        conn.rollback()
        st.warning(DB_ERROR_MSG)
        df = pd.DataFrame(columns=columns)
    return df, x_column, y_column


def draw_top(title, sql_script, columns, x_column, y_column, k):
    st.write(title)
    df, x, y = topk(sql_script, columns, x_column, y_column)
    df = df.sort_values(y, ascending=False).iloc[:k]
    st.bar_chart(data=df, x=x, y=y, horizontal=True, sort=False)


st.title('Ближайшие к земле объекты')

cols = st.columns(3)

with cols[0]:
    total = scalar(select_count_near_earth_objects)
    st.metric('Общее колличество', value=total, border=True)
with cols[1]:
    st.metric('Средняя скорость', value=scalar(select_speed_near_earth_objects, round_result=True), border=True)
with cols[2]:
    st.metric('Среднee расстояние от земли', value=scalar(select_dist_near_earth_objects, round_result=True), border=True)

k = st.slider('Показывать', min_value=0, max_value=max(total, 1), value=min(5, max(total, 1)))

draw_top('Топ ближайших', top_near_earth_objects, ['Имя', 'Дистанция'], 'Имя', 'Дистанция', k)
draw_top('Топ быстрых', top_fast_earth_objects, ['Имя', 'Скорость'], 'Имя', 'Скорость', k)
draw_top('Топ больших', top_big_earth_objects, ['Имя', 'Размер'], 'Имя', 'Размер', k)

st.header('Все объекты')
st.write(all_objs())