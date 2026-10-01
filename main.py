import streamlit as st

st.title('Дашборды по данным NASA')

with st.container(border=True):
    st.write('**Дашборд по ближайшим объектам к Земле**')
    st.write('Раз в день запрос к `https://api.nasa.gov/neo/rest/v1/feed` c Airflow, Postgre и httpx')
    st.page_link('')