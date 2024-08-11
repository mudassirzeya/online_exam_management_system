# Online Exam Management System
 This project is an Online Exam Management System built with Django. It allows educational institutions to manage and conduct online exams efficiently. The app supports secure exam environments, automatic result generation, and integration with Google Sheets for easy management of students and exam questions.

# WebApp Images
Admin Interface:
![image](https://github.com/user-attachments/assets/e85c9814-43d1-467c-8970-c2f6d86ba384)
![image](https://github.com/user-attachments/assets/38d35b1d-22ec-4adc-9977-f52ba17184dc)
![image](https://github.com/user-attachments/assets/8383ee4a-0552-4c1a-8da1-89fa16968cde)
![image](https://github.com/user-attachments/assets/5bbe16dc-ef43-4769-ad14-54c42926f496)
![image](https://github.com/user-attachments/assets/39a64565-2d8e-462e-8b83-e2100f77a3ae)
![image](https://github.com/user-attachments/assets/3d3aaf6a-78e7-4086-9df4-273247af0ecc)
![image](https://github.com/user-attachments/assets/48532e60-98c6-4e4f-b281-bd52883ceb25)


Student Interface:
![image](https://github.com/user-attachments/assets/c2a57ac5-9f4b-4322-8a29-859f03abd29b)
![image](https://github.com/user-attachments/assets/47c7f93e-24c2-4dfa-a12f-267e2b52b87e)
![image](https://github.com/user-attachments/assets/6b03f737-e356-4247-8795-d81dc41219ff)











# Features
1) User Authentication: Organizations can create accounts and add teachers, who receive their credentials via email.
2) Exam Creation: Teachers or admins can create exams by specifying the exam name, duration, and details.
3) Google Sheets Integration: Easily import students and exam questions from Google Sheets using a provided template.
4) Student Management: Add students to exams, and they will receive login credentials via email.
5) Exam Environment:
   1. Students see a message if the exam hasn’t started or has ended, disabling access.
   2. During the exam, students are alerted if they try to switch tabs, preventing cheating.
   3. The platform records students via their webcam during the exam.
6) Automatic Submission: Exams are automatically submitted when time runs out, with a "Time’s up" message displayed.
7) Result Management: Teachers can instantly view and download exam results in CSV format after the exam ends.
8) Student Responses: View individual student responses for detailed analysis.

# Technologies Used
1) Backend: Django
2) Frontend: HTML, CSS, Bootstrap 4, JavaScript
3) Database: SQLite (default, can be changed)
4) Email Service: Django's Email backend (for sending passwords)
5) Google Sheets Integration: gspread and Google OAuth2

# Installation
1) Clone the Repository: git clone https://github.com/mudassirzeya/online_exam_management_system.git
2) Create a Virtual Environment (It's recommended to use a virtual environment to manage dependencies).
   1. python3 -m venv venv
   2. source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3) Install Dependencies
   1. pip install django
   2. pip install pillow
4) Configure the Database (By default, the app uses SQLite. You can configure another database in the settings.py file).
   1. python manage.py migrate
5) Set Up Email Backend
   1. Update the email configuration in the settings.py file to use your preferred email service for sending passwords.

6) Set Up Google Sheets Integration:
   1. open the sheet https://docs.google.com/spreadsheets/d/1gteH_Qkake4c28gxLcYCWp7NRKLyBbI7oH4sZOSDaqk/edit?gid=12029154#gid=12029154
   2. Extensions >> Apps Script >> Deploy >> New deployment >> select type: Wen app >> Deploye >> Copy URL
   3. add page=jsn in the end of the link you copied for adding questions.
   4. add page=user in the end of the link you copied for adding students.
7) Create Superuser (Admin Account): python manage.py createsuperuser
8) Run the Development Server: python manage.py runserver

# Usage
### For Schools/Coaching Centers:
  1. Sign up for a new account.
  2. Add teachers to the platform, who will receive their credentials via email.
  3. Teachers can log in and create exams, add students, and manage questions.
### Google Sheets Integration:
  1. Use the provided template link to add your own questions and students.
  2. Deploy the sheet and use the provided link to import data into the app.
### For Students:
  1. Log in with the credentials sent via email.
  2. View assigned exams. If the exam is active, enter the exam page and complete the exam.
  3. Stay on the exam page without switching tabs to avoid termination alerts.
### For Teachers/Admins:
  1. View exam results instantly after completion.
  2. Download results in CSV format and analyze individual student responses.

# Contributing
Contributions are welcome! Please submit a pull request or open an issue to contribute to this project.
      
