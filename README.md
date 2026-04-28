# Lunar Birthday Reminder
This app generate ics file for lunar calender. 

<img width="1654" height="686" alt="image" src="https://github.com/user-attachments/assets/167bf818-ab86-4ddc-bfcd-5eceb9c693e9" />


# How to use locally
You can use setup.bat in windows to install the virtual environment. 

    cd lunar_birthday_config
    python manage.py runserver
    
Open your browser and navigate to http://127.0.0.1:8000/

# How to deploy
    docker build -t alvinchan2004/lunar-birthday-reminder:1.1 .

# How to run in docker
    docker run -p 9000:9000 alvinchan2004/lunar-birthday-reminder:1.0
