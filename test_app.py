import unittest
from flask import Flask
import json
import app  # Replace with the actual name of your Python file


class YourAppTestCase(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    # Uncomment if running 1st time
    '''
    def test_signup(self):
        data = {
            "username": "testuser1",
            "password": "testpassword1"
        }
        response = self.app.post('/signup', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Registration Successful")
    '''

    def test_login(self):
        data = {
            "username": "testuser1",
            "password": "testpassword1"
        }
        response = self.app.post('/login', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Login Successful")

    def test_login_with_wrong_password(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.app.post('/login', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["message"], "Login Failed")

    def test_find_bike(self):
        data = {
            "location": "Kelvingrove"
        }
        response = self.app.post('/find_bike', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("bike_id" in data)
        self.assertTrue("bike_type" in data)
        self.assertTrue("battery_level" in data)
        self.assertTrue("time_limit" in data)

    def test_book_ride(self):
        data = {
            "username": "testuser",
            "vehicle_id": "test_vehicle",
            "values": [0, 0, 10]  # Adjust the values as needed
        }
        response = self.app.post('/book', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Ride started successfully")

    def test_card_registration(self):
        data = {
            "username": "testuser",
            "card_details": "1234 5678 9012 3456",
            "cvv": "123"
        }
        response = self.app.post('/card_reg', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Card Registration Successful")

    def test_top_up_wallet(self):
        data = {
            "username": "testuser",
            "amount": 50,
            "type": "wallet",
            "cvv": "123"
        }
        response = self.app.post('/top_up', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Payment Successful")

    def test_top_up_deposit(self):
        data = {
            "username": "testuser",
            "amount": 100,
            "type": "deposit",
            "cvv": "123"
        }
        response = self.app.post('/top_up', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Payment Successful")

    def test_submit_feedback(self):
        data = {
            "username": "testuser",
            "feedback": "This is a test feedback",
            "sec_bal": 75  # Adjust the security deposit balance as needed
        }
        response = self.app.post('/submit_feedback', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Feedback Successful")

    def test_search_operator_vehicles(self):
        data = {
            "search_text": "",
            "search_field": "vehicle_id",  # Adjust search_field as needed
            "status_filter": ["parked", "in_transit", "low_battery", "defect_reported"]
            # Adjust status_filter as needed
        }
        response = self.app.post('/search_operator_vehicles', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("bike_id" in data)
        self.assertTrue("location_name" in data)
        self.assertTrue("battery_level" in data)
        self.assertTrue("time_limit" in data)

    def test_submit_report(self):
        data = {
            "loc": "kelvingrove",
            "username": "testuser",
            "report": "This is a test report",
            "subject": "Test Subject"
        }
        response = self.app.post('/submit_report', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Report Submission Successful")

    def test_get_complaint(self):
        data = {
            "complaint_id": "wrong_complaint_id"
        }
        response = self.app.post('/get_complaint', json=data)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    # def test_charge_vehicle(self):
    #     data = {
    #         "status": "parked",  # Adjust status as needed
    #         "vehicle_id": "test_vehicle"
    #     }
    #     response = self.app.post('/charge', json=data)
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["message"], "Vehicle set to charge")


if __name__ == '__main__':
    unittest.main()
