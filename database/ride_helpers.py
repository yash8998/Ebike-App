import sqlite3


def add_ride(user_data):
    """
    Add user record
    :param user_data: list

    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """INSERT INTO ride( user_id,vehicle_id, start_location_id,start_time)
                            VALUES(?, ?, ?, CURRENT_TIMESTAMP)"""
        cursor.execute(query, user_data)
        db.commit()


def update_ride(ride_id, end_location_id,fare):
    """
    Add end ride location
    :param ride_id:
    :param end_location_id:

    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """UPDATE ride SET end_location_id=?, fare=?, end_time=CURRENT_TIMESTAMP WHERE id=?"""
        cursor.execute(query, [end_location_id, fare, ride_id])
        db.commit()


def get_current_ride():
    """
    Gives the last ride id
    :param ride_id:
    :param end_location_id:

    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """Select id from ride order by id desc"""
        cursor.execute(query)
        return cursor.fetchall()[0][0]


def get_ride_hist_by_user(user_id):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT id,vehicle_id, start_time, fare FROM ride WHERE user_id=?"
        cursor.execute(query, [user_id])
        return cursor.fetchall()