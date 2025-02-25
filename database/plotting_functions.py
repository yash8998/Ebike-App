import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from database import location_helpers as lh

import matplotlib
matplotlib.use('Agg')

def location_heatmap_helper(date_range=None):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        if not date_range:
            query = """
                    SELECT start_location_id, end_location_id, COUNT(*)
                    FROM ride
                    GROUP BY start_location_id, end_location_id
                    """
            cursor.execute(query)
        else:
            query = """
                    SELECT start_location_id, end_location_id, COUNT(*)
                    FROM ride
                    WHERE end_time IS NOT NULL AND (date(ride.start_time) BETWEEN ? AND ?)
                    GROUP BY start_location_id, end_location_id
                    """
            cursor.execute(query, date_range)
        return cursor.fetchall()

def ride_durations_helper(date_range=None):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        if not date_range:
            query = """
                    SELECT vehicle_model.name, ROUND((julianday(end_time) - julianday(start_time))*86400) AS duration
                    FROM ride
                    INNER JOIN vehicle ON ride.vehicle_id=vehicle.id
                    INNER JOIN vehicle_model ON vehicle.model_id=vehicle_model.id 
                    WHERE ride.end_time IS NOT NULL
                    """
            cursor.execute(query)
        else:
            query = """
                    SELECT vehicle_model.name, ROUND((julianday(end_time) - julianday(start_time))*86400) AS duration
                    FROM ride
                    INNER JOIN vehicle ON ride.vehicle_id=vehicle.id
                    INNER JOIN vehicle_model ON vehicle.model_id=vehicle_model.id 
                    WHERE ride.end_time IS NOT NULL AND (date(ride.start_time) BETWEEN ? AND ?)
                    """
            cursor.execute(query, date_range)
        return cursor.fetchall()

def complaint_resolution_time_helper(date_range=None):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        if not date_range:
            query = """
                    SELECT ROUND((julianday(time_closed) - julianday(time_opened))*86400) AS tat
                    FROM complaint
                    WHERE time_closed IS NOT NULL
                    """
            cursor.execute(query)
        else:
            query = """
                    SELECT ROUND((julianday(time_closed) - julianday(time_opened))*86400) AS tat
                    FROM complaint
                    WHERE time_closed IS NOT NULL AND (date(time_opened) BETWEEN ? AND ?)
                    """
            cursor.execute(query, date_range)
        return cursor.fetchall()

def revenue_location_model_helper(date_range=None):
    with sqlite3.connect("bike_app.db") as db:
        cursor = db.cursor()
        if not date_range:
            query = """
                    SELECT location.name, vehicle_model.name, SUM(IFNULL(ride.fare, 0))
                    FROM location CROSS JOIN vehicle_model
                    LEFT JOIN vehicle ON vehicle_model.id=vehicle.model_id
                    LEFT JOIN ride ON vehicle.id=ride.vehicle_id AND location.id=ride.start_location_id
                    GROUP BY location.name, vehicle_model.name
                    """
            cursor.execute(query)
        else:
            query = """
                    SELECT location.name, vehicle_model.name, SUM(IFNULL(ride.fare, 0))
                    FROM location CROSS JOIN vehicle_model
                    LEFT JOIN vehicle ON vehicle_model.id=vehicle.model_id
                    LEFT JOIN ride ON vehicle.id=ride.vehicle_id AND location.id=ride.start_location_id
                    WHERE (date(ride.start_time) BETWEEN ? AND ?) OR (date(ride.start_time) IS NULL)
                    GROUP BY location.name, vehicle_model.name
                    """
            cursor.execute(query, date_range)
        return cursor.fetchall()

def location_heatmap(date_range=None):
    locations = lh.get_all_locations()
    loc_ids = [loc[0] for loc in locations if loc[0] != 4]
    loc_names = [loc[1] for loc in locations if loc[0] != 4]
    location_ride_counts = location_heatmap_helper(date_range)

    ride_count_matrix = np.zeros(shape=(len(loc_names), len(loc_names)))
    for record in location_ride_counts:
        if record[0] != 4 and record[1] != 4:
            # using loc_ids.index() in case ids are not contiguous from 1 (1,2,3,...)
            ride_count_matrix[loc_ids.index(record[0]), loc_ids.index(record[1])] = record[2]
    print(ride_count_matrix)

    ax = sns.heatmap(ride_count_matrix, linewidth=0.5, xticklabels=loc_names, yticklabels=loc_names, annot=True, square=True)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment="right")
    plt.xlabel("Destination Station")
    plt.ylabel("Starting Station")
    plt.title("Most Popular Trips")
    plt.savefig("traffic_flow.jpg", bbox_inches="tight")
    plt.close()

def ride_durations(date_range=None):
    durations = ride_durations_helper(date_range)
    df = pd.DataFrame(durations, columns=["Model", "Duration"])
    print(df)
    with sns.axes_style("darkgrid"):
        if df.empty:
            sns.displot(df, x="Duration", bins=50, binrange=[0, 80]).set(
                title="Model-wise Ride Duration")
        else:
            sns.displot(df, x="Duration", bins=50, hue="Model", binrange=[0, 80]).set(
                title="Model-wise Ride Duration")
        plt.xlabel('Ride Duration (seconds)')
        plt.savefig("ride_durations.jpg", bbox_inches="tight")
        plt.close()

def complaint_resolution_time(date_range=None):
    times = complaint_resolution_time_helper(date_range)
    times = [t[0] for t in times]
    df = pd.DataFrame(times, columns=["TAT"])
    print(df)
    with sns.axes_style("darkgrid"):
        sns.displot(df, x="TAT", bins=50, binrange=[0, 4000]).set(title="Complaint Turnaround Time")
        plt.xlabel('Turnaround Time (seconds)')
        plt.ylim(0, None)
        plt.savefig("complaint_tat.jpg", bbox_inches="tight")
        plt.close()

def revenue_location_model(date_range=None):
    records = revenue_location_model_helper(date_range)
    df = pd.DataFrame(records, columns=["Station", "Model", "Revenue"])
    print(df)
    with sns.axes_style("darkgrid"):
        ax = sns.catplot(df, x="Station", y="Revenue", hue="Model", kind="bar", palette=['purple', 'steelblue'])
        plt.xticks(rotation=45)
        plt.ylabel('Revenue (£)')
        plt.title("Model-wise Revenue at each Station")
        plt.savefig("revenue_chart.jpg", bbox_inches="tight")
        plt.close()


# ride_durations_helper(["2023-11-03 02:34:56", "2023-11-03 02:34:56"])
# complaint_resolution_time(["2023-11-03 02:34:56", "2023-11-03 02:34:56"])
# revenue_location_model(["2023-11-03 02:34:56", "2023-11-03 02:34:56"])
# ride_durations(["2023-11-03 02:34:56", "2023-11-03 02:34:56"])
# location_heatmap(["2023-11-03 02:34:56", "2023-11-03 02:34:56"])