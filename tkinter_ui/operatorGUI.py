# This is for creating operator interface

import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
from hashlib import md5
import requests
from tkinter import messagebox, StringVar


class OperaterGUI:
    def __init__(self, root, flask_app_url):
        self.complaints_table = None
        self.dropdown = None
        self.search_button = None
        self.search_entry = None
        self.radiobutton_frame = None
        self.root = root
        self.root.title("Ride-Sharing App")
        self.root.geometry('700x700')
        self.root.resizable(width=True, height=True)
        self.table = None
        self.entry_new_location = None

        # Added an icon
        self.root.iconbitmap('../Images/icon.ico')

        # Flask app URL
        self.flask_app_url = flask_app_url

        # Initialise Frames
        self.main_window_frame = None
        self.login_frame = None
        self.sign_up_frame = None
        self.change_frame = None
        self.operator_window_frame = None
        self.move_frame = None
        self.current_frame = None
        self.report_frame = None
        self.discription_frame = None

        # Create main window
        self.create_main_window()

    def create_main_window(self):
        # Create a frame to place contents of a page
        self.main_window_frame = ttk.Frame(self.root)
        self.main_window_frame.pack(padx=20, pady=20)

        # Adding Image
        self.home_img = ImageTk.PhotoImage(Image.open('../Images/home_img.jpg'))
        self.home_img_label = ttk.Label(self.main_window_frame, image=self.home_img)
        self.home_img_label.pack()

        # Create UI elements
        self.button_frame = ttk.Frame(self.main_window_frame)
        self.button_frame.pack()

        # Create Login button
        self.login_button = ttk.Button(self.button_frame, text="Login", command=self.show_login_page, width=20)
        self.login_button.pack(side=tk.LEFT, padx=20)

        # Create signup button
        self.signup_button = ttk.Button(self.button_frame, text="Sign Up", command=self.show_signup_page, width=20)
        self.signup_button.pack(side=tk.LEFT, padx=20)

        # Change current frame
        self.current_frame = self.main_window_frame

    def show_login_page(self):
        # Hide the main window frame
        self.current_frame.pack_forget()

        # Create Login Frame
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(padx=20, pady=20)

        # Create a title label
        title_label = ttk.Label(self.login_frame, text="Login", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Create a frame for the username and password
        input_frame = ttk.Frame(self.login_frame)
        input_frame.pack(pady=10)

        # Username Label and Entry
        username_label = ttk.Label(input_frame, text="Username:", font=("Arial", 18))
        username_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.username_entry = ttk.Entry(input_frame, font=("Arial", 18))
        self.username_entry.grid(row=0, column=1, padx=(0, 10))

        # Password Label and Entry
        password_label = ttk.Label(input_frame, text="Password:", font=("Arial", 18))
        password_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.password_entry = ttk.Entry(input_frame, show="*", font=("Arial", 18))
        self.password_entry.grid(row=1, column=1, padx=(0, 10))

        # Create a login button
        login_button = ttk.Button(self.login_frame, text="Login", command=self.login, width=20)
        login_button.pack(pady=20)

        # Create a back button
        back_button = ttk.Button(self.login_frame, text="Go Back", command=self.show_main_window, width=10)
        back_button.pack(anchor=tk.NW, padx=10, pady=10)

        # Change current frame
        self.current_frame = self.login_frame

    def show_signup_page(self):
        # Hide the main window frame
        self.current_frame.pack_forget()

        # Create sign up Frame
        self.sign_up_frame = ttk.Frame(self.root)
        self.sign_up_frame.pack(padx=20, pady=20)

        # Create a title label
        title_label = ttk.Label(self.sign_up_frame, text="SignUp", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Create a frame for the username and password
        input_frame = ttk.Frame(self.sign_up_frame)
        input_frame.pack(pady=10)

        # Username Label and Entry
        username_label = ttk.Label(input_frame, text="Username:", font=("Arial", 18))
        username_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.username_entry = ttk.Entry(input_frame, font=("Arial", 18))
        self.username_entry.grid(row=0, column=1, padx=(0, 10))

        # Password Label and Entry
        password_label = ttk.Label(input_frame, text="Set Password:", font=("Arial", 18))
        password_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.password_entry = ttk.Entry(input_frame, show="*", font=("Arial", 18))
        self.password_entry.grid(row=1, column=1, padx=(0, 10))

        # Create a signup button
        sign_up_button = ttk.Button(self.sign_up_frame, text="Sign Up", command=self.signup, width=20)
        sign_up_button.pack(pady=20)

        # Create a back button
        back_button = ttk.Button(self.sign_up_frame, text="Go Back", command=self.show_main_window, width=10)
        back_button.pack(anchor=tk.NW, padx=10, pady=10)

        # Change current frame
        self.current_frame = self.sign_up_frame

    def show_operator_interface(self):
        # Hide the current frame
        if self.current_frame:
            self.current_frame.pack_forget()

        # Create a frame to place contents of the page
        self.operator_window_frame = ttk.Frame(self.root)
        self.operator_window_frame.pack(padx=20, pady=20)

        # add page title
        title_label = ttk.Label(self.operator_window_frame, text="Operator Interface", font=("Arial", 15, "bold"))
        title_label.grid(row=0, column=0, pady=10)

        # Create other UI elements for OperatorGUI
        menubutton = ttk.Menubutton(self.operator_window_frame, text="Your account")
        menubutton.grid(row=1, column=0, sticky=tk.NW, padx=20)  # Changed pack to grid
        menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=menu)
        menu.add_command(label="Logout", command=self.show_main_window)
        menu.add_command(label="Change Password", command=self.show_changepassword_page)
        menu.add_command(label="view report", command=self.show_report_page)

        # Search Bar at the top center
        search_frame = ttk.Frame(self.operator_window_frame)
        search_frame.grid(row=2, column=0, pady=20)  # Changed pack to grid
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = ttk.Button(search_frame, text="Search", command=self.search)
        self.search_button.pack(side=tk.LEFT)

        # Adding the radio buttons for 'Status'
        self.status_var = tk.StringVar(value="all")  # Setting a default value
        status_radiobutton_frame = ttk.Frame(self.operator_window_frame)
        status_radiobutton_frame.grid(row=3, column=0, pady=5, sticky=tk.W)
        ttk.Label(status_radiobutton_frame, text="Status:").pack(side=tk.LEFT, padx=5)  # Instruction label for status

        # List of status options and their respective values
        status_options = [
            ("All", "all"),
            ("Parked", "parked"),
            ("in_transit", "in_transit"),
            ("low_battery", "low_battery"),
            ("defect_reported", "defect_reported")
        ]

        # Create and pack each Radiobutton for status options
        for text, value in status_options:
            rb = ttk.Radiobutton(status_radiobutton_frame, text=text, variable=self.status_var, value=value)
            rb.pack(side=tk.LEFT, padx=5)

        # Adding the radio buttons for 'search filter'
        self.radio_var = tk.StringVar(value="BikeID")  # Setting a default value

        filter_radiobutton_frame = ttk.Frame(self.operator_window_frame)
        filter_radiobutton_frame.grid(row=4, column=0, pady=5, sticky=tk.W)
        ttk.Label(filter_radiobutton_frame, text="search filter:").pack(side=tk.LEFT,
                                                                        padx=5)  # Instruction label for filter
        bikeID_rb = ttk.Radiobutton(filter_radiobutton_frame, text="BikeID", variable=self.radio_var, value="BikeID")
        bikeID_rb.pack(side=tk.LEFT, padx=5)
        location_rb = ttk.Radiobutton(filter_radiobutton_frame, text="Location", variable=self.radio_var,
                                      value="Location")
        location_rb.pack(side=tk.LEFT, padx=5)

        # Adding the vehicle table
        self.table = ttk.Treeview(self.operator_window_frame, columns=("Location", "Battery", "Time Limit"))
        self.table.heading("#0", text="BikeID")
        self.table.heading("#1", text="Location")
        self.table.heading("#2", text="Battery")
        self.table.heading("#3", text="Time Limit")

        # get data from server
        try:
            results = self.get_bike_data_from_server()
            bike_ids = results['bike_id']
            location_names = results['location_name']
            battery_levels = results['battery_level']
            time_limit = results['time_limit']

            for bike_id, location_name, battery_level, time in zip(bike_ids, location_names, battery_levels,
                                                                   time_limit):
                self.table.insert("", "end", text=bike_id, values=(location_name, battery_level, time))

        except Exception as e:
            print(f"Error while fetching bike data: {e}")
            # give message to users

        # Changes the width of the table by modifying the width.
        self.table.column("#0", width=100)
        self.table.column("#1", width=100)
        self.table.column("#2", width=100)
        self.table.column("#3", width=100)

        # Pack the table
        self.table.grid(row=5, column=0, pady=5)

        # Bottom Buttons
        bottom_frame = ttk.Frame(self.operator_window_frame)
        bottom_frame.grid(row=6, column=0, pady=20)  # Changed pack to grid
        charge_button = ttk.Button(bottom_frame, text="Charge", command=self.charge)
        charge_button.pack(side=tk.LEFT, padx=10)
        # able_button = ttk.Button(bottom_frame, text="Able/unable", command=self.able)
        # able_button.pack(side=tk.LEFT, padx=10)
        move_button = ttk.Button(bottom_frame, text="Move", command=self.move)
        move_button.pack(side=tk.LEFT, padx=10)
        # change current frame
        self.current_frame = self.operator_window_frame

    def show_changepassword_page(self):
        # Hide the main window frame
        if self.current_frame:
            self.current_frame.pack_forget()
        # Create sign up Frame
        self.change_frame = ttk.Frame(self.root)
        self.change_frame.pack(padx=20, pady=20)

        # Create a title label
        title_label = ttk.Label(self.change_frame, text="Change password", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Create a frame for the username and password
        input_frame = ttk.Frame(self.change_frame)
        input_frame.pack(pady=10)

        # Password Label and Entry
        password_label = ttk.Label(input_frame, text="Set Password:", font=("Arial", 18))
        password_label.grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        self.password_entry = ttk.Entry(input_frame, show="*", font=("Arial", 18))
        self.password_entry.grid(row=1, column=1, padx=(0, 10))

        # Create a signup button
        confirm_button = ttk.Button(self.change_frame, text="change", command=self.change, width=20)
        confirm_button.pack(pady=20)

        # Create a back button
        back_button = ttk.Button(self.change_frame, text="Go Back", command=self.show_operator_interface, width=10)
        back_button.pack(anchor=tk.NW, padx=10, pady=10)
        # change current frame
        self.current_frame = self.change_frame

    def show_main_window(self):
        # Hide the "next window" frame
        self.current_frame.pack_forget()

        # Show the main window frame again
        self.main_window_frame.pack()
        # change current frame
        self.current_frame = self.main_window_frame

    def show_move_page(self, selected_item):
        # Hide frame
        self.current_frame.pack_forget()

        # Create the move_frame here
        self.move_frame = ttk.Frame(self.root)

        self.move_frame.pack()

        # get data from server
        '''response = requests.get(f'{self.flask_app_url}/get_bike_info', json={'item': selected_item})
        bike_info = response.json()'''

        values = self.table.item(selected_item, "values")
        vehicle_id = self.table.item(selected_item, "text")
        # Create UI

        label_id = ttk.Label(self.move_frame, text=f"Bike ID: {vehicle_id}")
        label_id.pack(pady=10)
        label_current_location = ttk.Label(self.move_frame, text=f"Current location: {values[0]}")
        label_current_location.pack(pady=10)
        label_new_location = ttk.Label(self.move_frame, text="New location:")
        label_new_location.pack(pady=10)
        self.entry_new_location = ttk.Entry(self.move_frame)
        self.entry_new_location.pack(pady=10)
        move_button = ttk.Button(self.move_frame, text="Move",
                                 command=self.move_bike)
        move_button.pack(pady=10)
        back_button = ttk.Button(self.move_frame, text="Back to Operator Page", command=self.show_operator_interface)
        back_button.pack(pady=20)
        # change current frame
        self.current_frame = self.move_frame

    def move_bike(self):
        selected_item = self.table.selection()
        if selected_item:
            # Extract the data from the selected item
            values = self.table.item(selected_item, "values")
            if values:
                vehicle_id = self.table.item(selected_item, "text")  # Get the Vehicle ID (from the text column)
                print("Vehicle ID:", vehicle_id)
                print("Location:", values[0])
                response = requests.post(f'{self.flask_app_url}/move_vehicle',
                                         json={'vehicle_id': vehicle_id, 'location': self.entry_new_location.get()})
                if response.status_code == 200:
                    print("Vehicle moved successfully", vehicle_id)
                    print(response.json)
                    self.show_operator_interface()
                else:
                    print("Task failed")
        else:
            # send message
            messagebox.showwarning("Warning", "Please select an item first!")
            return

    def login(self):
        # add entry
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Check the input
        if not username.strip() or not password.strip():
            messagebox.showerror("Error", "Please enter both username and a password.")
            return
        password = md5(self.password_entry.get().encode('utf-8')).hexdigest()

        # Make an HTTP POST request to the Flask app for user registration
        response = requests.post(f'{self.flask_app_url}/login', json={'username': username, 'password': password})

        if response.status_code == 200:
            print("Login successful")
            # Add code to go to user profile
        else:
            print("Login failed")
        self.show_operator_interface()
        # Clear input
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def signup(self):
        # add entry
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Send message
        if not username.strip() or not password.strip():
            messagebox.showerror("Error", "Please enter both username and a password.")
            return

        # Make an HTTP POST request to the Flask app for user registration
        response = requests.post(f'{self.flask_app_url}/signup', json={'username': username, 'password': password})

        if response.status_code == 200:
            print("Registration successful")
            self.show_login_page()
        else:
            print("Registration failed")
            print(response.status_code)
        # Clear input
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def change(self):
        # add entry
        password = self.password_entry.get()
        if not password.strip():
            messagebox.showerror("Error", "Please enter password.")
            return
        password = md5(self.password_entry.get().encode('utf-8')).hexdigest()

        # Make an HTTP POST request to the Flask app for user registration
        response = requests.post(f'{self.flask_app_url}/signup', json={'password': password})

    def search(self):
        # get input and radiobutton
        query = self.search_entry.get()
        choice1 = self.radio_var.get()
        choice2 = self.status_var.get()

        # check if radiobutton is selected
        if not choice1 or not choice2:
            messagebox.showwarning("Warning", "Please select a search criterion first!")
            return

        # send HTTP POST to Flask app
        response = requests.post(f'{self.flask_app_url}/search_operator_vehicles', json={
            'search_text': query,
            'search_field': self.radio_var.get(),
            'status_filter': self.status_var.get()
        })

        # show success or failed
        if response.status_code == 200:
            results = response.json()
            if results:
                self.update_search_results(results)
            else:
                messagebox.showerror("Error", "No results found for your search.")
        else:
            all_items = self.table.get_children()
            for item_id in all_items:
                self.table.delete(item_id)
            messagebox.showerror("Error", "Failed to retrieve search results. Please try again.")

    def update_search_results(self, results):
        print('Inside update_search_results')

        # Delete all rows while keeping column headers
        all_items = self.table.get_children()
        for item_id in all_items:
            self.table.delete(item_id)

        # Extract data from results
        bike_ids = results['bike_id']
        bike_types = results['location_name']
        battery_level = results['battery_level']
        time_limits = results['time_limit']

        # Loop through each item and insert it into the table
        for bike_id, bike_type, charge, time_limit in zip(bike_ids, bike_types, battery_level, time_limits):
            self.table.insert("", "end", text=bike_id, values=(bike_type, charge, time_limit))

        return

    def charge(self):
        # get selected vehicle
        selected_item = self.table.selection()
        if selected_item:
            # Extract the data from the selected item
            values = self.table.item(selected_item, "values")
            if values:
                vehicle_id = self.table.item(selected_item, "text")  # Get the Vehicle ID (from the text column)
        else:
            messagebox.showwarning("Warning", "Please select an item first!")
            return
        # send data to server
        response = requests.post(f'{self.flask_app_url}/charge', json={'vehicle_id': vehicle_id})

        if response.status_code == 200:
            print("Charging successful for item:", selected_item)
        else:
            print("Charging failed")

    def able(self):
        # get selected vehicle
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item first!")
            return
        # send requests to server
        response = requests.post(f'{self.flask_app_url}/able_unable', json={'item': selected_item})

        if response.status_code == 200:
            print("Setting able/unable successful for item:", selected_item)
        else:
            print("Setting able/unable failed")

    def move(self):
        # get selected vehicle
        selected_item = self.table.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an item from the search results.")
            return

        # Show the move page, where the user can specify the new location for the bike.
        self.show_move_page(selected_item)

    def get_bike_data_from_server(self):
        # get data from server
        response = requests.post(f'{self.flask_app_url}/get_all_bike')

        if response.status_code != 200:
            # Handle non-success status codes
            raise Exception(f"Error: Received status code {response.status_code} from server.")

        return response.json()  # Assuming server returns JSON formatted data

    #  report page
    def show_report_page(self):
        # Hide the current frame
        self.current_frame.pack_forget()
        # Create a frame to place contents of the page
        self.report_frame = ttk.Frame(self.root)
        self.report_frame.pack(padx=20, pady=20)

        # add title
        title_label = ttk.Label(self.report_frame, text="Complaints Report", font=("Arial", 15, "bold"))
        title_label.grid(row=0, column=0, pady=10)

        # Search Bar at the top center
        search_frame = ttk.Frame(self.report_frame)
        search_frame.grid(row=1, column=0, pady=10)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_button = ttk.Button(search_frame, text="Search", command=self.search_complaints)
        self.search_button.pack(side=tk.LEFT)

        # Radio buttons for status
        status_frame = ttk.Frame(self.report_frame)
        status_frame.grid(row=2, column=0, pady=5)
        ttk.Label(status_frame, text="Status:").pack(side=tk.LEFT, padx=5)  # Instruction label for status
        self.status_var = tk.StringVar(value="all")
        open_rb = ttk.Radiobutton(status_frame, text="Open", variable=self.status_var, value="open")
        closed_rb = ttk.Radiobutton(status_frame, text="Closed", variable=self.status_var, value="closed")
        all_rb = ttk.Radiobutton(status_frame, text="All", variable=self.status_var, value="all")
        open_rb.pack(side=tk.LEFT, padx=5)
        closed_rb.pack(side=tk.LEFT, padx=5)
        all_rb.pack(side=tk.LEFT, padx=5)

        # Radio buttons for search column
        column_frame = ttk.Frame(self.report_frame)
        column_frame.grid(row=3, column=0, pady=5)
        ttk.Label(column_frame, text="Search by:").pack(side=tk.LEFT, padx=5)  # Instruction label for search column
        self.column_var = tk.StringVar(value="complaint ID")
        vehicleID_rb = ttk.Radiobutton(column_frame, text="Vehicle ID", variable=self.column_var, value="vehicle ID")
        complaintID_rb = ttk.Radiobutton(column_frame, text="Complaint ID", variable=self.column_var,
                                         value="complaint ID")
        subject_rb = ttk.Radiobutton(column_frame, text="Subject", variable=self.column_var, value="subject")
        vehicleID_rb.pack(side=tk.LEFT, padx=5)
        complaintID_rb.pack(side=tk.LEFT, padx=5)
        subject_rb.pack(side=tk.LEFT, padx=5)

        # add Table
        self.complaints_table = ttk.Treeview(self.report_frame,
                                             columns=("complaint id", "vehicle id", "subject", "time opened", "status"))
        self.complaints_table.heading("#0", text="Complaint ID")
        self.complaints_table.heading("#1", text="Vehicle ID")
        self.complaints_table.heading("#2", text="Subject")
        self.complaints_table.heading("#3", text="Time Opened")
        self.complaints_table.heading("#4", text="Status")

        # ... Populate the table using data from the server ...

        # Define column widths
        self.complaints_table.column("#0", width=100)
        self.complaints_table.column("#1", width=100)
        self.complaints_table.column("#2", width=100)
        self.complaints_table.column("#3", width=100)
        self.complaints_table.column("#4", width=100)

        # Bind a double-click event to open the selected complaint
        self.complaints_table.bind("<Double-1>", self.open_complaint)
        self.complaints_table.grid(row=4, column=0, pady=5)

        # get data from server
        try:
            results = self.get_report_data_from_server()
            complaint_ids = results['complaint_id']
            vehicle_ids = results['vehicle_id']
            subjects = results['subject']
            time_opened = results['time_opened']
            statuses = results['status']
            for complaint_id, vehicle_id, subject, time, status in zip(complaint_ids, vehicle_ids, subjects,
                                                                       time_opened, statuses):
                self.complaints_table.insert("", "end", text=complaint_id, values=(vehicle_id, subject, time, status))

        except Exception as e:
            print(f"Error while fetching bike data: {e}")

        # Creating a new frame for the buttons
        buttons_frame = ttk.Frame(self.report_frame)
        buttons_frame.grid(row=5, column=0, pady=20)

        # Adding a "Back" button inside buttons_frame
        back_button = ttk.Button(buttons_frame, text="Back", command=self.show_operator_interface)
        back_button.pack(side=tk.LEFT, padx=10)  # padx is used to give some space between the buttons

        # Adding a "Resolve" button next to "Back" button inside buttons_frame
        resolve_button = ttk.Button(buttons_frame, text="Repair", command=self.resolve_complaint)
        resolve_button.pack(side=tk.LEFT, padx=10)
        # Change current frame
        self.current_frame = self.report_frame

    def resolve_complaint(self):
        selected_item = self.complaints_table.selection()
        if selected_item:
            # Extract the data from the selected item
            values = self.table.item(selected_item, "values")
            if values:
                complaint_id = self.table.item(selected_item, "text")  # Get the Vehicle ID (from the text column)
                vehicle_id = values[0]
                print("complaint_id :", complaint_id)
                print("vehicle_id:", vehicle_id)
                response = requests.post(f'{self.flask_app_url}/resolve_complaint',
                                         json={'vehicle_id': vehicle_id, 'complaint_id': complaint_id})
                if response.status_code == 200:
                    print("Defect resolved successfully", vehicle_id)
                    print(response.json)
                    self.show_report_page()
                else:
                    print("Task failed")
        else:
            # send message
            messagebox.showwarning("Warning", "Please select an item first!")
            return

    def get_report_data_from_server(self):
        # Get data from server
        response = requests.post(f'{self.flask_app_url}/get_all_report')

        if response.status_code != 200:
            # Handle non-success status codes
            raise Exception(f"Error: Received status code {response.status_code} from server.")

        return response.json()  # Assuming server returns JSON formatted data

    def search_complaints(self):
        # Get input
        search_term = self.search_entry.get()
        # Get radio button
        status_selected = self.status_var.get()
        column_selected = self.column_var.get()

        if not status_selected or not column_selected:
            messagebox.showinfo("Info", "Please select the status and column for search.")
            return

        query = {
            "search_term": search_term,
            "status": status_selected,
            "column": column_selected
        }
        # page data
        response_data = self.get_complaints_from_server(query)

        if response_data:
            self.update_complaints_table(response_data)

    def get_complaints_from_server(self, query):
        # get data from server
        try:
            response = requests.post(f'{self.flask_app_url}/search_complaints', json=query)

            if response.status_code == 200:
                return response.json()
            else:
                all_items = self.complaints_table.get_children()
                for item_id in all_items:
                    self.complaints_table.delete(item_id)
                messagebox.showerror("Error", "Failed to fetch data from server.")
                return []

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return []

    def update_complaints_table(self, results):
        # update table
        all_items = self.complaints_table.get_children()
        for item_id in all_items:
            self.complaints_table.delete(item_id)

        # Extract data from results
        complaint_ids = results['complaint_id']
        vehicle_ids = results['vehicle_id']
        subjects = results['subject']
        time_openeds = results['time_opened']
        statuses = results['status']

        # Loop through each item and insert it into the table
        for complaint_id, vehicle_id, subject, time_opened, status in zip(complaint_ids, vehicle_ids, subjects,
                                                                          time_openeds, statuses):
            self.complaints_table.insert("", "end", text=complaint_id,
                                         values=(vehicle_id, subject, time_opened, status))

        return

    def open_complaint(self, event):
        # get selected data
        selected_item = self.complaints_table.selection()[0]
        complaint_id = self.complaints_table.item(selected_item)["text"]
        complaint_details = self.get_complaint_details_from_server(complaint_id)
        # if get data show detail
        if complaint_details:
            self.show_complaint_details(complaint_details)

    def get_complaint_details_from_server(self, complaint_id):
        # get data from server
        try:
            response = requests.get(f'{self.flask_app_url}/get_complaint_details',
                                    params={"complaint_id": complaint_id})
            # Show message
            if response.status_code == 200:
                return response.json()
            else:
                messagebox.showerror("Error", "Failed to fetch complaint details from server.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return None

    def show_complaint_details(self, details):
        # Hide the current frame
        self.current_frame.pack_forget()

        # Create a new frame for complaint details
        self.complaint_details_frame = ttk.Frame(self.root)
        self.complaint_details_frame.pack(padx=20, pady=20)

        # Create a title label
        title_label = ttk.Label(self.complaint_details_frame, text="Description", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Add a label to show the complaint details
        complaint_label = ttk.Label(self.complaint_details_frame, text=details["description"], wraplength=500,
                                    font=("Arial", 18))
        complaint_label.pack(pady=20)

        # Create a frame for the buttons
        button_frame = ttk.Frame(self.complaint_details_frame)
        button_frame.pack(pady=20)

        # Add "Back" button
        back_button = ttk.Button(button_frame, text="Back", command=self.show_operator_interface(), width=10)
        back_button.grid(row=0, column=0, padx=20)

        # Add "Able/Unable" button
        # able_unable_button = ttk.Button(button_frame, text="Able/Unable", command=self.able, width=20)
        # able_unable_button.grid(row=0, column=1, padx=20)
        # change current frame
        self.current_frame = self.complaint_details_frame


def main():
    root = ThemedTk()
    root.set_theme('radiance')  # choose one from list
    available_themes = root.get_themes()
    print(available_themes)
    flask_app_url = 'http://localhost:5000'
    app = OperaterGUI(root, flask_app_url)
    root.mainloop()


if __name__ == "__main__":
    main()
