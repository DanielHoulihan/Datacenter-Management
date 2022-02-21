Repository for UCD COMP30910 Final Year Project
Student Number: 18339866

To run webapp using Django:

Ensure Python 3.7 or higher is installed (may work with older versions but have not tested yet)


```
cd webapp
```

Install required packages (in Linux it may be pip instead of pip3 - depends on distro)
```
pip3 install -r requirements.txt
```

```
cd webapp
python3 manage.py runserver
```

Web app is now accessible at http://localhost:8000/tool

If you want to reset the database (there will be a buttons to delete certain items in the future) simply delete the file /webapp/db.sqlite3 and run the following commands:

```
python3 manage.py makemigrations
python3 manage.py migrate
```

You can now use this command to start the web app again
```
python3 manage.py runserver
```