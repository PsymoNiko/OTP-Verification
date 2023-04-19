<h1>OTP Authenticator</h1>

<h3>1-Create a virtual environment</h3>

To create a venv you need to type this code in your terminal:

    python -m venv venv
or

    python3 -m venv venv

After that you have to activate your venv by:

on linux:

    source venv/bin/activate

on windows:
    
    venv/Scripts/activate


<h3>2-Installing requirements</h3>

First of all install all the requirements:

    pip install -r requirements.txt

<h3>3-Take an API-KEY</h3>

To take an api-key, you need to register in sms.ir website from the link blow

https://sms.ir/

Then go to the "برنامه نویسان" and click on the "ساخت توکن جدید"

<h3>4-Making an Environment Variable</h3>

Open a new terminal ("be careful your venv must be deactivated")
then type this:

    export SMS_ENV="YOUR API-KEY"

instead of "YOUR API-KEY" you need to copy your api-key which was taken from the sms.ir website

Then to check that your API-KEY was saved or not run this:

    printenv SMS_ENV

<h3>5-Installation docker and run redis</h3>

To install docker on you linux type:

    sudo apt install docker.io

Then install redis on your docker:

    sudo docker pull redis

Finally, run you redis on port 6379:

    sudo docker run --name <name> -d redis

(By default redis coming up on port 6379, so you don't need to set a port)


<h3>6-Run the project and its celery</h3>

Back to your terminal with an activated venv

First:

    python manage.py migrate

Second:

    python manage.py runserver

Third:
open a new terminal and be sure you venv is activated:

    celery -A api.tasks worker -l info

-------------------------------------------------------

<h2>Sending OTP SMS</h2>

1) Open your browser and type:
    
http://127.0.0.1:8000/login/

2) Type:


    {"phone_number": "<write_your_phone_number>"}

3) Then going to this url and wait for a 6-digits code

http://127.0.0.1:8000/verify/

4) Now put that OTP code in this format and then POST it:


    {
        "phone_number": "<your_phone_number>",
        "otp": "<your_OTP_code>"
    }

# Congratulation
YOUR WERE REGISTERED ON THE SITE(user) 

<h1>Installing Docker and Pulling PostgreSQL Image</h1>
This guide will walk you through the steps to install Docker and pull the PostgreSQL image from the official Docker Hub repository.

# Prerequisites
Before you begin, make sure your system meets the following requirements:

Ubuntu 16.04 or later, macOS 10.14 or later, or Windows 10 Pro or Enterprise (64-bit) version 1809 or later
A Docker Hub account (you can sign up for free at hub.docker.com)
Internet connection
Installing Docker
# Ubuntu

    
    sudo apt-get update
    sudo apt-get install docker.io

# macOS
To install Docker on macOS, download and run the 
    https://www.docker.com/products/docker-desktop/

# Windows
To install Docker on Windows, download and run the
    https://www.docker.com/products/docker-desktop/


<h3>Pulling the PostgreSQL Image</h3>
Once Docker is installed, you can pull the PostgreSQL image from the Docker Hub repository by running the following command:

    docker pull postgres


<h3>Running PostgreSQL</h3>
To run the PostgreSQL image, use the following command:

    docker run --name <some-postgres> -e POSTGRES_PASSWORD=<mysecretpassword> -p <YourPort>:5432 -d postgres

# At the end:
Create a <.env> file next to your settings.py and fill it like the .env.sample with your API_KEY, SECRET_KEY, PSQL_PORT and PSQL_PASSWORD

# Then:
    
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver