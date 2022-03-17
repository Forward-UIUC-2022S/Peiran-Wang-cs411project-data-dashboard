# Sample Project
### About
This project is built to help student find thire research paper's directions and resources by dash plotly. 
### Setup
- Start MySQL sever and Neo4j server
- install virtualenv by ```pip install virtualenv```
- Run ``` virtualenv venv``` and ``` source venv/bin/activate ```
- install required packeges
```
pip install dash
pip install pandas
pip install sqlalchemy
pip install pymysql
pip install neo4j
pip install pymongo
```
- Run ```python app.py ``` to start the app
- Open dashboard in a browser using http://127.0.0.1:8050/
### Design
- ```app.py``` contains codes to build up the dashboard application
- ```layout.css``` in packege ```assets``` contains codes to adjust position of each components and to implement basic UI design like color and font
- ```mysql.py```, ```myneo4j.py```, ```mymongodb.py``` contain code to connect
and get data from database
### Demo Video
https://www.youtube.com/watch?v=tkZ9lEiSRfQ

# Sample Layout
### About
Provide basic implementation of layout for final project. See comments in CSS file to know how to adjust.  
