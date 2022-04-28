## Repository for UCD COMP30910 

## Final Year Project

## Student Number: 18339866

---

### 3 minute demonstration
Short demonstration of web application because you need to be on the same network as a datacenter to use any of the features:

https://drive.google.com/file/d/1Ki3sNgRQNWIsZqvzZYCo3Nslu1Wu_WTN/view?usp=sharing

---

### Instructions for running:

Ensure Python 3.7 or higher is installed (older versions not tested)

Naviagte to the 'webapp' directory 
```
cd webapp
```

There are three different ways to start the web application depending on your use case. 

Using docker:

```
docker compose build
docker compose up
```

Using a virtual environment (If you do not have docker but still want the app contained)
Run the startup bash script which creates a python virtual environment.

```
source startup.sh
fab run
```

To run the application in debug mode:
This will install python libraries globally (not recommended)

```
pip3 install -r requirements.txt
python3 manage.py runserver
```


Web application is now available at http://localhost:8000