from flask import Flask, render_template, jsonify, request, url_for
import twint
from pymongo import MongoClient
from bson.json_util import dumps
from frequencies import Frequency
import os
import json
from datetime import datetime
import numpy as np

client = MongoClient('localhost', 27017)
db = client.test
tweets = db.test
app = Flask(__name__)
tc = twint.Config()


@app.route('/')
def index():
    return render_template('landing.html')


# Loads home page
@app.route('/search')
def search():
    return render_template('index.html')

@app.route('/graphtwo', methods=['GET', 'POST'])
def graph_two():
    # if request.method == 'POST':
        # aggregate = request.form['aggregate']
        # org = request.form['news']
        # word = request.form['search']
        # end = request.form['end']
        # start = request.form['start']
        # graph = request.form['graph']

        # queried_title = f'"{word}" — {org} — {end} - {start}'
    freq = Frequency(client)
    # result = dumps(list(freq.get_year_total(search_keyword="Trump", date_from="2006-01-01", date_until="2020-11-10")))
    result = dumps(list(freq.get_day_total(search_keyword="Trump", date_from="2006-01-01", date_until="2020-11-10")))
    print(result)
    return result
        

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST':
        months = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']
        aggregate = request.form['aggregate']
        org = request.form['news']
        word = request.form['search']
        end = request.form['end']
        start = request.form['start']
        graph = request.form['graph']

        queried_title = f'"{word}" — {org} — {start} - {end}'

        freq = Frequency(client)
        if org == 'all':
            org = None

        rand_tweets = dumps(tweets.aggregate([
            {"$match": {"$text": {"$search": word}}}, 
            {"$sample": {"size": 1}}
            ]), default=str)

        if aggregate == 'month':
            result = list(freq.get_month_total(search_keyword=word, username=org, date_from=start, date_until=end))
            return render_template('graph_month.html', word_count=result, word=months, graph=graph, qt=queried_title)
        elif aggregate == 'week':
            result = list(freq.get_week_total(search_keyword=word, username=org, date_from=start, date_until=end))
            return render_template('graph_week.html', word_count=result, graph=graph, qt=queried_title,)
        elif aggregate == 'day':
            result = list(freq.get_day_total(search_keyword=word, username=org, date_from=start, date_until=end))
            return render_template('graph_day.html', word_count=result, graph=graph, qt=queried_title)
        elif aggregate == 'year':
            result = list(freq.get_year_total(search_keyword=word, username=org, date_from=start, date_until=end))
            return render_template('graph_year.html', word_count=result, graph=graph, qt=queried_title, randtw=rand_tweets)
    else:
        return 'Not found', 404

# API ROUTES

# Username Routes (for getting tweets via username)

@app.route('/api/username/<string:username>')
#   Accepts keyword (search term) to search a user's tweets
@app.route('/api/username/<string:username>/<string:keyword>')
def twintTimeline(username, keyword=None):
    tc.Output = "users.csv"
    tc.Store_csv = True
    tc.Username = username

    # Check if search terms were passed in
    if keyword is not None:
        tc.Search = keyword

    # Search user's timeline using config
    twint.run.Search(tc)


# Generic Search Routes

# Accepts a keyword (search term) to search all tweets
@app.route('/api/generic/<string:keyword>')
def twintGenericSearch(keyword):
    tc.Search = keyword  # Set search term in config
    twint.run.Search(tc)


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


# Adds a timestamp to static files so that browser uses updated CSS files
# (Browser caching means that new css files aren't being used)
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


if __name__ == '__main__':
    app.run(debug=True)