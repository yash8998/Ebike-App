import sqlite3

from database.location_helpers import get_num_vehicles_at_loc, get_loc_capacity, get_loc_id_by_name


def set_vehicle_loc(vehicle_id, location):
    """
    move vehicle to a location provided the location has space
    :param location: string
    :param vehicle_id: int
    :return: None
    """
    if get_num_vehicles_at_loc(get_loc_id_by_name(location)) == get_loc_capacity(get_loc_id_by_name(location)):
        print("cannot move vehicle, location is full!")  # TODO: raise something here?
        return False
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "UPDATE vehicle SET location_id=? WHERE id=?"
        cursor.execute(query, [get_loc_id_by_name(location), vehicle_id])
        db.commit()
        return True


def get_vehicles_at_loc(loc_id):
    """
    get vehicle records for vehicles parked at a specific location
    :param loc_id: int
    :return: tuple
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT * FROM vehicle WHERE location_id=?"
        cursor.execute(query, [loc_id])
        return cursor.fetchall()


def get_loc_id(vehicle_id):
    """
    get location id for a vehicle
    :param vehicle_id:
    :return: tuple
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT location_id FROM vehicle WHERE id=?"
        cursor.execute(query, [vehicle_id])
        return cursor.fetchall()[0][0]


def get_vehicles_by_status(status):
    """
    get vehicles records for vehicles with a specific status (charging, in_transit, etc.)
    :param status: str
    :return: tuple
    """
    # TODO: raise something when invalid value is provided as status
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT * FROM vehicle WHERE status=?"
        cursor.execute(query, [status])
        return cursor.fetchall()


def get_battery_level(vehicle_id):
    """
    get battery level for the vehicle
    :param vehicle_id: int
    :return: int
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT battery_level FROM vehicle WHERE id=?"
        cursor.execute(query, [vehicle_id])
        return cursor.fetchall()[0][0]


def get_status(vehicle_id):
    """
    get battery level for the vehicle
    :param vehicle_id: int
    :return: string
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT status FROM vehicle WHERE id=?"
        cursor.execute(query, [vehicle_id])
        return cursor.fetchall()


def update_status(vehicle_id, state):
    """
    update status for vehicle
    :param state: string
    :param vehicle_id: int
    :return: string
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "UPDATE vehicle SET status=? WHERE id=?"
        cursor.execute(query, [state, vehicle_id])
        db.commit()


def update_battery_level(vehicle_id, battery):
    """
    update battery level for the vehicle after ride ends or after charging
    :param battery: int
    :param vehicle_id: int
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "UPDATE vehicle SET battery_level=? WHERE id=?"
        cursor.execute(query, [battery, vehicle_id])
        db.commit()


