""" Unit tests """
import unittest
import os
import sys
import inspect
import logging
from pathlib import Path

from pisensors import Sensors

THIS_FOLDER = os.path.dirname(inspect.getfile(inspect.currentframe()))

log = logging.getLogger("pisensors_tests")
sh = logging.StreamHandler(sys.stdout)
log.addHandler(sh)
log.setLevel(logging.INFO)


class Testing(unittest.TestCase):
    """Testing class
    """
    def setUp(self):
        # Fake the db to use the one for the tests
        template_config_path = f'{Path(__file__).parent}/data/config-template.yml'
        self.sensors_instance = Sensors(template_config_path=template_config_path)

    def test_000_sensors_reading(self):
        """Test for sensors reading, using fake sensors
        """
        self.sensors_instance.sensor_read()

if __name__ == "__main__":
    unittest.main()
