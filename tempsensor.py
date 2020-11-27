import adafruit_dht
import time
import board
import mariadb
import sys

def getDBConn():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
            #user="root",
            #password="4M4!MukXKlYy",
            user="pi",
            password="i6B#Z*5Afvre",
            host="192.168.0.3",
            port=3307,
            database="hometelemetry"

        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    return conn


# --------- User Settings ---------
SENSOR_LOCATION_NAME = "Buhardilla"
# ---------------------------------

conn = getDBConn()
cursor = conn.cursor()

dhtSensor = adafruit_dht.DHT22(board.D2)

try:
    humidity = dhtSensor.humidity
    temp_c = dhtSensor.temperature

    if temp_c:
        #print(SENSOR_LOCATION_NAME + " Temperature(C) {}".format(temp_c))
        sql = "INSERT INTO hometelemetry.measurements VALUES (null, 0, now(), {})".format(temp_c)
        cursor.execute(sql)

    if humidity:
        #print(SENSOR_LOCATION_NAME + " Humidity(%) {}".format(humidity,".2f"))
        sql = "INSERT INTO hometelemetry.measurements VALUES (null, 1, now(), {})".format(humidity)
        cursor.execute(sql)

    conn.commit()

except Exception as e:
    print("RuntimeError: {}".format(e))


