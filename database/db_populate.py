import sqlite3

with sqlite3.connect("../bike_app.db") as db:
    cursor = db.cursor()

# populate user table with operator, manager and user records (1 of each)
user_records = (("Operator Man", "operatorman", "operatorpass", "operator"),
                ("Manager Man", "managerman", "managerpass", "manager"),
                ("Jeremy", "jeremy1999", "p1234", "customer"))
# if record already exists, silently skip that record without causing an error
cursor.executemany("""INSERT OR IGNORE INTO user(name, username, password, type)
                            VALUES(?, ?, ?, ?)""", user_records)
db.commit()


user_record = ("Jeremy", "jeremy1998", "p1234", "customer", 500)
# if record already exists, silently skip that record without causing an error
cursor.executemany("""INSERT OR IGNORE INTO user(name, username, password, type, wallet_amt)
                            VALUES(?, ?, ?, ?, ?)""", [user_record])
db.commit()

# populate location table
location_records = (("Kelvingrove", "1", "30"),
                    ("City Centre", "0", "45"),
                    ("Argyle Street", "0", "25"),
                    ("Baker Street", "1", "20"),
                    ("Banner Road", "0", "15"),
                    ("Essex Drive", "1", "25"),
                    ("System", "0", "26"))
cursor.executemany("INSERT OR IGNORE INTO location(name, has_charging, capacity) VALUES(?, ?, ?)", location_records)
db.commit()

# populate vehicle model table
model_records = (("E-scooter", "2", "5", "1.5", "10000"),
                 ("E-bike", "3", "6", "1.1", "15000"))
cursor.executemany("""INSERT OR IGNORE INTO
                            vehicle_model(name, fare_rate, charge_rate, discharge_rate, maintenance_interval) 
                            VALUES(?, ?, ?, ?, ?)""", model_records)
db.commit()

# populate vehicle table
# mentioning id explicitly to fail the constraint check and skip the record in case it already exists
# (id is the only unique column in this table)
vehicle_records = (("1" ,"1", "1"),
                   ("2", "1", "2"),
                   ("3", "2", "1"),
                   ("4", "2", "2"),
                   ("5", "3", "1"),
                   ("6", "4", "1"),
                   ("7", "5", "2"),
                   ("8", "6", "1"),
                   ("9", "6", "2"),
                   ("10", "5", "1"),
                   ("11", "4", "1"),
                   ("12", "5", "2"),
                   ("13", "4", "1"),
                   ("14", "3", "2"),
                   ("15", "2", "1"))
cursor.executemany("INSERT OR IGNORE INTO vehicle(id, location_id, model_id) VALUES(?, ?, ?)", vehicle_records)
db.commit()

# populate ride table
ride_records = (("1", "1", "1", "1", "3", "2023-09-03 02:34:56", "2023-09-03 02:45:36", "32"),
                ("2", "1", "2", "3", "1", "2023-09-03 07:17:24", "2023-09-03 07:52:07", "45"))
cursor.executemany("""INSERT OR IGNORE INTO 
                            ride(id, user_id, vehicle_id, start_location_id, end_location_id, start_time, end_time, fare) 
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?)""", ride_records)
db.commit()

# populate complaint table
# TODO: add some records with images
# TODO: add some records with ride ids
complaint_records = (("1", "3", "brakes not functioning", "hi,\nthe brakes of the bike are too loose.\nregards,\njeremy", "2023-09-03 07:52:07", "2023-09-03 09:55:07", "open"),)
cursor.executemany("""INSERT OR IGNORE INTO complaint(id, vehicle_id, subject, description, time_opened, time_closed, 
status) VALUES(?, ?, ?, ?, ?, ?, ?)""", complaint_records)
db.commit()

# print all the records in all the tables
cursor.execute("SELECT * FROM user")
print("user:", cursor.fetchall())
cursor.execute("SELECT * FROM location")
print("location:", cursor.fetchall())
cursor.execute("SELECT * FROM vehicle_model")
print("vehicle_model:", cursor.fetchall())
cursor.execute("SELECT * FROM vehicle")
print("vehicle:", cursor.fetchall())
cursor.execute("SELECT * FROM ride")
print("ride:", cursor.fetchall())
cursor.execute("SELECT * FROM complaint")
print("complaint:", cursor.fetchall())

db.close()