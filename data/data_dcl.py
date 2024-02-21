import sqlite3

conn = sqlite3.connect('data/sensor_data.db')
c = conn.cursor()

def insert_sensor_data(unix_timestamp, locals_data):
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()

    data_to_insert = {
        "time": unix_timestamp,
        "temperature": 'temperature_c',
        "humidity": 'humidity',
        "flux1": 'flow_rate',
        "flex": 'pressure',
        "air_quality": 'gas_value',
        "vibe1": 'vibration_count'
    }

    filtered_data = {k: locals_data.get(v) for k, v in data_to_insert.items() if v in locals_data}

    keys, values = zip(*filtered_data.items())

    query = f'INSERT INTO data ({", ".join(keys)}) VALUES ({", ".join(["?"] * len(keys))})'

    c.execute(query, values)

    conn.commit()
    conn.close()

def fetch_all_sensor_data():
    # 데이터베이스 연결 생성
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()

    # 모든 데이터를 검색하는 SQL 쿼리
    query = "SELECT * FROM data"

    # 쿼리 실행
    c.execute(query)

    # 검색된 모든 레코드 가져오기
    all_data = c.fetchall()

    # 데이터베이스 연결 종료
    conn.close()

    return all_data


import sqlite3

def create_sensor_data_table():
    # 데이터베이스 연결 생성
    conn = sqlite3.connect('sensor_data.db')
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS data (
            time INTEGER,
            temperature REAL,
            humidity REAL,
            flux1 REAL,
            flex REAL,
            air_quality REAL,
            tilt1 REAL,
            vibe1 REAL
        )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    all_sensor_data = fetch_all_sensor_data()
    for record in all_sensor_data:
        print(record)