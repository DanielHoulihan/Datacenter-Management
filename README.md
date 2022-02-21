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

---

There are 4 different pages in the app

1. Home 
- Shows some basic information about your selected datacenter(s) and allows you to select a configured data center after which you can view it's assets (and budget eventually)

2. Assets
- Will show the floors/ racks/ hosts of your selected data center. Once you've configured a data center properly you will also be able to see metrics relating to energy usage. The first time you view your hosts the calculations need to be made so this make take a while. Next time you click in the new information is appended - so it will be much quicker. 

3. Budget - TODO

4. Configure 
- You can change the IP Address of the master (default is localhost)
- Using the data centers available on this master, you can select one to configure. Here you can choose PUE, carbon conversion, energy cost as well as a start date (end date is the present time so it will update automatically when you check up on your hosts)
- Now that you have your configured data center you can go back to 'Home' and select one, and then view your assets. 
- You can delete configured data centers here using 'delete' button.
- ** Not all error handling has been completed so in some cases illegal input will show a broken page - just click back and try again. **

Notes:
- The appearance of the webapp will be updated once all the backend is completed.
- Code may be a little messy / lack of comments. This will also be tidied up in the near future.