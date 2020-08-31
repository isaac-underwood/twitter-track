from flask import Flask, render_template, jsonify
import twint
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = PyMongo(app)
tc = twint.Config()


# Loads home page
@app.route('/')
def index():
    return render_template('index.html')


# GET ROUTE - Get the graph page
# POST ROUTE - Queried word/news outlet
@app.route('/graph')
def graph():
    return render_template('graph.html')


# API ROUTES

# Username Routes (for getting tweets via username)

@app.route('/api/username/<string:username>', methods=['GET'])
def getTweetsByTimeline(username):
    # Find tweets by username
    tweets_by_user = mongo.db.test.find({"username": username})
    tweets_by_user_json = dumps(tweets_by_user)  # Convert to json
    if tweets_by_user_json == '[]':  # Check if no tweets were found
        return tweets_by_user_json, 404  # Return a 404 and empty json
    return tweets_by_user_json, 200  # Return a success and tweets by username


# Generic Search Routes

# Returns all tweets in the database
@app.route('/api/generic/', methods=['GET'])
def getAllTweets():
    all_tweets = mongo.db.test.find()  # Retrieve all objects in database
    all_tweets_json = dumps(all_tweets)
    if all_tweets_json == '[]':
        return all_tweets_json, 404
    return all_tweets_json, 200

# Accepts a keyword (search term) to search all tweets
@app.route('/api/generic/<string:keyword>')
def twintGenericSearch(keyword):
    tc.Search = keyword  # Set search term in config
    twint.run.Search(tc)


if __name__ == '__main__':
    app.run(debug=True)
