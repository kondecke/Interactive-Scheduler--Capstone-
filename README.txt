This file will describe how to download files and run the backend server and frontend server 
which is located at https://github.com/kmill227/InteractiveSchedulerFrontend.

Backend Server
1. Install python (download from online resources)
2. Create a repository and make sure you know how to get to it.
3. Clone the github in the repository you made using the command in terminal "git clone https://github.com/kmill227/Interactive-Scheduler--Capstone-"
4. Navigate to repo location and in terminal run command "python -m venv venv" for virtual environment. Not 100% needed but recommended.
5. Run command in terminal again ".\\venv\scripts\activate"
6. Install Django modules running command "python -m pip install django"
7. Run commands to create site directory "django-admin startproject mysite"
8. Change directory into mysite folder (should see manage.py if run command "ls")
9. Run command in terminal inside mysite directory "python manage.py startapp scheduler"
10. Start django local server in mysite directory by running terminal command "python manage.py runserver"
11. Backend server should be running. Make sure to run on port 8000.
