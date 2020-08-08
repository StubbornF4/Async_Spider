import pymongo

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students
student = {
    'id': '201701',
    'name': 'john',
    'age': '20',
    'gender': 'male',
}

student1 = {
    'id': '201701',
    'name': 'john',
    'age': '20',
    'gender': 'male',
}

student2 = {
    'id': '201701',
    'name': 'john',
    'age': 20,
    'gender': 'male',
}
student3 = {'a': 0}
results = collection.remove({'a': 0})
print(results)
