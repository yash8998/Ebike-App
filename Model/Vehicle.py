import time
import functools
import threading


class Vehicle:

    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        self.state = None
        self.max_duration = None
        self.battery_percentage = None
        self.start_time_var = None
        self.end_time_var = None

    def set_state(self, state):
        self.state = state

    def start_time(self):
        self.start_time_var = time.perf_counter()

    def end_time(self):
        self.end_time_var = time.perf_counter()
        return self.end_time_var - self.start_time_var

    def set_max_time_limit(self, max_duration):
        self.max_duration = max_duration
        self.set_battery_percentage(max_duration)

    def set_battery_percentage(self, max_duration):
        # I have assumed a rate of 5s per 10% of battery
        self.battery_percentage = max_duration * 0.02

    def battery_after_ride(self, duration):
        # Same logic as set_battery_percentage()
        self.battery_percentage -= duration * 0.02
        return self.battery_percentage

    def call_end_time_after_timeout(self, timeout_seconds):
        # Create a partial function that calls end_timing
        end_time_partial = functools.partial(self.end_time)

        # Create a timer thread to call end_time_partial after the specified timeout
        timer_thread = threading.Timer(timeout_seconds, end_time_partial)
        timer_thread.start()


def timeout_decorator(timeout_seconds):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            instance = args[0]  # Get the instance of the class

            # Start timing
            instance.start_time()

            # Call the original function
            result = func(*args, **kwargs)

            # Check if the timeout is exceeded
            if instance.end_time() > timeout_seconds:
                print("Timeout exceeded. Ending the ride.")
            return result

        return wrapper

    return decorator
