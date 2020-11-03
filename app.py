from flask import Flask, render_template, jsonify, request, url_for
import twint
from pymongo import MongoClient
from bson.json_util import dumps
from frequencies import Frequency
import os
from datetime import datetime

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


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST':
        days_count = [0, 0, 0, 0, 0, 0, 0]
        months = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']
        months_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        weeks_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        years_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        aggregate = request.form['aggregate']
        org = request.form['news']
        word = request.form['search']
        end = request.form['start']
        start = request.form['end']
        graph = request.form['graph']

        queried_title = f'"{word}" — {org} — {end} - {start}'

        if org == 'all':
            t = tweets.find({"$text": {"$search": word}, "date": {"$lt": start}, "date": {"$gt": end}})
        else:
            t = tweets.find({"$text": {"$search": word}, "username": org, "date": {"$lt": start}, "date": {"$gt": end}})
        for tw in t:
            date = tw['date'].replace('-', '/')
            date_obj = datetime.strptime(date, '%Y/%m/%d')
            if aggregate == 'month':
                months_count[date_obj.month-1]+=1
            if aggregate == 'day':
                days_count[date_obj.weekday()]+=1
            if aggregate == 'week':
                weeks_count[date_obj.isocalendar()[1]-2]+=1
            if aggregate == 'year':
                years_count[date_obj.year%2011]+=1
            # date = tw['date'].replace('-', '/')
            # date_obj = datetime.strptime(date, '%Y/%m/%d')
            # if word in tw['tweet']:
            #     if aggregate == 'month':
            #         months_count[date_obj.month-1]+=1
            #     if aggregate == 'day':
            #         days_count[date_obj.weekday()]+=1
            #     if aggregate == 'week':
            #         weeks_count[date_obj.isocalendar()[1]-1]+=1
            #     if aggregate == 'year':
            #         years_count[date_obj.year%2011]+=1
        if aggregate == 'month':
            return render_template('graph_month.html', word_count=months_count, word=months, graph=graph, qt=queried_title)
        if aggregate == 'week':
            return render_template('graph_week.html', word_count=weeks_count, graph=graph, qt=queried_title)
        if aggregate == 'day':
            return render_template('graph_day.html', word_count=days_count, graph=graph, qt=queried_title)
        if aggregate == 'year':
            return render_template('graph_year.html', word_count=years_count, graph=graph, qt=queried_title)
    else:
        return render_template('graph_year.html')
    # return str(tweet['tweet'])

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