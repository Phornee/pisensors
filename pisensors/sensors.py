from influxdb_wrapper import influxdb_factory
from baseutils_phornee import ManagedClass
from baseutils_phornee import Logger
from baseutils_phornee import Config


class Sensors(ManagedClass):

    def __init__(self):
        super().__init__(execpath=__file__)

        self.logger = Logger({'modulename': self.getClassName(), 'logpath': 'log', 'logname': 'sensors'})
        self.config = Config({'modulename': self.getClassName(), 'execpath': __file__})

        self.conn = influxdb_factory()
        self.conn.openConn(self.config['influxdbconn'])

    @classmethod
    def getClassName(cls):
        return "sensors"

    def sensorRead(self):
        """
        Read sensors information
        """
        have_readings = False

        if self.is_raspberry_pi():
            try:
                import adafruit_dht  # noqa
                dhtSensor = adafruit_dht.DHT22(self.config['pin'])

                humidity = dhtSensor.humidity
                temp_c = dhtSensor.temperature

                have_readings = True
            except Exception as e:
                self.logger.error("Error reading sensor DHT22: {}".format(e))
        else:
            humidity = 50
            temp_c = 25
            have_readings = True

        if have_readings:
            try:
                points = [
                    {
                        "tags": {"sensorid": self.config['id']},
                        "fields": {"temp": float(temp_c), "humidity": float(humidity)}
                    }
                ]
                self.conn.insert('DHT22', points)

                self.logger.info("Temp: {} | Humid: {}".format(temp_c, humidity))

            except Exception as e:
                self.logger.error("RuntimeError: {}".format(e))
                self.logger.error("influxDB conn={}".format(self.config['influxdbconn']))


if __name__ == "__main__":
    sensors_instance = Sensors()
    sensors_instance.sensorRead()
