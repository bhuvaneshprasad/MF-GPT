import pandas as pd
import requests
import psycopg2
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

db_params = {
    'dbname': 'mutual_funds',
    'user': 'postgres',
    'password': 'Teddy678@pg',
    'host': 'localhost'
}

def create_table():
    conn = None
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Create table if not exists
        create_table_query = '''
        CREATE TABLE IF NOT EXISTS mutual_funds_nav (
            scheme_code INT,
            nav_date DATE,
            nav FLOAT,
            UNIQUE (scheme_code, nav_date, nav)
        );
        '''
        cur.execute(create_table_query)
        conn.commit()

        # Close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insert_data(scheme_code, nav_date, nav):
    conn = None
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Insert data
        insert_query = '''
        INSERT INTO mutual_funds_nav (scheme_code, nav_date, nav)
        VALUES (%s, %s, %s);
        '''
        cur.execute(insert_query, (scheme_code, nav_date, nav))
        conn.commit()

        # Close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def fetch_and_insert_data(scheme_code):
    url = f'https://api.mfapi.in/mf/{scheme_code}'
    response = requests.get(url)
    json_response = response.json()
    
    navs_data = json_response['data']
    for nav_data in navs_data:
        date = datetime.strptime(nav_data['date'], '%d-%m-%Y')
        nav = nav_data['nav']
        insert_data(scheme_code=int(scheme_code), nav_date=date, nav=nav)

def batch_insert_data(data):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    
    insert_query = """
    INSERT INTO mutual_funds_nav (scheme_code, nav_date, nav)
    VALUES (%s, %s, %s)
    ON CONFLICT (scheme_code, nav_date, nav) DO NOTHING;
    """
    
    cursor.executemany(insert_query, data)
    connection.commit()
    
    cursor.close()
    connection.close()

def fetch_and_prepare_data(scheme_code):
    url = f'https://api.mfapi.in/mf/{scheme_code}/latest'
    response = requests.get(url)
    json_response = response.json()
    
    navs_data = json_response['data']
    data = []
    for nav_data in navs_data:
        date = datetime.strptime(nav_data['date'], '%d-%m-%Y')
        nav = nav_data['nav']
        data.append((int(scheme_code), date, nav))
    
    return data

df = pd.read_csv("direct_scheme_codes.csv")

scheme_codes = df.scheme_code.values

total_schemes = len(scheme_codes)

create_table()

all_data = []
with ThreadPoolExecutor() as executor:
    futures = [executor.submit(fetch_and_prepare_data, scheme_code) for scheme_code in scheme_codes]
    
    for i, future in enumerate(as_completed(futures), 1):
        try:
            data = future.result()
            all_data.extend(data)
        except Exception as e:
            print(f"Error: {e}")
        print(f"{i+1} / {len(scheme_codes) + 1} --> {len(all_data)}")

print(len(all_data))
# Batch insert all collected data
batch_insert_data(all_data)