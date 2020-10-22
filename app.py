from flask import Flask, render_template, jsonify
import twint
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.json_util import dumps
import datetime
from frequencies import Frequency

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/test"
mongo = MongoClient()
tc = twint.Config()


# Loads home page
@app.route('/')
def index():
    return render_template('index.html')


# GET ROUTE - Get the graph page
# POST ROUTE - Queried word/news outlet
@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST':
        granularity = request.form['aggregate']  # Granularity must be passed in as value from 0-3
        username = request.form['news']
        search_keyword = request.form['search']
        date_from = request.form['start']
        date_until = request.form['end']
        graph = request.form['graph']

        results = getTweetSearchWithDates(username, search_keyword,
                                          granularity, dfrom, dto)
        if granularity == "1":
            return render_template('graph_month.html', word_count=results, graph=graph)
        elif granularity == "2":
            return render_template('graph_day.html', word_count=results, graph=graph)
        else:
            return render_template('graph_week.html', word_count=results, graph=graph)

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


@app.route(
    '/api/username/<string:username>/<string:keyword>/<string:granularity>',
    methods=['GET'])
def getTweetSearchNoDates(username, keyword, granularity):
    pass


@app.route(
    '/api/username/<string:username>/<string:keyword>/<string:granularity>/<string:dfrom>/<string:dto>',
    methods=['GET'])
def getTweetSearchWithDates(username, keyword, granularity, dfrom, dto):
    freq_conn = Frequency(mongo)
    results = -1
    # YEAR GRANULARITY
    if granularity == "0":
        results = dumps(freq_conn.get_year_total(username, keyword, dfrom, dto))
    # MONTH GRANULARITY
    elif granularity == "1":
        results = dumps(freq_conn.get_month_total(username, keyword, dfrom, dto))
    # DAY GRANULARITY
    elif granularity == "2":
        results = dumps(freq_conn.get_day_total(username, keyword, dfrom, dto))
    elif granularity == "3":
        results = dumps(freq_conn.get_week_total(username, keyword, dfrom, dto))

    return results


# Generic Search Routes

# Returns all tweets in the database
@app.route('/api/all/', methods=['GET'])
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
