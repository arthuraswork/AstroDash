import os

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from psycopg2 import connect

from database.norad_queries import (
    select_current_count, select_max_alt, select_min_alt,
    select_total_count, select_current_sputnics_lat_lon
)

st.title('Спутники Starlink вокруг Москвы')

load_dotenv()

DB_ERROR_MSG = 'Ошибка, скорее всего проблемы с бд'

conn = connect(os.environ['DBURI'])

def get_metric(sql_script):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
            value = cursor.fetchone()[0]
            return value
    except Exception:
        conn.rollback()
        st.warning(DB_ERROR_MSG)
        return 0

def to_map(sql_script):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
            value = cursor.fetchall()
            df = pd.DataFrame(value, columns = ['lat', 'lon'])
            return df
    except Exception:
        conn.rollback()
        st.warning(DB_ERROR_MSG)
        return 0



st.title('Колличество:')
cols = st.columns(2)
with cols[0]:
    total = get_metric(select_current_count)
    st.metric('Сейчас', value=total, border=True)
with cols[1]:
    st.metric('Всегда', value=get_metric(select_total_count), border=True)


st.title('Высотность:')
cols = st.columns(2)
with cols[0]:
    total = get_metric(select_max_alt)
    st.metric('Самый высокий', value=total, border=True)
with cols[1]:
    st.metric('Самый низкий', value=get_metric(select_min_alt), border=True)

st.map(to_map(select_current_sputnics_lat_lon))