# This is for creating user interface

import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedTk
from PIL import ImageTk, Image
from hashlib import md5
import requests

from tkinter import ttk


class UserGUI:
    def __init__(self, root, flask_app_url):
        self.subject_input = None
        self.report_input = None
        self.security_balance = 0
        self.account_balance = 0
        self.feedback_frame = None
        self.feedback_input = None
        self.return_table = None
        self.username = None
        self.book_table = None
        self.location_entry = None
        self.password_entry = None
        self.root = root
        self.root.title("Ride-Sharing App")
        self.root.geometry('900x750')
        self.root.resizable(width=True, height=True)

        # Added an icon
        self.root.iconbitmap('../Images/icon.ico')

        # Flask app URL
        self.flask_app_url = flask_app_url

        # Initialise Frames
        self.main_window_frame = None
        self.login_frame = None
        self.sign_up_frame = None
        self.history_frame = None
        self.change_frame = None
        self.current_frame = None
        self.book_frame = None
        self.status_frame = None
        self.wallet_frame = None
        self.card_frame = None
        self.day_pass_frame = None
        self.success_frame = None
        self.confirm_order_frame = None

        # Address of record, added by min
        self.location_var = None

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

        self.login_button = ttk.Button(self.button_frame, text="Login", command=self.show_login_page, width=20)
        self.login_button.pack(side=tk.LEFT, padx=20)

        self.signup_button = ttk.Button(self.button_frame, text="Sign Up", command=self.show_signup_page, width=20, )
        self.signup_button.pack(side=tk.LEFT, padx=20)

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
        back_button = ttk.Button(self.login_frame, text="Go Back", command=self.show_main_window, width=20)
        back_button.pack(anchor=tk.NW, padx=10, pady=10)

        self.current_frame = self.login_frame

    def show_signup_page(self):
        # Hide the main window frame
        self.current_frame.pack_forget()

        # Create Login Frame
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

        # Create a login button
        sign_up_button = ttk.Button(self.sign_up_frame, text="Sign Up", command=self.signup, width=20)
        sign_up_button.pack(pady=20)

        # Create a back button
        back_button = ttk.Button(self.sign_up_frame, text="Go Back", command=self.show_main_window)
        back_button.pack(anchor=tk.NW, padx=10, pady=10)

        self.current_frame = self.sign_up_frame

    def wallet_info(self, account_balance, security_balance):
        # Hide the currently displayed interface
        self.current_frame.pack_forget()
        self.account_balance = int(account_balance)
        self.security_balance = int(security_balance)
        # Framework:
        # Basic Framework - wallet_frame
        self.wallet_frame = tk.Frame(self.root)
        self.wallet_frame.pack(padx=20, pady=20)

        # title
        title_label = tk.Label(self.wallet_frame, text="Wallet Information", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))
        # add page UI
        account_balance_label = ttk.Label(self.wallet_frame, text=f"Account Balance: {self.account_balance}")
        security_balance_label = ttk.Label(self.wallet_frame, text=f"Security Balance: {self.security_balance}")
        account_balance_label.pack(pady=10)
        security_balance_label.pack(pady=10)
        amount_label = ttk.Label(self.wallet_frame, text="Amount:", font=("Arial", 18))
        amount_label.pack(pady=10)
        self.amount_entry = ttk.Entry(self.wallet_frame, font=("Arial", 18))
        self.amount_entry.pack(pady=10)
        cvv_label = ttk.Label(self.wallet_frame, text="CVV:", font=("Arial", 18))
        cvv_label.pack(pady=10)
        self.cvv_entry = ttk.Entry(self.wallet_frame, font=("Arial", 18))
        self.cvv_entry.pack(pady=10)
        # "Top up" button to navigate to the next page
        top_up_deposit_button = ttk.Button(self.wallet_frame, text="Top up Deposit", command=self.top_up_deposit,
                                           width=20)
        top_up_deposit_button.pack(pady=10)
        top_up_wallet_button = ttk.Button(self.wallet_frame, text="Top up Wallet", command=self.top_up_wallet, width=20)
        top_up_wallet_button.pack(pady=10)

        # "Return" button to go back to the "Book a Bike" page
        if self.security_balance >= 80:
            return_button = ttk.Button(self.wallet_frame, text="Return", command=self.book_a_bike, width=20)
            return_button.pack(pady=10)

        # change current frame
        self.current_frame = self.wallet_frame

    def top_up_deposit(self):
        # get input
        amount = self.amount_entry.get()
        cvv = md5(self.cvv_entry.get().encode('utf-8')).hexdigest()
        # send data
        response = requests.post(f'{self.flask_app_url}/top_up',
                                 json={'username': self.username, 'amount': amount, 'type': 'deposit', 'cvv': cvv})

        if response.status_code == 200:
            print("Payment Successful")
            self.security_balance += int(amount)
        else:
            print("Payment failed")
        # Clear input
        self.amount_entry.delete(0, tk.END)
        self.cvv_entry.delete(0, tk.END)
        self.wallet_info(self.account_balance, self.security_balance)

    def top_up_wallet(self):
        # get input
        amount = self.amount_entry.get()
        cvv = md5(self.cvv_entry.get().encode('utf-8')).hexdigest()
        # send data
        response = requests.post(f'{self.flask_app_url}/top_up',
                                 json={'username': self.username, 'amount': amount, 'type': 'wallet', 'cvv': cvv})

        if response.status_code == 200:
            print("Payment Successful")
            self.account_balance += int(amount)
        else:
            print("Payment failed")
        # Clear input
        self.amount_entry.delete(0, tk.END)
        self.cvv_entry.delete(0, tk.END)
        self.wallet_info(self.account_balance, self.security_balance)

    def card_info(self):
        # Hide the currently displayed interface
        self.current_frame.pack_forget()

        # Basic Framework - card_frame
        self.card_frame = ttk.Frame(self.root)
        self.card_frame.pack(padx=20, pady=20)

        title_label = ttk.Label(self.card_frame, text="Card Information", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Create labels and input fields to enter credit card information
        card_number_label = ttk.Label(self.card_frame, text="Card Number:")
        card_number_label.pack(pady=(0, 20))
        self.card_number_entry = ttk.Entry(self.card_frame)
        self.card_number_entry.pack(pady=(0, 20))

        expiration_date_label = ttk.Label(self.card_frame, text="Expired Data: MM/YY ")
        expiration_date_label.pack(pady=(0, 20))
        self.expiration_date_entry = ttk.Entry(self.card_frame)
        self.expiration_date_entry.pack(pady=(0, 20))

        cvv_label = ttk.Label(self.card_frame, text="CVV:")
        cvv_label.pack(pady=(0, 20))
        self.cvv_entry = ttk.Entry(self.card_frame)
        self.cvv_entry.pack(pady=(0, 20))

        name_label = ttk.Label(self.card_frame, text="Name:")
        name_label.pack(pady=(0, 20))
        self.name_entry = ttk.Entry(self.card_frame)
        self.name_entry.pack(pady=(0, 20))
        # Add button UI
        save_button = ttk.Button(self.card_frame, text="Save", command=self.save_credit_card_info)
        save_button.pack(pady=10)
        back_to_book_button = ttk.Button(self.card_frame, text="Back to Book a Bike", command=self.book_a_bike)
        back_to_book_button.pack(pady=10)

        # Change current frame
        self.current_frame = self.card_frame

    def save_credit_card_info(self):
        # Get input
        card_number = self.card_number_entry.get()
        exp_date = self.expiration_date_entry.get()
        cvv = self.cvv_entry.get()
        name = self.name_entry.get()
        # check input
        if not card_number.strip() or not exp_date.strip() or not cvv.strip() or not name.strip():
            messagebox.showerror("Error", "Please enter all the details.")
            return

        # deal with detail
        card_details = card_number + name + exp_date
        card_details_hash = md5(card_details.encode('utf-8')).hexdigest()
        cvv_details_hash = md5(cvv.encode('utf-8')).hexdigest()
        # Make an HTTP POST request to the Flask app for user registration
        response = requests.post(f'{self.flask_app_url}/card_reg',
                                 json={'username': self.username, 'card_details': card_details_hash,
                                       'cvv': cvv_details_hash})

        if response.status_code == 200:
            print("Card registration successful")
            self.show_login_page()
            # self.login()
        else:
            print("Card Registration failed")
            print(response.status_code)

        # Clear input
        self.card_number_entry.delete(0, tk.END)
        self.expiration_date_entry.delete(0, tk.END)
        self.cvv_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)

    def day_pass(self):
        # forget frame
        self.current_frame.pack_forget()

        self.day_pass_frame = ttk.Frame(self.root)
        self.day_pass_frame.pack(padx=20, pady=20)
        # Add title
        title_label = ttk.Label(self.day_pass_frame, text="Buy a Day Pass", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Create labels to display Day-pass information
        day_pass_label = ttk.Label(self.day_pass_frame, text="Buy a Day-pass For XXX GBP")
        day_pass_label.pack(pady=10)

        # Create "Buy" button
        buy_button = ttk.Button(self.day_pass_frame, text="Buy", command=self.day_pass_success)
        buy_button.pack(pady=10)
        # change current frame
        self.current_frame = self.day_pass_frame

    def day_pass_success(self):
        # forget previous page
        self.current_frame.pack_forget()

        self.success_frame = ttk.Frame(self.root)
        self.success_frame.pack(padx=20, pady=20)
        # Add page UI
        title_label = ttk.Label(self.success_frame, text="Successfully buy a day pass!", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))
        day_pass_label = ttk.Label(self.success_frame, text="You already got a Day-Pass. Enjoy your trip!")
        day_pass_label.pack(pady=10)
        back_button = ttk.Button(self.success_frame, text="Buy", command=self.top_up)
        back_button.pack(pady=10)
        back_to_book_button = ttk.Button(self.success_frame, text="Back to Book a Bike", command=self.book_a_bike)
        back_to_book_button.pack(pady=10)
        # Change current frame
        self.current_frame = self.success_frame

    def book_a_bike(self):
        # Hide the currently displayed interface
        self.current_frame.pack_forget()

        # Toggle display of different sections
        def show_selected_section(section):
            if section == "Wallet":
                self.wallet_info(self.account_balance, self.security_balance)
            elif section == "Day_pass":
                self.day_pass()  # card_info()
            elif section == "History":
                self.show_history_page()
            elif section == "Change password":
                self.show_changepassword_page()  # TO_DO
            elif section == "Logout":
                self.show_main_window()  # TO_DO

        # We can add more sections as needed

        # section_var Variable tracking dropdown menu
        def on_section_select(*args):
            selected_section = section_var.get()
            show_selected_section(selected_section)

        self.book_frame = ttk.Frame(self.root)
        self.book_frame.pack(padx=20, pady=20)

        # Create a dropdown menu to select the section
        section_var = tk.StringVar()
        section_var.trace_add("write", on_section_select)  # Bind the callback function
        section_frame = ttk.Frame(self.book_frame)
        section_frame.pack(anchor="nw")
        section_var.set("Your Account")

        # Create a dropdown with the four options
        section_dropdown = tk.OptionMenu(section_frame, section_var, "Wallet", "History", "Logout")
        section_dropdown.pack(pady=10)
        # Title
        title_label = ttk.Label(self.book_frame, text="Book a Bike", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # create a frame for the location searching
        input_frame = ttk.Frame(self.book_frame)
        input_frame.pack(pady=10)

        # Text & input
        location_label = ttk.Label(input_frame, text="Your Location:", font=("Arial", 18))
        location_label.pack(pady=10)

        self.location_var = tk.StringVar()

        self.location_entry = ttk.Entry(input_frame, font=("Arial", 18), textvariable=self.location_var)
        self.location_entry.pack(side=tk.LEFT, padx=5)

        # Button
        find_bike_button = ttk.Button(self.book_frame, text="Find a Bike", command=self.update_address)
        find_bike_button.pack(pady=10)

        # We create a table to facilitate the output
        self.book_table = ttk.Treeview(self.book_frame, columns=("Location", "Battery", "Time Limit"))
        self.book_table.heading("#0", text="Vehicle ID")
        self.book_table.heading("#1", text="Vehicle Type")
        self.book_table.heading("#2", text="Battery Level")
        self.book_table.heading("#3", text="Time Limit")

        # Changes the width of the table by modifying the width.
        self.book_table.column("#0", width=100)
        self.book_table.column("#1", width=100)
        self.book_table.column("#2", width=100)
        self.book_table.column("#3", width=100)

        # Pack the table
        self.book_table.pack()

        # Button
        book_button = ttk.Button(self.book_frame, text="Book", command=self.book_status, width=20)
        book_button.pack(side="left", padx=(20, 40))

        # Button
        report_button = ttk.Button(self.book_frame, text="Report", command=self.show_report_page, width=20)
        report_button.pack(side="left", padx=(40, 20))

        # Change current frame
        self.current_frame = self.book_frame

    def end_ride(self):
        # Get selected vehicle
        selected_item = self.return_table.selection()
        if selected_item:
            # Extract the data from the selected item
            values = self.return_table.item(selected_item, "values")
            if values:
                location = self.return_table.item(selected_item, "text")  # Get the Vehicle ID (from the text column)
                print("Location: ", location)
                print("Parking zone type :", values[0])
                response = requests.post(f'{self.flask_app_url}/end_ride',
                                         json={'username': self.username, 'location': location, 'type': values[0]})
                if response.status_code == 200:
                    print("Ending ride at: ", location)
                    print(response.json())
                    self.account_balance = response.json()['acc_bal']
                    self.security_balance = response.json()['sec_bal']
                    self.show_feedback_page(response.json()['discount'], response.json()['fare'])
                else:
                    print("Could not end the ride")
        else:
            # Show message
            messagebox.showwarning("Warning", "Please select a location first!")
            return

    def book_status_page(self):
        # Preparation for later database connections.
        # Temporary
        global bike_status
        global time_left
        global battery
        # set default value
        bike_status = tk.StringVar()
        time_left = tk.StringVar()
        battery = tk.StringVar()
        bike_status.set("N/A")
        time_left.set("N/A")
        battery.set("N/A")

        # Hide the currently displayed interface
        self.current_frame.pack_forget()

        # Framework:
        # Basic Framework - current_frame
        self.current_frame = ttk.Frame(self.root)
        self.current_frame.pack(padx=20, pady=20)

        # Upper Part: Display Bike Status
        # Upper half: [basic information] and [discount]
        upper_frame = ttk.Frame(self.current_frame)
        upper_frame.pack(pady=(0, 20))

        # Create a frame for the left labels
        # left_frame = ttk.Frame(upper_frame)
        # left_frame.pack(side="left", padx=(0, 20))
        #
        # # PART1
        # # Create a frame for Bike Status Label and Value[basic information]
        # bike_status_frame = ttk.Frame(left_frame)
        # bike_status_frame.pack(side="top")
        # # Bike Status Label[basic information]
        # bike_status_label = ttk.Label(bike_status_frame, text="Bike Status:", font=("Arial", 12))
        # bike_status_label.pack(anchor="w", pady=(0, 10), side="left")
        # # Bike Status Value[basic information]
        # bike_status_value = ttk.Label(bike_status_frame, textvariable=bike_status, font=("Arial", 12))
        # bike_status_value.pack(pady=(0, 10), side="left")
        #
        # # PART2
        # # Create a frame for Time Left Label and Value[basic information]
        # time_left_frame = ttk.Frame(left_frame)
        # time_left_frame.pack(side="top")
        # # Time Left Label[basic information]
        # time_left_label = ttk.Label(time_left_frame, text="Time Left:", font=("Arial", 12))
        # time_left_label.pack(anchor="w", pady=(0, 10), side="left")
        # # Time Left Value[basic information]
        # time_left_value = ttk.Label(time_left_frame, textvariable=time_left, font=("Arial", 12))
        # time_left_value.pack(pady=(0, 10), side="left")
        #
        # # PART3
        # # Create a frame for Battery Label and Value[basic information]
        # battery_frame = ttk.Frame(left_frame)
        # battery_frame.pack(side="top")
        # # Battery Label[basic information]
        # battery_label = ttk.Label(battery_frame, text="Battery:", font=("Arial", 12))
        # battery_label.pack(anchor="w", pady=(0, 10), side="left")
        # # Battery Value[basic information]
        # battery_value = ttk.Label(battery_frame, textvariable=battery, font=("Arial", 12))
        # battery_value.pack(pady=(0, 10), side="left")
        #
        # # Create a frame for the right text [discount]
        # right_frame = ttk.Frame(upper_frame)
        # right_frame.pack(side="left")
        #
        # some_text = ttk.Label(right_frame, text="Discount![text]")
        # some_text.pack(side="right", padx=10)

        # Lower Part: Table and Return Button
        lower_frame = ttk.Frame(self.current_frame)
        lower_frame.pack(pady=20)

        # Create a table (Treeview) for location, charging point, distance, etc.
        self.return_table = ttk.Treeview(lower_frame, columns=("Charging Point", "Parking Available"))
        self.return_table.heading("#0", text="Location")
        self.return_table.heading("#1", text="Charging Point")
        self.return_table.heading("#2", text="Parking Available")

        location_names = ["Kelvingrove", "City Centre", "Argyle Street", "Baker Street", "Banner Road", "Essex Drive"]
        is_charging_available = ['yes', 'no', 'no', 'yes', 'no', 'yes']
        is_parking_available = ['yes', 'yes', 'yes', 'yes', 'yes', 'yes']

        for location_name, charging, parking in zip(location_names, is_charging_available, is_parking_available):
            self.return_table.insert("", "end", text=location_name, values=(charging, parking))

        self.return_table.column("#0", width=100)
        self.return_table.column("#1", width=100)
        self.return_table.column("#2", width=100)

        # Pack the table
        self.return_table.pack()

        # Create the Return button
        return_button_frame = ttk.Frame(lower_frame)
        return_button_frame.pack(side="top", fill="both", expand=True)
        return_button = ttk.Button(return_button_frame, text="Return", command=self.end_ride, width=20)
        return_button.pack(expand=True)

    def show_main_window(self):
        # Hide the "next window" frame
        self.current_frame.pack_forget()

        # Show the main window frame again
        self.main_window_frame.pack()

        self.current_frame = self.main_window_frame  # go back to main page after login

    def login(self):
        # get input
        self.username = self.username_entry.get()
        password = self.password_entry.get()
        # show in terminal
        print(f"Original username: '{self.username}', Stripped: '{self.username.strip()}'")
        print(f"Original password: '{password}', Stripped: '{password.strip()}'")
        if not self.username.strip() or not password.strip():
            messagebox.showerror("Error", "Please enter both username and a password.")
            return
        password = md5(self.password_entry.get().encode('utf-8')).hexdigest()

        # Make an HTTP POST request to the Flask app for user registration
        response = requests.post(f'{self.flask_app_url}/login', json={'username': self.username, 'password': password})

        if response.status_code == 200:
            # Set security and account balance
            self.account_balance = response.json()['acc_bal']
            self.security_balance = response.json()['sec_bal']
            # change status
            if response.json()['redirect'] == 'top-up':
                self.wallet_info(account_balance=response.json()['acc_bal'],
                                 security_balance=response.json()['sec_bal'])
                messagebox.showwarning("Warning", "Please amend your security deposit to £80.")
            else:
                self.book_a_bike()
            print("Login successful")

            # Add code to go to user profile
        else:
            print("Login failed")
            print(response.status_code)
        # Clear input
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def book_status(self):
        # Get selected item
        selected_item = self.book_table.selection()
        if selected_item:
            # Extract the data from the selected item
            values = self.book_table.item(selected_item, "values")
            if values:
                vehicle_id = self.book_table.item(selected_item, "text")  # Get the Vehicle ID (from the text column)
                print("Vehicle ID:", vehicle_id)
                print("Location:", values[0])
                print("Battery:", values[1])
                print("Time Limit:", values[2])
                response = requests.post(f'{self.flask_app_url}/book',
                                         json={'username': self.username, 'vehicle_id': vehicle_id, 'values': values})
                if response.status_code == 200:
                    print("Booking successful for vehicle:", vehicle_id)
                    print(response.json)
                    self.book_status_page()
                else:
                    print("Booking failed")
        else:
            # send message
            messagebox.showwarning("Warning", "Please select an item first!")
            return

    def update_address(self):
        # get location
        location = self.location_var.get()

        # Check if the location is empty or None
        if not location:
            messagebox.showerror("Error", "Please enter a location before booking.")
            return
        # Send data to server
        response = requests.post(f'{self.flask_app_url}/find_bike', json={'location': location})

        if response.status_code == 200:
            results = response.json()
            if results:
                print(results)
                self.update_search_results(results)
            else:
                messagebox.showerror("Error", "No results found for your search")
        else:
            messagebox.showerror("Error", "Unable to obtain data")

        self.location_var.set("")

    def update_search_results(self, results):
        print('Inside update search results')
        # Delete all rows while keeping column headers

        all_item_ids = self.book_table.get_children()

        # Loop through the list of item IDs and delete each item
        for item_id in all_item_ids:
            self.book_table.delete(item_id)
        bike_ids = results['bike_id']
        bike_types = results['bike_type']  # Use 'bike_type' instead of 'bike_id'
        battery_level = results['battery_level']  # Use 'battery_level' instead of 'bike_id'
        time_limits = results['time_limit']  # Use 'time_limit' instead of 'bike_id'

        for bike_id, bike_type, charge, time_limit in zip(bike_ids, bike_types, battery_level, time_limits):
            self.book_table.insert("", "end", text=bike_id, values=(bike_type, charge, time_limit))

        return

    def top_up(self):
        # Get data from server
        response = requests.post(f'{self.flask_app_url}/top_up',
                                 json={'amount': 100})  # Send the amount to be topped up.
        # Send message
        if response.status_code == 200:
            messagebox.showerror("Error", "Top-up failed. Please try again later.")
        else:
            messagebox.showinfo("Success", "Top-up successful!")

    def signup(self):
        # Get input
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
            self.username = username
            self.card_info()
        # print result
        elif response.status_code == 402:
            print('Password needs to be at least 8 characters and must contain at least one digit')
            tk.messagebox.showerror(
                message='Password should contain both letters and digit and should be at least 8 characters!')
        else:
            print("Registration failed")
            print(response.status_code)
            tk.messagebox.showerror(message='Username already exists!')
        # Clear input
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def show_changepassword_page(self):
        # Hide the main window frame
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
        back_button = ttk.Button(self.change_frame, text="Go Back", command=self.book_a_bike, width=10)
        back_button.pack(anchor=tk.NW, padx=10, pady=10)

        self.current_frame = self.change_frame

    def change(self):
        password = self.password_entry.get()
        if not password.strip():
            messagebox.showerror("Error", "Please enter password.")
            return
        password = md5(self.password_entry.get().encode('utf-8')).hexdigest()

        # Make an HTTP POST request to the Flask app for user registration
        response = requests.post(f'{self.flask_app_url}/signup', json={'password': password})

    def show_report_page(self):
        # Get selected item
        selected_item = self.book_table.selection()
        if selected_item:
            # Extract the data from the selected item
            location = self.book_table.item(selected_item, "text")
            values = self.book_table.item(selected_item, "values")

            # Hide the current frame
            self.current_frame.pack_forget()

            # Create report Frame
            self.report_frame = ttk.Frame(self.root)
            self.report_frame.pack(padx=20, pady=20)

            subject_label = ttk.Label(self.report_frame, text="Report Subject", font=("Arial", 24, "bold"))
            subject_label.pack(pady=(0, 20))

            # Create an input box for the report
            self.subject_input = tk.Text(self.report_frame, height=2, width=40, font=("Arial", 18))
            self.subject_input.pack(pady=10)

            # Create a title label
            title_label = ttk.Label(self.report_frame, text="Report", font=("Arial", 24, "bold"))
            title_label.pack(pady=(0, 20))

            # Create an input box for the report
            self.report_input = tk.Text(self.report_frame, height=7, width=40, font=("Arial", 18))
            self.report_input.pack(pady=10)

            # Create a submit button
            submit_button = ttk.Button(self.report_frame, text="Submit", command=self.submit_report, width=20)
            submit_button.pack(pady=20)

            # Create a back button
            back_button = ttk.Button(self.report_frame, text="Go Back", command=self.book_a_bike, width=20)
            back_button.pack(anchor=tk.NW, padx=10, pady=10)
            # change current frame
            self.current_frame = self.report_frame

        else:
            messagebox.showwarning("Warning", "Please select an item first!")
            return

    def submit_report(self):
        # Get content
        selected_item = self.book_table.selection()
        if selected_item:
            # Extract the data from the selected item
            vehicle_id = self.book_table.item(selected_item, "text")
            print(vehicle_id)
            report_content = self.report_input.get(1.0, tk.END).strip()
            subject_content = self.subject_input.get(1.0, tk.END).strip()
            print(report_content)
            if not report_content:
                messagebox.showerror("Error", "Please enter a report.")
                return

            vehicle_id = self.book_table.item(selected_item, "text")
            # Submit the report to the Flask server
            response = requests.post(f'{self.flask_app_url}/submit_report',
                                     json={'username': self.username, 'vehicle_id': vehicle_id,
                                           'subject': subject_content,
                                           'report': report_content})

            if response.status_code == 200:
                print("Report submitted successfully")
                self.book_a_bike()  # Returning to user page after submitting the report
            else:
                print("Report submission failed")
                print(response.status_code)
        else:
            messagebox.showwarning("Warning", "Please select an item first!")
            return

    def show_feedback_page(self, discount_applied, fare):
        # Hide the current frame
        self.current_frame.pack_forget()

        # Create feedback Frame
        self.feedback_frame = tk.Frame(self.root)
        self.feedback_frame.pack(padx=20, pady=20)

        # Create a title label
        title_label = tk.Label(self.feedback_frame, text="Thanks for using!", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        # Retrieve the data from the server

        discount = round(discount_applied, 2)
        total_price = round(fare, 2)
        wallet_balance = round(self.account_balance, 2)

        # Display retrieved data
        discount_label = tk.Label(self.feedback_frame, text=f"Discount: {discount}", font=("Arial", 18))
        discount_label.pack(pady=(0, 10))

        price_label = tk.Label(self.feedback_frame, text=f"Total Price: {total_price}", font=("Arial", 18))
        price_label.pack(pady=(0, 10))

        balance_label = tk.Label(self.feedback_frame, text=f"Wallet Balance: {wallet_balance}", font=("Arial", 18))
        balance_label.pack(pady=(0, 20))

        # Asking for user feedback
        ask_label = tk.Label(self.feedback_frame, text="How do you feel about this trip?", font=("Arial", 18))
        ask_label.pack()

        self.feedback_input = tk.Text(self.feedback_frame, height=5, width=50, font=("Arial", 18))
        self.feedback_input.pack(pady=10)

        # Create a submit button
        submit_button = tk.Button(self.feedback_frame, text="Submit", command=self.submit_feedback, font=("Arial", 18))
        submit_button.pack(pady=20)
        # Change current frame
        self.current_frame = self.feedback_frame

    def submit_feedback(self):
        # Get input
        feedback_content = self.feedback_input.get(1.0, tk.END).strip()
        if not feedback_content:
            messagebox.showerror("Error", "Please enter your feedback.")
            return

        # Submit the feedback to the Flask server
        response = requests.post(f'{self.flask_app_url}/submit_feedback',
                                 json={'username': self.username, 'sec_bal': self.security_balance,
                                       'feedback': feedback_content})

        if response.status_code == 200:
            print("Feedback submitted successfully")
            if response.json()['redirect'] == 'top-up':
                self.wallet_info(account_balance=self.account_balance,
                                 security_balance=response.json()['sec_bal'])
            else:
                self.book_a_bike()
        else:
            # Even if feedback submission fails, print the failure and continue to the main window
            print("Feedback submission failed")
            print(response.status_code)

        # Return to the main window regardless of feedback submission success or failure
        self.book_a_bike()

    def show_history_page(self):
        # Hide the current frame
        self.current_frame.pack_forget()

        # Create history Frame
        self.history_frame = ttk.Frame(self.root)
        self.history_frame.pack(padx=20, pady=20)

        # Create a title label
        title_label = ttk.Label(self.history_frame, text="Your Trip History:", font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 20))

        self.history_table = ttk.Treeview(self.history_frame, columns=("BikeID", "Time", "Time Price"))
        self.history_table.heading("#0", text="TripID")
        self.history_table.heading("#1", text="BikeID")
        self.history_table.heading("#2", text="Time")
        self.history_table.heading("#3", text="Price")

        # Retrieve the data from the server
        response = requests.post(f'{self.flask_app_url}/get_trip_history', json={'username': self.username})
        if response.status_code == 200:
            trip_data = response.json()
            print(trip_data)
            trip_ids = trip_data['TripID']
            bike_ids = trip_data['BikeID']
            time = trip_data['Time']
            price = trip_data['Price']

            for trip_id, bike_id, duration, fare in zip(trip_ids, bike_ids, time, price):
                self.history_table.insert("", "end", text=trip_id, values=(bike_id, duration, fare))
        else:
            print("Failed to retrieve trip history.")
            trip_data = []  # Empty list

        # Changes the width of the table by modifying the width.
        self.history_table.column("#0", width=100)
        self.history_table.column("#1", width=100)
        self.history_table.column("#2", width=100)
        self.history_table.column("#3", width=100)

        # Pack the table
        self.history_table.pack()

        # Create a back button
        back_button = ttk.Button(self.history_frame, text="Go Back", command=self.book_a_bike)
        back_button.pack(pady=20)
        # Change current frame
        self.current_frame = self.history_frame

    def confirm_order_page(self):
        # Hide the current frame
        self.current_frame.pack_forget()

        # Create confirm order Frame
        self.confirm_order_frame = ttk.Frame(self.root)
        self.confirm_order_frame.pack(padx=20, pady=20)

        # Retrieve the bike details from the server
        response = requests.get(f'{self.flask_app_url}/get_bike_details')
        if response.status_code == 200:
            bike_details = response.json()
        else:
            print("Failed to retrieve bike details.")
            bike_details = {
                "BikeID": "N/A",
                "Type": "N/A",
                "Battery": "N/A",
                "Time limit": "N/A"
            }  # Set default values to show N/A for unavailable data

        # Displaying bike details
        bike_label = ttk.Label(self.confirm_order_frame, text="The bike you chose:", font=("Arial", 18))
        bike_label.pack(pady=(0, 20))

        details_label = ttk.Label(self.confirm_order_frame, text=f"BikeID: {bike_details['BikeID']}\n"
                                                                 f"Type: {bike_details['Type']}\n"
                                                                 f"Battery: {bike_details['Battery']}\n"
                                                                 f"Time limit: {bike_details['Time limit']}",
                                  font=("Arial", 18))
        details_label.pack(pady=20)

        # Ask the user for confirmation
        confirm_label = ttk.Label(self.confirm_order_frame, text="Are you sure you want to book?", font=("Arial", 18))
        confirm_label.pack(pady=20)

        # Buttons for confirmation and cancellation
        self.button_frame = ttk.Frame(self.confirm_order_frame)
        self.button_frame.pack(pady=20)

        confirm_button = ttk.Button(self.button_frame, text="Confirm", command=self.book_status_page, width=20)
        confirm_button.pack(side=tk.LEFT, padx=20)

        cancel_button = ttk.Button(self.button_frame, text="Cancel", command=self.book_a_bike, width=20)
        cancel_button.pack(side=tk.LEFT, padx=20)

        self.current_frame = self.confirm_order_frame


def main():
    root = ThemedTk()
    root.set_theme('radiance')  # choose one from list
    available_themes = root.get_themes()
    print(available_themes)
    flask_app_url = 'http://localhost:5000'
    app = UserGUI(root, flask_app_url)
    root.mainloop()


if __name__ == "__main__":
    main()
