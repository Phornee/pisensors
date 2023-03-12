from influxdb_wrapper import influxdb_factory
from baseutils_phornee import Logger, Logger_Mode, Config, is_raspberry_pi
from pathlib import Path

class Sensors():

    def __init__(self):
        self.logger = Logger(package_name= self.getClassName(), 
                            log_file_name='log', 
                            mode=Logger_Mode.NONE)

        self.config = Config(package_name=self.getClassName(), 
                             template_path='{}/config-template.yml'.format(Path(__file__).parent),
                             config_file_name='config.yml')

        influx_conn_type = self.config['influxdbconn'].get('type', 'influx')
        self.conn = influxdb_factory(influx_conn_type)
        self.conn.openConn(self.config['influxdbconn'])


    @classmethod
    def getClassName(cls):
        return "sensors"

    def sensorRead(self):
        """
        Read sensors information
        """
        have_readings = False

        if is_raspberry_pi():
            try:
                import adafruit_dht
                dhtSensor = adafruit_dht.DHT22(self.config['pin'])

                humidity = dhtSensor.humidity
                temp_c = dhtSensor.temperature

                have_readings = True
            except Exception as e:
                self.logger.error("Error reading sensor DHT22: {}".format(e))
        else:
                humidity = 51
                temp_c = 25
                have_readings = True

        if have_readings:
            try:
                points = [
                    {
                        "tags": {
                            "sensorid": self.config['id']
                        },
                        "fields": {
                            "temp": float(temp_c),
                            "humidity": float(humidity)
                        }
                    }
                ]
                self.conn.insert('DHT22', points)

                self.logger.info("Temp: {}°C | Humid: {}%".format(temp_c, humidity))

            except Exception as e:
                self.logger.error("RuntimeError: {}".format(e))
                self.logger.error("influxDBURL={} | influxDBToken={}".format(self.config['influxdbconn']['url'],
                                                                             self.config['influxdbconn']['token']))

if __name__ == "__main__":
    sensors_instance = Sensors()
    sensors_instance.sensorRead()





