import uniittest
from device_module import Device

class TestDevice(unittest.TestCase):

	def setUp(self):
		""" set up the method"""
		self.device = Device()

	def test_importdb(self):
		""" import the database file"""
		