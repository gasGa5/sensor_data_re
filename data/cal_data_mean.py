import sqlite3

database_path = 'sensor_data.db'

# 데이터베이스에 연결
conn = sqlite3.connect(database_path)

cursor = conn.cursor()

query = """
SELECT
    strftime('%s', time) AS time,
    temperature,
    humidity,
    flux1,
    flex,
    air_quality,
    tilt1,
    vibe1
FROM
    sensor_data;
"""

try:
    cursor.execute(query)

    rows = cursor.fetchall()

    for row in rows:
        print(row)

except Exception as e:
    print("An error occurred:", e)

finally:
    conn.close()
