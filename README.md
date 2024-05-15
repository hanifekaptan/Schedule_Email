# Scheduled_Email
The application, developed using Python, PyQt5 and PyQt Designer, ensures that a letter written with a future date is delivered to the target person via Gmail on the relevant date. This application aims to easily handle memories that you want to remember in the future, prospective messages or planned e-mail transactions. The informatin is kept in the PostgreSQL database to be read again on the target date specified by the user. The user can change them manually, but it is not recommendend to do so.

Shortcomings and weaknesses:
1. The application runs on a server and connected to the database, but the current situation the application is not connected to a server.
2. The user is responsible for making the database.
3. The codes responsible for creating the database and tables required for PostgreSQL are located in the BeforeMain.py file.

Main Page:  
![image](https://github.com/hnfkptn/Scheduled_Email/assets/129584767/1dae6558-4177-4c48-8fbb-447b1ed5a879)

Settings Page:  
![image-1](https://github.com/hnfkptn/Scheduled_Email/assets/129584767/bebfecc6-d7f2-4d36-9381-198f1c540a24)

Delete Person Page:  
![image-2](https://github.com/hnfkptn/Scheduled_Email/assets/129584767/63d072c5-3466-481e-9fbc-d9f283a2b38b)

Insert Person Page:  
![image-3](https://github.com/hnfkptn/Scheduled_Email/assets/129584767/81a37235-58c6-4680-aac2-ad66ff33be1b)

Send Letter Page:  
![image-4](https://github.com/hnfkptn/Scheduled_Email/assets/129584767/2af3093b-a376-476e-84fa-0c5ab7023ff4)

