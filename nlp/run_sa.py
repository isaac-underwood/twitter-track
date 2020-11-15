from flask_pymongo import PyMongo
from pymongo import MongoClient
from sentiment_analysis import SentimentAnalysis

client = MongoClient('localhost', 27017)
db = client.test
tweets = db.test
sa = SentimentAnalysis(tweets)
sa.process_tweets()