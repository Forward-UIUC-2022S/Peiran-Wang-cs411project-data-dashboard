from pymongo import MongoClient

def getArticleByName(name):
  client = MongoClient("mongodb://127.0.0.1:27017")
  db=client.academicworld
  command = db.faculty.find({"name": name}, {"_id":0, "publications": 1}).limit(5)
  publicationsInfo = list(command)[0]["publications"]
  allInfo = []
  for i in publicationsInfo:
    allInfo.append(list(db.publications.find({"id":i}, {"_id":0, "title":1, "venue":1, "year":1, "numCitations": 1})))
  data2 = [list(i[0].values()) for i in allInfo]
  data3 = list(map(list, zip(*data2)))
  return data3
