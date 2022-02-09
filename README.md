Repository for UCD COMP30910 Final Year Project
Student Number: 18339866
---

To run dummy API from reports json:

```
npm install -g json-server
json-server --watch 3c940024-2e13-4dc6-aa2d-b17711f5fba5.json --port 3002
```
This is now visible at http://localhost:3002/reports

---

To run webapp using Django:

Install required packages
```
pip3 install -r requirements.txt
```

```
cd webapp
python3 migrate.py runserver
```

Web app is now accessible at http://localhost:8000/tool