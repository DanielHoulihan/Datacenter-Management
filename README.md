Repository for UCD COMP30910 Final Year Project

Student Number: 18339866


Ensure Python 3.7 or higher is installed (older versions not tested)

```
cd webapp
```

There are three different ways to start the web application depending on your use case. 

Using docker:

```
docker compose build
docker compose up
```

Using a virtual environment (If you do not have adocker but still want the app contained)
Run the startup bash script which creates a python virtual environment.

```
source startup.sh
fab run
```

To run the application in debug mode (with command line output):

```
python3 manage.py runserver
```

Webapp is now available at http://localhost:8000


To stop the webapp run:
```
fab kill
```

To reset the webapp (including entire database) run:
```
fab reset
```