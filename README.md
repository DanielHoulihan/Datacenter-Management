Repository for UCD COMP30910 Final Year Project

Student Number: 18339866


Ensure Python 3.7 or higher is installed (older versions not tested)

```
cd webapp
```

Run the startup bash script which creates a python virtual environment.

```
source startup.sh
```

All required libraries are now installed and the virtual environment is activated.

To start the webapp run:
```
fab run
```

To stop the webapp run:
```
fab kill
```

To reset the webapp (including entire database) run:
```
fab reset
```