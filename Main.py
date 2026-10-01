import streamlit as st

st.title('Дашборды по данным NASA')

with st.container(border=True):
    st.write('**Дашборд по ближайшим объектам к Земле**')
    st.write('Раз в день запрос к `https://api.nasa.gov/neo/rest/v1/feed`')
    st.page_link('./pages/Near_objects.py', label='**Перейти**', width='stretch')

with st.container(border=True):
    st.write('**Дашборд по пролетающим спутникам вокруг Москвы**')
    st.write('Раз в день запрос к `https://api.n2yo.com/rest/v1/satellite/above/55.7558/37.6173/0/90/52`')
    st.page_link('./pages/Starlink_sputnics.py', label='**Перейти**', width='stretch')

with st.container(border=True):
    st.write('**Технологии**')
    st.table([['Оркестратор', 'БД', 'Реквесты'],['Airflow','Postgres','httpx']])
