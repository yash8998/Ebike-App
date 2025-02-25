import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from database import location_helpers as lh

import matplotlib
matplotlib.use('Agg')


def revenue_location_model_helper(date_range=None):
    with sqlite3.connect("../bike_app.db") as db:
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


def complaint_resolution_time_helper(date_range=None):
    with sqlite3.connect("../bike_app.db") as db:
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


def complaint_resolution_time(date_range=None):
    times = complaint_resolution_time_helper(date_range)
    times = [t[0] for t in times]
    df = pd.DataFrame(times, columns=["TAT"])
    print(df)
    with sns.axes_style("darkgrid"):
        sns.displot(df, x="TAT", bins=50, binrange=[0, 10000]).set(title="Complaint Turnaround Time")
        plt.xlabel('Turnaround Time (seconds)')
        plt.ylim(0, None)
        plt.savefig("complaint_tat.jpg", bbox_inches="tight")
        plt.close()


# ride_durations_helper(["2023-11-03 02:34:56", "2023-11-03 02:34:56"])
complaint_resolution_time(["2023-11-03", "2023-11-03"])
revenue_location_model(["2023-11-03", "2023-11-03"])
# ride_durations(["2023-11-03 02:34:56", "2023-11-03 02:34:56"])
# location_heatmap(["2023-11-03 02:34:56", "2023-11-03 02:34:56"])