from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb+srv://vishu842301:vishu842301@cluster0.zrz66q0.mongodb.net/test?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route("/")
def home():
    collection = mongo.db.inventory
    collection.insert_one({"name": 'karan'})
    return "Home Page"

if __name__ == "__main__":
    app.run(debug=True, port=8000)
