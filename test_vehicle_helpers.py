import unittest
import sqlite3

from database import vehicle_helpers as vh


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_connection = sqlite3.connect("bike_app.db")
        self.cursor = self.db_connection.cursor()

    def tearDown(self):
        self.cursor.close()
        self.db_connection.close()

    def test_set_vehicle_loc(self):
        # Assuming valid inputs
        vehicle_id = 1
        location = "kelvingrove"
        self.assertTrue(vh.set_vehicle_loc(vehicle_id, location))

    def test_get_vehicles_at_loc(self):
        # Assuming a valid location ID
        loc_id = 1
        vehicles = vh.get_vehicles_at_loc(loc_id)
        self.assertIsInstance(vehicles, list)

    def test_get_vehicles_by_status(self):
        # Assuming a valid status
        status = "parked"
        vehicles = vh.get_vehicles_by_status(status)
        self.assertIsInstance(vehicles, list)

        # Assuming an invalid status
        status = "invalid_status"
        vehicles = vh.get_vehicles_by_status(status)
        self.assertIsInstance(vehicles, list)

    def test_get_battery_level(self):
        # Assuming a valid vehicle ID
        vehicle_id = 1
        battery_level = vh.get_battery_level(vehicle_id)[0][0]
        self.assertIsInstance(battery_level, int)

    def test_get_status(self):
        # Assuming a valid vehicle ID
        vehicle_id = 1
        status = vh.get_status(vehicle_id)[0][0]
        self.assertIsInstance(status, str)

    def test_update_status(self):
        # Assuming valid inputs
        vehicle_id = 1
        state = "parked"
        vh.update_status(vehicle_id, state)

        # You can add assertions to check if the status has been updated in the database

    def test_update_battery_level(self):
        # Assuming valid inputs
        vehicle_id = 1
        battery = 50
        vh.update_battery_level(vehicle_id, battery)

        # You can add assertions to check if the battery level has been updated in the database

    def test_find_bike(self):
        # Assuming a valid location ID
        loc_id = 1
        bikes = vh.find_bike(loc_id)
        self.assertIsInstance(bikes, list)

    def test_filter_vehicles(self):
        # Assuming no search text
        search_text = ""
        search_field = "vehicle_id"
        status = ["parked", "in_transit"]
        vehicles = vh.filter_vehicles(search_text, search_field, status)
        self.assertIsInstance(vehicles, list)

        # You can write more test cases for different combinations of search_text, search_field, and status

    def test_filter_complaints(self):
        # Assuming no search text
        search_text = ""
        search_field = "complaint_id"
        status = ["open", "closed"]
        complaints = vh.filter_complaints(search_text, search_field, status)
        self.assertIsInstance(complaints, list)

        # You can write more test cases for different combinations of search_text, search_field, and status

    def test_get_complaint(self):
        # Assuming a valid complaint ID
        complaint_id = 1
        complaint = vh.get_complaint(complaint_id)
        self.assertIsInstance(complaint, list)

    def test_add_complaint(self):
        # Assuming valid inputs
        vehicle_id = 1
        subject = "Test Subject"
        description = "Test Description"
        ride_id = 2
        image = "test.jpg"
        vh.add_complaint(vehicle_id, subject, description, ride_id, image)

        # You can add assertions to check if the complaint has been added to the database


if __name__ == '__main__':
    unittest.main()
