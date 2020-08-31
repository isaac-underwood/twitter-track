from flask import Flask, render_template
import twint
from pymongo import MongoClient
import pprint

client = MongoClient('localhost', 27017)
db = client.twitter
tweets = db.tweets
app = Flask(__name__)
tc = twint.Config()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graph')
def graph():
    t = tweets.find({})
    word_count = 0
    word_count2 = 0
    word = "great"
    word2 = "bad"
    tweet = t[0]
    for tw in t:
        if word in tw['tweet']:
            word_count+=1
    for tw in t:
        if word2 in tw['tweet']:
            word_count2+=1
    return render_template('graph.html', word_count=word_count, word_count2=word_count2)
    #return str(tweet['tweet'])


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


if __name__ == '__main__':
    app.run(debug=True)
