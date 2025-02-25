import threading
import re
from hashlib import md5

from flask import Flask, request, jsonify, make_response
from Model import Vehicle
from database import location_helpers as lh
from database import vehicle_helpers as vh
from database import user_helpers as uh
from database.location_helpers import get_loc_id_by_name
from database import ride_helpers as rh
from database import plotting_functions as pf

# Create a Flask web application
app = Flask(__name__)
app.config['DATABASE'] = 'bike_app.db'

# Simulated database for rides (replace with SQLite or other)
rides = []

# Append Vehicle objects to this dictionary; key is vehicle ID and value is Vehicle object
current_rides = {}
user_rides = {}
ride_data = {}
active_rides = {}


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # name = data['name']
    username = data['username']
    password = data['password']

    # Appending to list for now, but we need to add to tables
    if uh.get_users(username):
        print(uh.get_users(username))
        return jsonify({'message': 'Registration Failed'}), 401
    elif len(password) < 8 or not re.search(r'\d', password):
        print('Password needs to be at least 8 characters and must contain at least one digit')
        return jsonify({'message': 'Registration Failed'}), 402
    else:
        password = md5(password.encode('utf-8')).hexdigest()
        user_record = ['yash', username, password, 'customer', 'no', 'xyz', 'xyz', 0, 0]
        uh.add_user(user_record)
        print(f'{username} inserted')
        return jsonify({'message': 'Registration Successful'}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    username = data['username']
    password = data['password']

    print(password, uh.get_password(username))
    # Appending to list for now, but we need to add to tables
    if username in uh.get_users(username)[0]:
        if password == uh.get_password(username)[0][0]:
            print(f'Login Successful for user {username}')
            security_deposit = uh.get_deposit_balance(username)[0][0]
            if security_deposit < 80:
                return jsonify(
                    {'message': 'Login Successful', 'redirect': 'top-up',
                     'acc_bal': uh.get_wallet_balance(username)[0][0],
                     'sec_bal': uh.get_deposit_balance(username)[0][0]}), 200
            return jsonify(
                {'message': 'Login Successful', 'redirect': 'book-ride',
                 'acc_bal': uh.get_wallet_balance(username)[0][0],
                 'sec_bal': uh.get_deposit_balance(username)[0][0]}), 200
        else:
            print('Wrong Password')
            return jsonify({'message': 'Login Failed'}), 401
    else:
        print(f'Username not found')
        return jsonify({'message': 'Login Failed'}), 401


@app.route('/manager_login', methods=['POST'])
def manager_login():
    data = request.get_json()

    username = data['username']
    password = data['password']

    print(password, uh.get_password(username))
    # Appending to list for now, but we need to add to tables
    if username in uh.get_users(username)[0]:
        if password == uh.get_password(username)[0][0]:
            print(f'Login Successful for user {username}')
            return jsonify(
                {'message': 'Login Successful'}), 200
        else:
            print('Wrong Password')
            return jsonify({'message': 'Login Failed'}), 401
    else:
        print(f'Username not found')
        return jsonify({'message': 'Login Failed'}), 401

def get_max_duration(vehicle_id):
    # Return max time limit based on battery
    battery = vh.get_battery_level(vehicle_id)
    battery = battery[0][0]
    # Assumed a distance of 2s per unit of battery
    max_time_limit = battery * 2
    return max_time_limit


def get_vehicle_state(vehicle_id):
    return vh.get_status(vehicle_id)


def update_vehicle_state(vehicle_id, state):
    vh.update_status(vehicle_id, state)


@app.route('/find_bike', methods=['POST'])
def find_bike():
    data = request.get_json()

    location = data['location'].lower()
    location_id = get_loc_id_by_name(location)
    vehicle_data = vh.find_bike(location_id)

    if vehicle_data:
        return jsonify({
            "bike_id": [row[0] for row in vehicle_data],
            "bike_type": [row[1] for row in vehicle_data],
            "battery_level": [row[2] for row in vehicle_data],
            "time_limit": [row[3] for row in vehicle_data]
        },
        ), 200
    else:
        print('Incorrect location or no vehicle available')
        return jsonify({'message': 'No vehicle available at this location'}), 401


@app.route('/book', methods=['POST'])
def book_ride():
    data = request.get_json()

    username = data['username']
    vehicle_id = data['vehicle_id']
    max_time_limit = float(data['values'][2])
    print(f'Vehicle ID : {vehicle_id} is available for booking\nMax run time for ride is {max_time_limit}')

    # Create a Vehicle instance
    vehicle = Vehicle.Vehicle(vehicle_id)
    # Start the ride automatically with the timeout decorator
    timeout_seconds = max_time_limit
    start_ride_response = start_ride(username, vehicle, timeout_seconds)

    return start_ride_response, 200


# Use the timeout_decorator from Vehicle.py to decorate the start_ride method

def start_ride(username, vehicle, timeout_seconds):
    with app.app_context():
        def ride_timeout():
            # This function will be called if the ride isn't ended in time
            end_ride_by_system(username, vehicle)

        # Create a new thread to handle the ride
        ride_thread = threading.Thread(target=ride_timeout)
        ride_thread.daemon = True
        ride_thread.start()

        # Set a timer for ending the ride after `timeout_seconds`
        vehicle.start_time()
        ride_data[vehicle.vehicle_id] = vehicle
        user_rides[username] = vehicle.vehicle_id
        timer = threading.Timer(timeout_seconds, end_ride_by_system, args=(username, vehicle,))
        timer.start()

        # Update state of vehicle
        vh.update_status(vehicle.vehicle_id, 'in_transit')
        # Store the thread and timer in the vehicles_in_transit dictionary
        active_rides[vehicle.vehicle_id] = timer
        ride_record = [uh.get_user_id(username), vehicle.vehicle_id, vh.get_loc_id(vehicle.vehicle_id)]
        rh.add_ride(ride_record)
        ride_id = rh.get_current_ride()
        current_rides[vehicle.vehicle_id] = ride_id
        return make_response(jsonify({'message': 'Ride started successfully'}), 200)


def end_ride_by_system(username, vehicle):
    with app.app_context():

        vehicle_id = vehicle.vehicle_id

        if vehicle_id in active_rides:
            # Cancel the timer for this ride
            active_timer = active_rides[vehicle_id]
            active_timer.cancel()

            # Calculate ride duration
            current_veh = ride_data[vehicle_id]
            ride_duration = current_veh.end_time()
            vh.set_vehicle_loc(vehicle_id, 'System')
            vh.update_status(vehicle_id, 'parked')
            vh.update_battery_level(vehicle_id, ride_duration / 1.2)
            # Remove the ride from the active_rides dictionary
            del active_rides[vehicle_id]
            del ride_data[vehicle_id]
            del user_rides[username]

            if vh.get_battery_level(vehicle_id) <= 10:
                vh.update_status(vehicle_id, 'low_battery')

            amount_source, fare, discount_applied = payment(username, ride_duration, 'no')
            ride_id = current_rides[vehicle.vehicle_id]
            end_loc_id = lh.get_loc_id_by_name('System')
            rh.update_ride(ride_id, end_loc_id, fare)

            del current_rides[vehicle.vehicle_id]

            print('Ride ended by System')
            if amount_source == 'wallet':
                response_data = {
                    'message': 'Ride Ended by System',
                    'fare': fare,
                    'source': 'wallet',
                    'duration_seconds': ride_duration,
                    'discount': discount_applied
                    # Include additional details as needed
                }
                return make_response(jsonify(response_data), 200)
            else:
                response_data = {
                    'message': 'Ride Ended by System',
                    'fare': fare,
                    'source': 'deposit',
                    'duration_seconds': ride_duration,
                    'discount': discount_applied
                    # Include additional details as needed
                }
                return make_response(jsonify(response_data), 200)
        else:
            return make_response(jsonify({'message': 'Vehicle not found in transit'}), 404)


# Use if the user ends the ride on time
@app.route('/end_ride', methods=['POST'])
def end_ride_by_user():
    with app.app_context():
        data = request.get_json()
        location = data['location']
        print(location)
        username = data['username']
        is_charging = data['type'].lower()
        vehicle_id = user_rides[username]

        if vehicle_id in active_rides:
            # Cancel the timer for this ride
            active_timer = active_rides[vehicle_id]
            active_timer.cancel()

            # Calculate ride duration
            current_veh = ride_data[vehicle_id]
            ride_duration = current_veh.end_time()
            vh.set_vehicle_loc(vehicle_id, location.lower())
            vh.update_status(vehicle_id, 'parked')
            vh.update_battery_level(vehicle_id, ride_duration / 1.2)
            # Remove the ride from the active_rides dictionary
            del active_rides[vehicle_id]
            del ride_data[vehicle_id]
            if vh.get_battery_level(vehicle_id) <= 10:
                vh.update_status(vehicle_id, 'low_battery')

            amount_source, fare, discount_applied = payment(username, ride_duration, is_charging)

            ride_id = current_rides[vehicle_id]
            end_loc_id = lh.get_loc_id_by_name(location.lower())
            rh.update_ride(ride_id, end_loc_id, fare)

            del current_rides[vehicle_id]

            if amount_source == 'wallet':
                response_data = {
                    'message': 'Ride Ended by user',
                    'fare': fare,
                    'source': 'wallet',
                    'duration_seconds': ride_duration,
                    'discount': discount_applied,
                    'acc_bal': uh.get_wallet_balance(username)[0][0],
                    'sec_bal': uh.get_deposit_balance(username)[0][0]
                    # Include additional details as needed
                }
                return make_response(jsonify(response_data), 200)
            else:
                response_data = {
                    'message': 'Ride Ended by user',
                    'fare': fare,
                    'source': 'deposit',
                    'duration_seconds': ride_duration,
                    'discount': discount_applied,
                    'acc_bal': uh.get_wallet_balance(username)[0][0],
                    'sec_bal': uh.get_deposit_balance(username)[0][0]
                    # Include additional details as needed
                }
                return make_response(jsonify(response_data), 200)
        else:
            return make_response(jsonify({'message': 'Vehicle not found in transit'}), 404)


def payment(username, ride_duration, is_charging):
    wallet_balance = uh.get_wallet_balance(username)[0][0]

    # Check if user has day pass
    is_day_pass = uh.get_day_pass(username)[0][0].lower()
    fare = ride_duration * 1.5
    discount_applied = 0

    # Apply day pass discount
    if is_day_pass == 'yes':
        discount_applied += fare * 0.2

    # Apply discount if user parks in a parking lot with charging
    if is_charging == 'yes':
        discount_applied += fare * 0.05

    # Calculate total fare
    total_fare = round(fare - discount_applied, 2)
    print(f'Fare of the ride was {total_fare}')

    if wallet_balance >= total_fare:
        uh.debit_wallet_amount(username, total_fare)
        return 'wallet', total_fare, discount_applied
    else:
        uh.debit_wallet_amount(username, wallet_balance)
        uh.debit_deposit_amount(username, total_fare - wallet_balance)
        return 'deposit', total_fare, discount_applied


@app.route('/top_up', methods=['POST'])
def wallet_payment():
    data = request.get_json()
    username = data['username']
    amount = data['amount']
    wallet_or_deposit = data['type']
    cvv = data['cvv']
    print(cvv)
    print(uh.get_cvv(username))
    if cvv == uh.get_cvv(username)[0][0]:

        if wallet_or_deposit == 'deposit':
            uh.credit_deposit_amount(username, amount)
            print(f'Security deposit credited with {amount}')
            return jsonify({'message': 'Payment Successful'}), 200
        else:
            uh.credit_wallet_amount(username, amount)
            print(f'Wallet credited with {amount}')
            return jsonify({'message': 'Payment Successful'}), 200
    else:
        return jsonify({'message': 'Payment Failed, Enter correct cvv'}), 401


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.get_json()

    username = data['username']
    feed_back = data['feedback']
    security_deposit = data['sec_bal']

    # Add feedback to database
    if security_deposit < 70:
        return jsonify({'message': 'Feedback Successful', 'redirect': 'top-up'}), 200
    return jsonify({'message': 'Feedback Successful', 'redirect': 'book-ride'}), 200


@app.route('/submit_report', methods=['POST'])
def submit_report():
    data = request.get_json()

    vehicle_id = data['vehicle_id']
    username = data['username']
    report_content = data['report']
    subject = data['subject']

    # Add report to database
    try:
        vh.add_complaint(vehicle_id, subject, report_content)
        vh.update_status(vehicle_id, 'defect_reported')
        print(f'Report submitted')
        return jsonify({'message': 'Report Submission Successful'}), 200
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return jsonify({'message': 'Report Submission Failed'}), 401


@app.route('/resolve_complaint', methods=['POST'])
def resolve_complaint():
    data = request.get_json()

    vehicle_id = data['vehicle_id']
    complaint_id = data['complaint_id']

    # Add report to database
    try:
        vh.close_complaint(complaint_id)
        vh.update_status(vehicle_id, 'parked')
        print(f'Complaint closed successfully')
        return jsonify({'message': 'Complaint closed successfully'}), 200
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return jsonify({'message': 'Could not close complaint'}), 401


@app.route('/card_reg', methods=['POST'])
def card_registration():
    data = request.get_json()
    user_name = data['username']
    card_details = data['card_details']
    cvv = data['cvv']
    print(cvv)
    print(user_name)
    print(card_details)
    uh.add_card_details(user_name, card_details, cvv)
    print(f'Card details inserted')
    return jsonify({'message': 'Card Registration Successful'}), 200


@app.route('/move_vehicle', methods=['POST'])
def move_vehicle():
    # TODO: check whether vehicle is in transit (cannot move in transit)
    data = request.get_json()
    print(data)
    vehicle_id = data["vehicle_id"]
    location = data["location"]
    # location_id = lh.get_loc_id_by_name(location)
    is_vehicle_moved = vh.set_vehicle_loc(vehicle_id, location)
    if is_vehicle_moved:
        return jsonify({'message': 'Moved vehicle'}), 200
    else:
        return jsonify({'message': f'Cannot move, location {location} is full'}), 404


@app.route('/search_operator_vehicles', methods=['POST'])
def search_operator_vehicles():
    try:
        data = request.get_json()
        search_text = data["search_text"]  # string entered in the text box
        search_field = data["search_field"]  # which column to search? from radio button (by location or vehicle?)
        status_filter = data["status_filter"]  # filter by status; from radio button (in_transit, parked, etc.)

        print(data)
        # print(f"search text: {data['search_text']}")
        # print(f"search field: {data['search_field']}")
        # print(f"search filter: {data['status_filter']}")

        records = vh.filter_vehicles(search_text=search_text,
                                     search_field=search_field,
                                     status=status_filter)

        if records:
            return jsonify({
                "bike_id": [row[0] for row in records],
                "location_name": [row[1] for row in records],
                "battery_level": [row[2] for row in records],
                "time_limit": [row[3] for row in records]
            }), 200
        return jsonify({'message': 'No such vehicle or location'}), 401
    except Exception as e:
        # TODO: is this the right error code?
        return jsonify({'message': f'Search failed: {e}'}), 404


@app.route('/search_complaints', methods=['POST'])
def search_complaints():
    # try:
    data = request.get_json()
    search_text = data["search_term"]  # string entered in the text box
    search_field = data[
        "column"]  # which column to search? from radio button (by complaint, vehicle, or subject?)
    status_filter = data["status"]  # filter by status; from radio button (open, closed, etc.)

    records = vh.filter_complaints(search_text=search_text,
                                 search_field=search_field,
                                 status=status_filter)

    if records:
        return jsonify({
            "complaint_id": [row[0] for row in records],
            "vehicle_id": [row[1] for row in records],
            "subject": [row[2] for row in records],
            "time_opened": [row[3] for row in records],
            "status": [row[4] for row in records]
        }), 200
    return jsonify({"message": "No such complaint"}), 401
    # except Exception as e:
    #     print(e)
    #     return jsonify({"message": f"Search failed: {e}"}), 404


@app.route('/get_complaint', methods=['POST'])
def get_complaint():  # TODO: rename this (name same as vh.get_complaint)
    data = request.get_json()
    complaint_id = data["complaint_id"]
    record = vh.get_complaint(complaint_id)
    if record:
        return jsonify({"complaint_id": record[0],
                        "vehicle_id": record[1],
                        "ride_id": record[2],
                        "subject": record[3],
                        "description": record[4],
                        "time_opened": record[5],
                        "status": record[6],
                        "image": record[7]}), 200
    return jsonify({"message": "No such complaint"}), 401


@app.route('/get_all_report', methods=['POST'])
def get_report_data_from_server():
    records = vh.get_all_complaints()
    print(records)
    if records:
        return jsonify({
            "complaint_id": [row[0] for row in records],
            "vehicle_id": [row[1] for row in records],
            "subject": [row[2] for row in records],
            "time_opened": [row[3] for row in records],
            "status": [row[4] for row in records]
        }), 200
    return jsonify({"message": "No complaints"}), 401


@app.route('/get_all_bike', methods=['POST'])
def get_bike_data_from_server():
    records = vh.get_all_bikes()
    print(records)
    if records:
        return jsonify({
            "bike_id": [row[0] for row in records],
            "location_name": [row[1] for row in records],
            "battery_level": [row[2] for row in records],
            "time_limit": [row[3] for row in records]
        }), 200
    return jsonify({"message": "No bike data available"}), 401


@app.route('/get_trip_history', methods=['POST'])
def get_ride_history():
    data = request.get_json()
    username = data['username']
    user_id = uh.get_user_id(username)
    records = rh.get_ride_hist_by_user(user_id)
    print(records)
    if records:
        return jsonify({
            "TripID": [row[0] for row in records],
            "BikeID": [row[1] for row in records],
            "Time": [row[2] for row in records],
            "Price": [row[3] for row in records]
        }), 200
    return jsonify({"message": "No ride history for this user"}), 401


@app.route('/add_complaint', methods=['POST'])
def add_complaint():  # TODO: change this name
    try:
        data = request.get_json()
        vh.add_complaint(vehicle_id=data.get("vehicle_id"),
                         subject=data.get("subject"),
                         description=data.get("description"),
                         ride_id=data.get("ride_id"),
                         image=data.get("image")
                         )
        return jsonify({"message": "successfully added complaint record"}), 200
    except Exception as e:
        # TODO: is this the right status code?
        return jsonify({"message": f"failed to add record to complaint table: {e}"}), 404


@app.route('/repair_vehicle', methods=['POST'])
def repair_vehicle():
    data = request.get_json()
    vehicle_id = data["vehicle_id"]


    is_vehicle_moved = vh.set_vehicle_loc(vehicle_id, location_id=4)

    if is_vehicle_moved:
        vh.update_status(vehicle_id, "parked")
        return jsonify({'message': 'Moved vehicle'}), 200
    else:
        return jsonify({'message': f'Cannot move, repair center is full'}), 404


@app.route('/charge', methods=['POST'])
def charge():
    data = request.get_json()
    print(data)
    # status = data["status"]
    vehicle_id = data["vehicle_id"]

    # don't move a vehicle in transit to a charging location
    # if status == "in_transit":
    #     return jsonify({'message': f'Cannot charge vehicle in transit'}), 401

    # get available charging locations ordered by available capacity (descending)
    charging_locations = lh.get_charging_locations()

    # if all the charging spots are full then we can't charge the vehicle
    if not charging_locations:
        return jsonify({'message': f'No available charging points'}), 404

    # get the charging location with max available spots
    charge_loc = charging_locations[0][0]
    is_vehicle_moved = vh.set_vehicle_loc(vehicle_id, charge_loc)
    if is_vehicle_moved:
        vh.update_battery_level(vehicle_id, 100)
        vh.update_status(vehicle_id, state="parked")
        return jsonify(
            {'message': f'Vehicle {vehicle_id} set to charge at {charge_loc}'}), 200
    return jsonify({'message': 'Failed to move vehicle to charging location'}), 404


@app.route('/search_manager_report', methods=['POST'])
def search_manager_report():
    data = request.get_json()
    from_date = data['from_date']
    to_date = data['to_date']
    choice = data['choice']
    if 'Histogram ride duration' == choice:
        pf.ride_durations([from_date, to_date])
        return jsonify({'image_url': '../ride_durations.jpg'}), 200

    elif 'Confusion matrix popular paths' == choice:
        pf.location_heatmap([from_date, to_date])
        return jsonify({'image_url': '../traffic_flow.jpg'}), 200

    elif 'Revenue vs location' == choice:
        print('In revenue')
        pf.revenue_location_model([from_date, to_date])
        return jsonify({'image_url': '../revenue_chart.jpg'}), 200

    elif 'Time to close complaint histogram' == choice:
        pf.complaint_resolution_time([from_date, to_date])
        return jsonify({'image_url': '../complaint_tat.jpg'}), 200

    else:
        return jsonify({'message': 'No report found'}), 401


if __name__ == '__main__':
    app.run(debug=True)
