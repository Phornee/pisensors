import adafruit_dht
import time
import board
import mariadb
import sys


# --------- User Settings ---------
SENSOR_LOCATION_NAME = "Buhardilla"
# ---------------------------------

def getDBConn():
    """"""
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(
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

def sensorRead(conn, pin):
    """"""
    dhtSensor = adafruit_dht.DHT22(pin)

    try:
        humidity = dhtSensor.humidity
        temp_c = dhtSensor.temperature

        if temp_c:
            # print(SENSOR_LOCATION_NAME + " Temperature(C) {}".format(temp_c))
            sql = "INSERT INTO hometelemetry.measurements VALUES (null, 0, UTC_TIMESTAMP(), {})".format(temp_c)
            cursor.execute(sql)

        if humidity:
            # print(SENSOR_LOCATION_NAME + " Humidity(%) {}".format(humidity,".2f"))
            sql = "INSERT INTO hometelemetry.measurements VALUES (null, 1, UTC_TIMESTAMP(), {})".format(humidity)
            cursor.execute(sql)

        conn.commit()

    except Exception as e:
        print("RuntimeError: {}".format(e))


conn = getDBConn()
cursor = conn.cursor()

sensorRead(conn, board.D2)