def find_bike(loc_id):
    """
    get vehicle records for vehicles parked at a specific location
    :param loc_id: int
    :return: tuple
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = '''
				SELECT 
					v.id,vm.name AS VEHICLE_TYPE,v.battery_level,0.9 * round(v.battery_level/vm.discharge_rate,2) as Time_limit 
				FROM vehicle v
				LEFT OUTER JOIN vehicle_model vm ON v.model_id = vm.id
				LEFT OUTER JOIN location loc ON loc.id = v.location_id
				WHERE location_id=? AND STATUS = 'parked'
				'''
        cursor.execute(query, [loc_id])
        return cursor.fetchall()


def filter_vehicles(search_text="", search_field="BikeID",
                    status=["parked", "in_transit", "low_battery", "defect_reported"]):
    # TODO: what if search_field is something else?
    with (sqlite3.connect("bike_app.db") as db):
        cursor = db.cursor()

        if status == "all":
            status = ["parked", "in_transit", "low_battery", "defect_reported"]
        else:
            status = [status]

        # sqlite does not allow for lists to be passed as param to a single ? in cursor.execute()
        # hence a hack to programmatically include a ? for each status in status list in the WHERE status in ()
        # clause
        base_query = f"""
                    SELECT v.id, l.name, v.battery_level, 0.9*v.battery_level/vm.discharge_rate
                    FROM vehicle v
                    INNER JOIN vehicle_model vm ON v.model_id = vm.id
                    INNER JOIN location l on v.location_id = l.id 
                    WHERE status IN (%s)
                     """ % ",".join("?" * len(status))
        if not search_text:
            query = base_query
            cursor.execute(query, status)
        # if user has entered some text and field radio button is set to vehicle id
        elif search_field == "BikeID":
            query = base_query + " AND v.id=?"
            filter = status + [search_text]  # create a single list for all filter params
            cursor.execute(query, filter)
        # if user has entered some text and field radio button is set to location
        else:
            query = base_query + f" AND LOWER(l.name) LIKE LOWER(?)"
            filter = status + [search_text]  # create a single list for all filter params
            cursor.execute(query, filter)

        records = cursor.fetchall()
        print(records)
        return records
        # return cursor.fetchall()


def filter_complaints(search_text="", search_field="complaint_id", status=["open", "closed"]):
    # TODO: what if search_field is something else?
    with (sqlite3.connect("bike_app.db") as db):
        cursor = db.cursor()

        if status == "all":
            status = ["open", "closed"]
        else:
            status = [status]

        # sqlite does not allow for lists to be passed as param to a single ? in cursor.execute()
        # hence a hack to programmatically include a ? for each status in status list in the WHERE status in ()
        # clause
        base_query = f"""
                      SELECT c.id, v.id, c.subject, c.time_opened, c.status
                      FROM complaint c
                      INNER JOIN vehicle v ON c.vehicle_id = v.id
                      WHERE c.status IN (%s)
                      """ % ",".join("?" * len(status))

        if not search_text:
            query = base_query
            cursor.execute(query, status)
        # if user has entered some text and field radio button is set to vehicle id
        elif search_field == "vehicle ID":
            query = base_query + " AND v.id=?"
            filter = status + [search_text]  # create a single list for all filter params
            cursor.execute(query, filter)
        # if user has entered some text and field radio button is set to complaint id
        elif search_field == "complaint ID":
            query = base_query + " AND c.id=?"
            filter = status + [search_text]  # create a single list for all filter params
            cursor.execute(query, filter)
        # field radio button is set to "subject" -- search by subject
        else:
            query = base_query + " AND LOWER(c.subject) LIKE LOWER(?)"
            filter = status + ["%" + search_text + "%"]  # create a single list for all filter params
            cursor.execute(query, filter)
        return cursor.fetchall()


def get_complaint(complaint_id):
    with (sqlite3.connect("bike_app.db") as db):
        cursor = db.cursor()
        query = "SELECT * FROM complaint WHERE id=?"
        cursor.execute(query, [complaint_id])
        return cursor.fetchall()


def get_all_complaints():
    with (sqlite3.connect("bike_app.db") as db):
        cursor = db.cursor()
        query = "SELECT id,vehicle_id,subject,time_opened,status FROM complaint"
        cursor.execute(query)
        return cursor.fetchall()


def get_all_bikes():
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = '''
    				SELECT 
    					v.id,loc.name,v.battery_level,0.9 * v.battery_level/vm.discharge_rate as Time_limit 
    				FROM vehicle v
    				LEFT OUTER JOIN vehicle_model vm ON v.model_id = vm.id
    				LEFT OUTER JOIN location loc ON loc.id = v.location_id
    				'''
        cursor.execute(query)
        return cursor.fetchall()


def add_complaint(vehicle_id, subject, description, ride_id=None, image=None):
    update_status(vehicle_id, "defect_reported")
    with (sqlite3.connect("bike_app.db") as db):
        cursor = db.cursor()
        query = """INSERT INTO complaint(vehicle_id, ride_id, subject, description, time_opened, image)
                   VALUES(?, ?, ?, ?, CURRENT_TIMESTAMP, ?)"""
        cursor.execute(query, [vehicle_id, ride_id, subject, description, image])
        db.commit()


def close_complaint(complaint_id):
    """
    close complaint for vehicle
    :param :complaint_id int
    :return: string
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "UPDATE complaint SET status='closed',time_closed=CURRENT_TIMESTAMP WHERE id=?"
        cursor.execute(query, [complaint_id])
        db.commit()


# test prints (temporary)
if __name__ == '__main__':
    print(filter_vehicles(search_text=""))
    add_complaint(1, "battery exploded", "battery spontaneously combusted :(")
    print(filter_complaints(search_text=""))
    # print(get_vehicles_by_status("parked"))
    # print(get_vehicles_at_loc(1))
    # print(get_vehicles_at_loc(2))
    # print(set_vehicle_loc(1, 2))
    # print(get_vehicles_at_loc(1))
    # print(get_vehicles_at_loc(2))
    print(get_all_complaints())
