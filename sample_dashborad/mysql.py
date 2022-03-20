from warnings import catch_warnings
from numpy import character
import sqlalchemy as sql
from sqlalchemy.sql import text
import pandas as pd
import numpy as np


db_connection_str = 'mysql+pymysql://username:password@localhost:3306/AcademicWorld' #connect your loacal sql by your password and name
db_connection = sql.create_engine(db_connection_str)

def getTop5Professor():
    sql = "SELECT f.name, f.position, p.title, f.research_interest, f.photo_url, u.name FROM publication p JOIN faculty_publication fp on fp.publication_id = p.id JOIN faculty f on fp.faculty_id = f.id JOIN university u on f.university_id = u.id ORDER BY num_citations DESC LIMIT 5;"
    data = db_connection.execute(text(sql)).fetchall();
    data2 = [list(i) for i in data]
    return data2

def getTop5Areas():
    sql = "SELECT name, count FROM keyword JOIN (SELECT keyword_id, COUNT(keyword_id) as count FROM publication_keyword GROUP BY keyword_id ORDER BY COUNT(keyword_id) DESC LIMIT 5) temp ON id = temp.keyword_id;"
    data = db_connection.execute(text(sql)).fetchall();
    return data

def getTop5Article(keyword_name):
    sql = "SELECT title, num_citations FROM keyword f JOIN publication_keyword pk on f.id = pk.keyword_id JOIN publication p ON pk.publication_id = p.id WHERE f.name = :x ORDER BY num_citations DESC LIMIT 5;"
    data = db_connection.execute(text(sql), {'x': keyword_name}).fetchall()
    return data

def getPopularArticle():
    top5Areas = getTop5Areas()
    info = []
    character = [i[0] for i in top5Areas]
    parent = ["", "", "", "", ""]
    value = [i[1] for i in top5Areas]
    for i in top5Areas:
        area = i[0]
        article = getTop5Article(area)
        info.append(article)
        for j in article:
            character.append(j[0])
            parent.append(i[0])
            value.append(j[1])
    return character, parent, value

def insertCitaion(titleName):
    sql1 = "SELECT p.id FROM publication p WHERE title = :x;"
    data = db_connection.execute(text(sql1), {'x': titleName}).fetchall()
    if(len(data) == 0):
        return []
    try:
        sql2 = "INSERT INTO CitationList VALUES (:y);"
        db_connection.execute(text(sql2), {'y': data[0][0]})
    except:
        return [0]
    else:
        return data

def createTable():
    sql0 = "DROP TABLE IF EXISTS CitationList;"
    db_connection.execute(text(sql0))
    sql = "CREATE TABLE CitationList ( publication_id int primary key );"
    db_connection.execute(text(sql))

def getCitationList():
    sql = "SELECT title, name, year, num_citations FROM publication p JOIN CitationList c on p.id = c.publication_id JOIN faculty_publication fp ON p.id = fp.publication_id JOIN faculty f ON f.id = fp.faculty_id;"
    data = db_connection.execute(text(sql)).fetchall()
    data2 = [list(i) for i in data]
    data3 = list(map(list, zip(*data2)))
    return data3

def getTrend(topic_name):
    sql = "SELECT year, count(id) FROM (SELECT p.id, year, keyword_id FROM publication p JOIN publication_keyword pk ON p.id = pk.publication_id JOIN keyword k on pk.keyword_id = k.id WHERE k.name = :x) temp GROUP BY year ORDER BY year;"
    data = db_connection.execute(text(sql), {'x': topic_name}).fetchall()
    year = [i[0] for i in data]
    num = [i[1] for i in data]
    return year, num

def removeCitationList():
    if (getCitationList() == []):
        return;
    titles = getCitationList()[0]
    for j in titles:
        str = "UPDATE publication SET num_citations = num_Citations + 1 WHERE title = :x";
        db_connection.execute(text(str), {"x":j})
    sql = 'DELETE FROM CitationList;'
    db_connection.execute(text(sql))
    return;
