import sqlite3


def add_user(user_data):
    """
    Add user record
    :param user_data: list

    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """INSERT INTO user( name,username, password, type,day_pass_available,credit_card,cvv,wallet_amt,deposit_amt)
                            VALUES(?,?, ?, ?,?,?,?,?,?)"""
        cursor.execute(query, user_data)
        db.commit()


def get_users(username):
    """
    get username
    :param username: string
    :return: tuple
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT username FROM user WHERE username=?"
        cursor.execute(query, [username])
        try:
            return cursor.fetchall()
        except:
            return None


def get_password(username):
    """
    get password for user
    :param username:
    :return: string
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT password FROM user WHERE username=?"
        cursor.execute(query, [username])
        return cursor.fetchall()


def debit_wallet_amount(username, amount):
    """
        update wallet after ride ends
        :param username: text
        :param amount: int
        """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """UPDATE user SET wallet_amt=wallet_amt-? WHERE username=?"""
        cursor.execute(query, [amount, username])
        db.commit()


def credit_wallet_amount(username, amount):
    """
        update wallet after ride ends
        :param username: text
        :param amount: int
        """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """UPDATE user SET wallet_amt=wallet_amt+? WHERE username=?"""
        cursor.execute(query, [amount, username])
        db.commit()


def debit_deposit_amount(username, amount):
    """
        update deposit after ride ends
        :param username: text
        :param amount: int
        """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """UPDATE user SET deposit_amt=deposit_amt-? WHERE username=?"""
        cursor.execute(query, [amount, username])
        db.commit()


def credit_deposit_amount(username, amount):
    """
        update deposit after ride ends
        :param username: text
        :param amount: int
        """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """UPDATE user SET deposit_amt=deposit_amt+? WHERE username=?"""
        cursor.execute(query, [amount, username])
        db.commit()


def get_wallet_balance(username):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """Select wallet_amt from user WHERE username=?"""
        cursor.execute(query, [username])
        return cursor.fetchall()


def get_deposit_balance(username):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """Select deposit_amt from user WHERE username=?"""
        cursor.execute(query, [username])
        return cursor.fetchall()


def add_card_details(user_name, card_details, cvv):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """UPDATE user SET credit_card=?,cvv=? WHERE username=?"""
        cursor.execute(query, [card_details, cvv, user_name])
        db.commit()


def get_users_details(username):
    """
    get username
    :param username: string
    :return: tuple
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT * FROM user WHERE username=?"
        cursor.execute(query, [username])
        return cursor.fetchall()


def get_cvv(username):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT cvv FROM user WHERE username=?"
        cursor.execute(query, [username])
        return cursor.fetchall()


def get_day_pass(username):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT day_pass_available FROM user WHERE username=?"
        cursor.execute(query, [username])
        return cursor.fetchall()


def get_complaints():
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT * FROM complaint"
        cursor.execute(query)
        return cursor.fetchall()


def get_user_id(username):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT id FROM user WHERE username=?"
        cursor.execute(query, [username])
        return cursor.fetchall()[0][0]


if __name__ == '__main__':
    # print(get_users('jeremy1999'))
    # debit_wallet_amount('jeremy1998', 100)
    print(get_complaints())
