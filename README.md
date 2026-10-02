
# ДАШБОРДЫ ПО ДАННЫМ NASA И STARLINK

Проект представляет собой набор интерактивных дашбордов на Streamlit,
которые визуализируют данные, собранные через Apache Airflow из открытых
API NASA и N2YO. Данные хранятся в PostgreSQL.


### СОДЕРЖАНИЕ

- Возможности
- Архитектура
- Технологии
- Структура проекта
- Установка и запуск
- Настройка окружения
- DAG'и Airflow
- Дашборды


### ВОЗМОЖНОСТИ

Дашборд **Ближайшие к Земле объекты**
- Общее количество объектов, сближающихся с Землёй
- Средняя скорость и среднее расстояние до Земли
- Топ-N объектов по:
  - близости к Земле
  - скорости
  - размеру
- Таблица со всеми объектами

Дашборд **Спутники Starlink вокруг Москвы**
- Текущее и общее количество спутников
- Максимальная и минимальная высота орбиты
- Карта с текущим положением спутников


АРХИТЕКТУРА
-----------

NASA API ---+
            +--> Airflow DAG --> PostgreSQL --> Streamlit Dashboard
N2YO API ---+

Airflow по расписанию (раз в день) забирает данные из внешних API,
очищает их и складывает в PostgreSQL. Streamlit-приложение читает
данные из БД и отображает их в виде метрик, графиков и карт.


ТЕХНОЛОГИИ
----------

Компонент        | Технология
-----------------+-------------------------
Оркестратор      | Apache Airflow
База данных      | PostgreSQL
HTTP-клиент      | httpx
Дашборды         | Streamlit
Работа с данными | pandas, psycopg2
Конфигурация     | python-dotenv, Airflow Variables


УСТАНОВКА И ЗАПУСК
------------------

1. Клонирование репозитория

   git clone <repo-url>
   cd <repo-dir>

2. Установка зависимостей

   pip install -r requirements.txt

   Пример requirements.txt:

   streamlit
   pandas
   psycopg2-binary
   httpx
   apache-airflow
   python-dotenv

3. Запуск Streamlit-приложения

   streamlit run Main.py

4. Запуск Airflow

   airflow db init
   airflow standalone

   После запуска перейдите в веб-интерфейс Airflow
   (http://localhost:8080) и включите DAG'и near_earth_objects
   и starlink_moscow.


НАСТРОЙКА ОКРУЖЕНИЯ
-------------------

Переменные окружения (.env):

   DBURI=postgresql://user:password@host:port/dbname

Airflow Variables (устанавливаются через UI Airflow:
Admin -> Variables, или через CLI):

   Variable       | Описание
   ---------------+-----------------------------------------------
   dburi          | Строка подключения к PostgreSQL
   nasa-apikey    | API-ключ NASA (https://api.nasa.gov)
   norad-apikey   | API-ключ N2YO (https://www.n2yo.com/api/)
   proxy          | HTTP/HTTPS-прокси (если требуется)


### DAG'И AIRFLOW


near_earth_objects
~~~~~~~~~~~~~~~~~~

Загружает данные об объектах, сближающихся с Землёй, за последние 7 дней.

Задачи:
   1. init_table       - создаёт таблицу в БД
   2. api_request      - запрос к https://api.nasa.gov/neo/rest/v1/feed
   3. clean_and_upload - очистка и вставка данных

starlink_moscow
~~~~~~~~~~~~~~~

Загружает данные о спутниках Starlink в зоне видимости над Москвой.

Задачи:
   1. init_db          - создаёт таблицу в БД
   2. collect_sputnics - запрос к
                         https://api.n2yo.com/rest/v1/satellite/above/...
   3. insert_sputnics  - вставка данных в БД

Расписание: раз в день (timedelta(days=1)).


### ДАШБОРДЫ

Главная страница (Main.py)
-> Содержит ссылки на дашборды и информацию о технологиях.

Near Objects (pages/Near_objects.py)

- Метрики: количество, средняя скорость, среднее расстояние
- Слайдер для выбора топ-N
- Горизонтальные bar-chart'ы: топ ближайших, топ быстрых, топ больших
- Таблица всех объектов

Starlink (pages/Starlink_sputnics.py)

- Метрики: текущее/общее количество спутников, макс./мин. высота
- Карта с текущим положением спутников

url: https://nasa-dashboard.cloudpub.ru/
