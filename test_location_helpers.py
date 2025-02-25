import unittest
import sqlite3
from database import location_helpers as lh
from database import vehicle_helpers as vh


class LocationHelpersTestCase(unittest.TestCase):

    def setUp(self):
        self.db_connection = sqlite3.connect("bike_app.db")

    def tearDown(self):
        self.db_connection.close()

    def test_get_num_vehicles_at_loc(self):
        num_vehicles = lh.get_num_vehicles_at_loc(1)  # Assuming location ID 1 exists
        self.assertIsInstance(num_vehicles, int)
        self.assertGreaterEqual(num_vehicles, 0)

    def test_get_loc_capacity(self):
        loc_capacity = lh.get_loc_capacity(1)  # Assuming location ID 1 exists
        self.assertIsInstance(loc_capacity, int)
        self.assertGreaterEqual(loc_capacity, 0)

    def test_get_loc_id_by_name(self):
        loc_id = lh.get_loc_id_by_name("kelvingrove")  # Replace with an actual location name
        self.assertIsInstance(loc_id, int)
        self.assertGreaterEqual(loc_id, 0)


    def test_get_loc_name_by_id(self):
        # Assuming location_id is valid
        location_id = 1
        location_name = lh.get_loc_name_by_id(location_id)
        self.assertIsInstance(location_name, str)
        self.assertGreater(len(location_name), 0)

    def test_get_loc_name_by_id_invalid(self):
        # Assuming an invalid location_id
        location_id = 9999
        location_name = lh.get_loc_name_by_id(location_id)
        self.assertIsNone(location_name)

    def test_get_charging_locations(self):
        charging_locations = lh.get_charging_locations()
        self.assertIsInstance(charging_locations, list)
        self.assertGreaterEqual(len(charging_locations), 0)

    def test_set_vehicle_loc(self):
        # Assuming vehicle_id and location_id are valid
        vehicle_id = 1
        location = 'kelvingrove'
        result = vh.set_vehicle_loc(vehicle_id, location)
        self.assertTrue(result)

    def test_get_vehicles_at_loc(self):
        # Assuming location_id is valid
        location_id = 1
        vehicles_at_location = vh.get_vehicles_at_loc(location_id)
        self.assertIsInstance(vehicles_at_location, list)
        self.assertGreaterEqual(len(vehicles_at_location), 0)

if __name__ == '__main__':
    unittest.main()
