from neo4j import GraphDatabase
class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response

def getArticleInArea(area):
    conn =  Neo4jConnection(uri="bolt://localhost:7687", user="neo4j", pwd="123456")
    qurrstring = f"MATCH (a:PUBLICATION) -[r:LABEL_BY] - (k:KEYWORD) WHERE k.name = \"{area}\" RETURN a as article ORDER BY a.numCitations DESC"
    data = list(conn.query(qurrstring,db='academicworld'))
    properties = [record['article']._properties for record in data]
    data2 = {key: [i[key] for i in properties] for key in properties[0]}
    title = ['title', 'venue', 'year', 'numCitations']
    data3 = [data2[i] for i in title]
    return data3

getArticleInArea('deep learning')









