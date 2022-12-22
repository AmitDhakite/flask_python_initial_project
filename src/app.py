from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)


from pymongo import MongoClient

client = MongoClient('mongodb+srv://amit:123@cluster0.immwx.mongodb.net/?retryWrites=true&w=majority')
db = client.get_database('python_project')
users = db.users

CORS(app)



@app.route("/")
def index():
    return 'Hello World!!!'

@app.route("/addUser", methods = ["POST"])
def createUser():
    # print(request.json['name'])
    # return "OK"
    id = users.insert_one({
        'name': request.json['name'],
        'email': request.json['email'],
        'contact': request.json['contact'],
        'address': request.json['address']   
    })
    return jsonify({'id': str(id.inserted_id), 'msg': 'User Added Successfully'})

@app.route("/getUsers", methods = ["GET"])
def getUsers():
    allUsers = users.find()
    users_list = []
    for user in allUsers:
        users_list.append({
            'id': str(user['_id']),
            'name': str(user['name']),
            'email': str(user['email']),
            'contact': str(user['contact']),
            'address': str(user['address']),
        })
    return jsonify(users_list)

@app.route('/getUser/<id>', methods = ["GET"])
def getUser(id):
    foundData = users.find_one({'_id': ObjectId(id)})
    foundUser = {
        'id': str(foundData['_id']),
        'name': str(foundData['name']),
        'email': str(foundData['email']),
        'contact': str(foundData['contact']),
        'address': str(foundData['address']),
    }
    return jsonify(foundUser)

@app.route('/deleteUser/<id>', methods=["DELETE"])
def deleteUser(id):
    db.users.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg': 'User deleted successfully!!'})

@app.route('/updateUser/<id>', methods=["PUT"])
def updateUser(id):
    users.update_one({'_id': ObjectId(id)}, {'$set': {
        'name': request.json['name'],
        'email': request.json['email'],
        'contact': request.json['contact'],
        'address': request.json['address']   
    }})
    return jsonify({'msg': 'User updated successfully!!'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')    