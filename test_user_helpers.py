import unittest
import sqlite3
from database import user_helpers as uh

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_connection = sqlite3.connect("bike_app.db")
        self.cursor = self.db_connection.cursor()

    def tearDown(self):
        self.cursor.close()
        self.db_connection.close()


    def test_get_users(self):
        # Assuming a valid username
        username = "testuser"
        users = uh.get_users(username)
        self.assertIsInstance(users, list)

    def test_get_password(self):
        # Assuming a valid username
        username = "testuser"
        password = uh.get_password(username)[0][0]
        self.assertIsInstance(password, str)

    def test_debit_wallet_amount(self):
        # Assuming valid inputs
        username = "testuser"
        amount = 50
        uh.debit_wallet_amount(username, amount)

        # You can add assertions to check if the wallet amount has been updated in the database

    def test_credit_wallet_amount(self):
        # Assuming valid inputs
        username = "testuser"
        amount = 50
        uh.credit_wallet_amount(username, amount)

        # You can add assertions to check if the wallet amount has been updated in the database

    def test_debit_deposit_amount(self):
        # Assuming valid inputs
        username = "testuser"
        amount = 50
        uh.debit_deposit_amount(username, amount)

        # You can add assertions to check if the deposit amount has been updated in the database

    def test_credit_deposit_amount(self):
        # Assuming valid inputs
        username = "testuser"
        amount = 50
        uh.credit_deposit_amount(username, amount)

        # You can add assertions to check if the deposit amount has been updated in the database

    def test_get_wallet_balance(self):
        # Assuming a valid username
        username = "testuser"
        wallet_balance = uh.get_wallet_balance(username)[0][0]
        self.assertIsInstance(wallet_balance, float)

    def test_get_deposit_balance(self):
        # Assuming a valid username
        username = "testuser"
        deposit_balance = uh.get_deposit_balance(username)[0][0]
        self.assertIsInstance(deposit_balance, int)

    def test_add_card_details(self):
        # Assuming valid inputs
        username = "testuser"
        card_details = "test_card"
        cvv = "test_cvv"
        uh.add_card_details(username, card_details, cvv)

        # You can add assertions to check if the card details have been updated in the database

    def test_get_users_details(self):
        # Assuming a valid username
        username = "testuser"
        user_details = uh.get_users_details(username)
        self.assertIsInstance(user_details, list)

    def test_get_cvv(self):
        # Assuming a valid username
        username = "testuser"
        cvv = uh.get_cvv(username)[0][0]
        self.assertIsInstance(cvv, str)

    def test_get_day_pass(self):
        # Assuming a valid username
        username = "testuser"
        day_pass = uh.get_day_pass(username)[0][0]
        self.assertIsInstance(day_pass, str)

    def test_get_complaints(self):
        complaints = uh.get_complaints()
        self.assertIsInstance(complaints, list)

if __name__ == '__main__':
    unittest.main()
