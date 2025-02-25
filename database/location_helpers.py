import sqlite3


def get_loc_by_id(loc_id):
    """
    get location record for a given location id
    :param loc_ids: int
    :return: tuple
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT * FROM location WHERE id=?"
        cursor.execute(query, [loc_id])
        # TODO: raise the correct exception here
        try:
            return cursor.fetchall()[0]
        except:
            return None


def get_loc_id_by_name(loc_name):
    """
    get corresponding location id for a given location name
    :param loc_name: str
    :return: int (if name in db), None (if name not in db)
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT id FROM location WHERE lower(name)=?"
        cursor.execute(query, [loc_name.lower()])
        try:
            return cursor.fetchall()[0][0]
        except:
            # TODO: raise the correct exception here
            return None

def get_loc_name_by_id(loc_id):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT name FROM location WHERE id=?"
        cursor.execute(query, [loc_id])
        try:
            return cursor.fetchall()[0][0]
        except:
            # TODO: raise the correct exception here
            return None

def get_num_vehicles_at_loc(loc_id):
    """
    get number of vehicles parked at a specific location
    :param loc_id: int
    :return: int
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = "SELECT num_of_vehicles FROM location WHERE id=?"
        cursor.execute(query, [loc_id])
        capacity = cursor.fetchall()[0][0]
        return capacity


def get_loc_capacity(loc_id):
    """
    get the parking capacity of a specific location
    :param loc_id: int
    :return: int
    """
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        _, _, _, _, loc_capacity = get_loc_by_id(loc_id)
        return loc_capacity

def get_charging_locations():
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()

        # query available charging locations sorted in increasing order of available capacity
        query = """
                SELECT name, (capacity - num_of_vehicles) AS available_capacity
                FROM location
                WHERE has_charging=1 AND num_of_vehicles < capacity
                ORDER BY available_capacity DESC
                """
        cursor.execute(query)
        return cursor.fetchall()

def get_all_locations():
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        query = """
                SELECT id, name
                FROM location
                """
        cursor.execute(query)
        return cursor.fetchall()

if __name__ == '__main__':
    # test prints (temporary)
    # print(get_loc_capacity(2))
    # print(get_num_vehicles_at_loc(2))
    # print(get_loc_id_by_name("Argyle Street"))
    # print(get_loc_by_id(1))
    # print(get_charging_locations())
    print(get_all_locations())
