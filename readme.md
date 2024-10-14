# Developed in Windows. These are the Requirements:
- docker

# Quick Start
`git clone https://github.com/chiathepanda/coding_interview.git

in the folder coding_interview

`docker-compose build --no-cache
`docker-compose up

backend: accessible via http://localhost:8000
frontend: accessible via http://localhost:3000
___

# Requirements for development:
- MySQL server (Create a database called `astekproject`)
- python 3.12
- pipenv
- node

A requirements.txt was generated through `pipenv requirements > requirements.txt`. </br>
pipenv was activated in the same folder as manage.py `pipenv install` will install and create a virtual enviroment </br>
Run the following : </br>
> cd myproject </br>
> pipenv install 

`pipenv install
cd .\backend\
`python manage.py makemigrations
`python manage.py migrate

`python manage.py populate_db

cd backend
`python manage.py runserver

client side: 
`npm run dev

# Assumptions
- Employee ID are all uppercase
- I added created_at updated_at for the models
- On the last page of the problem statement: Location [Reusable Textbox]
so, I did not use latitude and longitude for location. (could have implemented onto the model with django's django.contrib.gis.db)
- npm create vite@latest client --template react
- For GET endpoint /employees?cafe=<café>
    - the email_address in the instruction was duplicated, i only returned 1 email_address
    - gender is returned
    - both cafe's id and name is returned instead of just name, so that I could relate it by id instead of name by cafe
male/female is lowercase in the database

# Extra Notes
serving files from media root instead of cloudservice or CDN

This is the key-value for how employee is releated to cafe
"cafe_relation": {
    "cafe_id": "8b285725-aa78-4990-8751-179640bf1945",
    "start_date": "2024-10-10"
}

# References:
https://mui.com/material-ui/getting-started/templates/
https://ant.design/docs/react/introduce
https://www.ag-grid.com/react-data-grid/getting-started/
https://formik.org/docs/overview

https://hub.docker.com/_/python/


comment out in astek/backend/docker.sh If you don't want the dummy data
python manage.py populate_db

Try running Docker desktop as admin and Make sure Mysql service isn't running on port 3306

change the .env.production file
docker-compose build --no-cache
docker-compose up --abort-on-container-



Error: open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified.
Close Docker Desktop
Open cmd and run wsl --shutdown
Start Docker Desktop and press Restart on the notification below
(It should pop up in a few seconds)

Error Only one usage of each socket address (protocol/network address/port) is normally permitted.
If the port was 3306, you need to stop the Mysql service


# for development:
set DJANGO_ENV=development