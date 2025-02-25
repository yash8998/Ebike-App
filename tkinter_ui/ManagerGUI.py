# This is for creating manager interface

import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Frame

from ttkthemes import ThemedTk
from PIL import ImageTk, Image
from hashlib import md5
import requests
from tkinter import messagebox, StringVar
from tkcalendar import DateEntry


class managerGUI:

    def __init__(self, root, flask_app_url):
        self.report_img_label = None
        self.report_img = None
        self.root = root
        self.root.title('manager page')
        self.root.geometry('700x700')
        self.root.resizable(width=True, height=True)
        # Added an icon
        self.root.iconbitmap('../Images/icon.ico')

        # Flask app URL
        self.flask_app_url = flask_app_url

        self.main_window_frame = None
        self.login_frame = None
        self.manager_window_frame = None

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

        self.current_frame = self.login_frame

    def login(self):
        # add input field
        username = self.username_entry.get()
        password = self.password_entry.get()
        # check input
        if not username.strip() or not password.strip():
            messagebox.showerror("Error", "Please enter both username and a password.")
            return

        # Make an HTTP POST request to the Flask app for user registration
        response = requests.post(f'{self.flask_app_url}/manager_login', json={'username': username, 'password': password})

        if response.status_code == 200:
            print("Login successful")
            self.show_manager_interface()
            # Add code to go to user profile
        else:
            print("Login failed")
        # show interface

        # Clear input
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def search_manager_data(self):
        # get content
        from_date = self.from_date_entry.get()
        to_date = self.to_date_entry.get()
        choice = self.chart_dropdown.get()
        # send to servers
        response = requests.post(f'{self.flask_app_url}/search_manager_report',
                                 json={'from_date': from_date, 'to_date': to_date, 'choice': choice})

        if response.status_code == 200:
            # get results
            results = response.json()
            if results:
                # Clear the previous image if it exists
                if self.report_img is not None:
                    self.report_img_label.grid_forget()  # Remove the label from the grid
                    self.report_img_label.destroy()  # Destroy the label widget
                    del self.report_img  # Delete the reference to the previous image

                self.report_img = ImageTk.PhotoImage(Image.open(results['image_url']))
                self.report_img_label = ttk.Label(self.manager_window_frame, image=self.report_img)
                self.report_img_label.configure(image=self.report_img)
                self.report_img_label.image = self.report_img
                self.report_img_label.grid(row=3, column=0, columnspan=2, pady=10)

            else:
                messagebox.showerror("Error", "No results found for your search.")
        else:
            messagebox.showerror("Error", "Failed to retrieve search results. Please try again.")

    # def show_downloaded_image(self, image_path):
    #     # load and show page
    #     img = ImageTk.PhotoImage(Image.open(image_path))
    #     if hasattr(self, 'downloaded_img_label'):
    #         # update if exist
    #         self.downloaded_img_label.configure(image=img)
    #         self.downloaded_img_label.image = img
    #     else:
    #         # first time
    #         self.downloaded_img_label = ttk.Label(self.manager_window_frame, image=img)
    #         self.downloaded_img_label.image = img
    #         self.downloaded_img_label.grid(row=3, column=0, columnspan=2, pady=10)

    def show_manager_interface(self):
        # Hide the current frame
        if self.current_frame:
            self.current_frame.pack_forget()

        # Create a frame to place contents of the manager page
        self.manager_window_frame = ttk.Frame(self.root)
        self.manager_window_frame.pack(padx=20, pady=20)
        # set title
        title_label = ttk.Label(self.manager_window_frame, text="Manager Page", font=("Arial", 15, "bold"))
        title_label.grid(row=0, column=0, pady=10, columnspan=2)

        # Date picker for "From" and "To" date range
        date_frame = ttk.Frame(self.manager_window_frame)
        date_frame.grid(row=1, column=0, pady=10, sticky=tk.W)

        from_label = ttk.Label(date_frame, text="From")
        from_label.pack(side=tk.LEFT, padx=5)

        self.from_date_entry = DateEntry(date_frame, date_pattern='y-mm-dd', width=10)  # Date entry for "From"
        self.from_date_entry.pack(side=tk.LEFT, padx=5)

        to_label = ttk.Label(date_frame, text="To")
        to_label.pack(side=tk.LEFT, padx=5)

        self.to_date_entry = DateEntry(date_frame, date_pattern='y-mm-dd', width=10)  # Date entry for "To"
        self.to_date_entry.pack(side=tk.LEFT, padx=5)

        # Drop-down menu for selecting the type of visualization chart/report
        chart_frame = ttk.Frame(self.manager_window_frame)
        chart_frame.grid(row=1, column=1, pady=10, sticky=tk.E)

        self.chart_options = ["Histogram ride duration", "Confusion matrix popular paths", "Revenue vs location",
                              "Time to close complaint histogram"]
        self.chart_dropdown = ttk.Combobox(chart_frame, values=self.chart_options, width=25)
        self.chart_dropdown.set(self.chart_options[0])  # Set default value
        self.chart_dropdown.pack(side=tk.LEFT, padx=5)

        search_button = ttk.Button(chart_frame, text="Search", command=self.search_manager_data)
        search_button.pack(side=tk.LEFT, padx=5)

        # change current frame
        self.current_frame = self.manager_window_frame
        self.from_date_entry.focus_set()


def main():
    root = ThemedTk()
    root.set_theme('radiance')  # choose one from list
    available_themes = root.get_themes()
    print(available_themes)
    flask_app_url = 'http://localhost:5000'
    app = managerGUI(root, flask_app_url)
    root.mainloop()


if __name__ == "__main__":
    main()
