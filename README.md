# M14-Team-Project

## Name
E-Vehicle Share system

## Description
The application is designed to provide an accessible and seamless user experience while providing crucial tools for vehicle management and data analysis.

The project's objectives focus on the development of an application that facilitates customer ride booking, enables efficient vehicle tracking and management for operators, and equips managers with informative visualizations for better understanding trends in customer behaviour. Emphasis is placed on delivering these functionalities seamlessly and robustly, with a well-structured and documented codebase to support future expansion.
Informed by a review of contemporary solutions, the resulting prototype not only meets the minimum viable product (MVP) requirements but also lays the foundation for scalability and enhanced functionality. Rigorous testing and an adherence to industry best practices ensures a seamless experience for all users.

## Installation
Install the packages mentioned in requirements.txt . If you are using pycharms it can directly install all the packages from requirements.txt for you.

## Usage
We have 3 different GUIs for 3 different types of users:

1. Customers: For customers we have the UserGUI.py file. To access user functionalities you will need to run this file.
2. Operators: For operators we have the OperatorGUI.py file. To access operator functionalities you will need to run this file.
3. Manager: For managers we have the ManagerGUI.py file. To access manager functionalities you will need to run this file.

These files can be found in tkinter_ui folder.

Before running these files make sure you keep running app.py file in background. This is the flask file and is responsible for routing UI requests to appropriate backend functionalities.

We have tried our best to handle all the exceptions, but in case the app.py or any of the UI files encounter an error or exception you will have to restart them to continue working.

The idea behind having 3 different GUIs is similar to having multiple applications for different types of users, which is done in most ride sharing systems.

We have already uploaded the sqlitedb in our codebase so that its easier for you to run the application and have better reports for managers. However if you want to restart the db you will have to do so by running db_populate.py and db_initialise.py scripts under databse folder.

## UserGUI Guide
<img src="https://stgit.dcs.gla.ac.uk/programming-and-systems-development-m/2023/lc01-m14/m14-team-project/-/blob/develop/Images/BookRide.png" align="center" height="150" width="150"/>

To book a ride , enter the one of the available locations and click on find a bike to get a list of vehicles at that location.
Select the bike you want to book and click on book button.

The available locations are:

1. Kelvingrove
2. City Centre
3. Argyle Street
4. Baker Street
5. Banner Road
6. Essex Drive

<img src="https://stgit.dcs.gla.ac.uk/programming-and-systems-development-m/2023/lc01-m14/m14-team-project/-/blob/develop/Images/Return%20Ride.png" align="center" height="150" width="150"/>

To end the ride select a location and clicke on return button.
If you fail to end the ride in the time limit of the vehicle it will be automatically ended by the system.

<img src="https://stgit.dcs.gla.ac.uk/programming-and-systems-development-m/2023/lc01-m14/m14-team-project/-/blob/develop/Images/End%20Auto.png" align="center" height="150" width="150"/>

## OperatorGUI Guide
<img src="https://stgit.dcs.gla.ac.uk/programming-and-systems-development-m/2023/lc01-m14/m14-team-project/-/blob/develop/Images/Operator%20Interface.png" align="center" height="150" width="150"/>

The operator can see all the vehicles in this page once its opened. To filter according to specific criterias we have provided radio buttons. For example to search for vehicles with low battery at a specific location, select respective radio buttons and enter the desired location.

To see defect reports click on your account menu and navigate to reports.
## ManagerGUI Guide
<img src="https://stgit.dcs.gla.ac.uk/programming-and-systems-development-m/2023/lc01-m14/m14-team-project/-/blob/develop/Images/Manager.png" align="center" height="150" width="150"/>

To see the manager reports select the date using the drop down calendar. We suggest selecting 1st November 2023 as that is the date with most data. Select an appropriate end date and use the drop down to select the type of report you want to see.
## Support
In case of any queries please refer the application vide or feel free to reach us on teams.

## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request

## Authors and acknowledgment
Yash Gupte
Ritajit Dey
Min Ma
Ruizhi Li
"# Ebike-App" 
