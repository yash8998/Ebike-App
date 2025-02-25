import sqlite3

with sqlite3.connect("../bike_app.db") as db:
    cursor = db.cursor()

cursor.execute("DROP TABLE vehicle_model")
db.commit()
# User table
cursor.execute("""CREATE TABLE IF NOT EXISTS user(    
    id integer PRIMARY KEY,
    type text NOT NULL CHECK (type in ('customer', 'operator', 'manager')),
    name text NOT NULL,
    username text NOT NULL UNIQUE,
    password text NOT NULL,
    day_pass_available text,
    credit_card text,
    cvv text,
    wallet_amt integer,
    deposit_amt integer);""")
db.commit()

# Location table
cursor.execute("""CREATE TABLE IF NOT EXISTS location(
    id integer PRIMARY KEY,
    name text NOT NULL UNIQUE,
    has_charging boolean NOT NULL CHECK (has_charging IN (0,1)),
    num_of_vehicles integer NOT NULL DEFAULT 0,
    capacity integer NOT NULL);""")
db.commit()

# Vehicle model table
cursor.execute("""CREATE TABLE IF NOT EXISTS vehicle_model(
    id integer PRIMARY KEY,
    name text NOT NULL UNIQUE,
    fare_rate integer NOT NULL,
    charge_rate integer NOT NULL,
    discharge_rate integer NOT NULL,
    maintenance_interval integer)""")
db.commit()

# Vehicle table
cursor.execute("""CREATE TABLE IF NOT EXISTS vehicle(
    id integer PRIMARY KEY,
    model_id integer NOT NULL,
    status text NOT NULL CHECK (status in ('parked', 'in_transit', 'low_battery', 'defect_reported')) DEFAULT "parked",
    location_id integer NOT NULL,
    time_travelled integer NOT NULL DEFAULT 0,
    battery_level integer NOT NULL DEFAULT 100,
    FOREIGN KEY (location_id) REFERENCES location (id),
    FOREIGN KEY (model_id) REFERENCES vehicle_model (id))""")
db.commit()

# cursor.execute("""DROP TABLE IF EXISTS vehicle""")
# db.commit()

# Ride table
cursor.execute("""CREATE TABLE IF NOT EXISTS ride(
    id integer PRIMARY KEY,
    user_id integer NOT NULL,
    vehicle_id integer NOT NULL,
    start_location_id integer NOT NULL,
    end_location_id integer,
    start_time timestamp NOT NULL,
    end_time timestamp,
    fare integer,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicle (id),
    FOREIGN KEY (start_location_id) REFERENCES location (id),
    FOREIGN KEY (end_location_id) REFERENCES location (id))
    """)
db.commit()

# Complaint table
# including vehicle_id (required) as well as ride_id (optional ) because user does not have to initiate a ride to raise a complaint
# TODO: limit description text to 150 chars
cursor.execute("""CREATE TABLE IF NOT EXISTS complaint(
    id integer PRIMARY KEY,
    vehicle_id integer NOT NULL,
    ride_id integer,
    subject text,
    description text,
    time_opened timestamp NOT NULL,
    time_closed timestamp,
    status text NOT NULL CHECK (status in ('open', 'closed')) DEFAULT 'open',
    image blob,
    FOREIGN KEY (vehicle_id) REFERENCES vehicle (id),
    FOREIGN KEY (ride_id) REFERENCES ride (id))""")
db.commit()

# TODO: decide constraint states
# TODO: add logging and maybe an assertion that all six tables must be in the database

# list all the created tables in the database (there should be 6):
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

db.close()
