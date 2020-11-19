from multiprocessing import Process
from flask_pymongo import PyMongo
from datetime import datetime


# Gets frequencies of tweets using MongoDB aggregation
class Frequency:
    def __init__(self, conn):
        self.mongo = conn

    # Function returns a JSON of total tweets per year for given dates
    def get_year_total(self, search_keyword, date_from, date_until, username=None):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_until = datetime.strptime(date_until, "%Y-%m-%d")
        self.set_year_pipeline(search_keyword, date_from, date_until, username)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.year_pipeline, allowDiskUse=True)
        return results

    # Function returns a JSON of total tweets per month for given dates
    def get_month_total(self, search_keyword, date_from, date_until, username=None):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_until = datetime.strptime(date_until, "%Y-%m-%d")
        self.set_month_pipeline(search_keyword, date_from, date_until, username)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.month_pipeline, allowDiskUse=True)
        return results

    # Function returns a JSON of total tweets per week for given dates
    def get_week_total(self, search_keyword, date_from, date_until, username=None):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_until = datetime.strptime(date_until, "%Y-%m-%d")
        self.set_week_pipeline(search_keyword, date_from, date_until, username)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.week_pipeline, allowDiskUse=True)
        return results

    # Function returns a JSON of total tweets per day for given dates
    def get_day_total(self, search_keyword, date_from, date_until, username=None):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_until = datetime.strptime(date_until, "%Y-%m-%d")
        self.set_day_pipeline(search_keyword, date_from, date_until, username)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.day_pipeline, allowDiskUse=True)
        return results

    # Initialises the aggregation pipeline for year granularity
    def set_year_pipeline(self, keyword, date_from, date_until, username=None):
        # Check if a username has been passed in, if not do not filter on username
        match = {}
        if username is None:
            match = {"$match": {"$text": {"$search": f'\"{keyword}\"'}}}
        else:
            match = {"$match": {"username": username, "$text": {"$search": f'\"{keyword}\"'}}}
        self.year_pipeline = [
            match,  # The match filter (either containing username filter or not)
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": date_from,
                    "dateUntil": date_until,
                    "year": {"$year": {"$dateFromString": {"dateString": "$date"}}},
                    "positiveSentiment": {"$strcasecmp": ['$sentiment_label', 'positive']},
                    "negativeSentiment": {"$strcasecmp": ['$sentiment_label', 'negative']},
                }
            },
            {
                "$match": {"wholeDate": {"$gte": date_from, "$lte": date_until}}
            },
            {
                "$group":
                {
                    "_id": {"year": "$year"},
                    "count": {"$sum": 1},
                    "positive_sentiment": {
                        "$sum": 
                            {
                                "$cond": 
                                    [{
                                        "$eq": [
                                            "$positiveSentiment", 0
                                        ]
                                    }, 1, 0]}
                    },
                    "negative_sentiment": {
                        "$sum": 
                            {
                                "$cond": 
                                    [{
                                        "$eq": [
                                            "$negativeSentiment", 0
                                        ]
                                    }, 1, 0]}
                    },
                }
            },
            {
                "$sort":
                {
                    "_id": 1
                }
            }
        ]

    # Initialises the aggregation pipeline for month granularity
    def set_month_pipeline(self, keyword, date_from, date_until, username=None):
        # Check if a username has been passed in, if not do not filter on username
        match = {}
        if username is None:
            match = {"$match": {"$text": {"$search": f'\"{keyword}\"'}}}
        else:
            match = {"$match": {"username": username, "$text": {"$search": f'\"{keyword}\"'}}}
        self.month_pipeline = [
            match,  # The match filter (either containing username filter or not)
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": date_from,
                    "dateUntil": date_until,
                    "month": {"$month": {"$dateFromString": {"dateString": "$date"}}},
                    "positiveSentiment": {"$strcasecmp": ['$sentiment_label', 'positive']},
                    "negativeSentiment": {"$strcasecmp": ['$sentiment_label', 'negative']},

                }
            },
            # {
            #     "$match": {"wholeDate": {"$gte": "dateFrom", "$lte": "dateUntil"}}
            # },
            {
                "$group":
                {
                    "_id": {"month": "$month"},
                    "count": {"$sum": 1},
                    "positive_sentiment": {
                        "$sum": 
                            {
                                "$cond": 
                                    [{
                                        "$eq": [
                                            "$positiveSentiment", 0
                                        ]
                                    }, 1, 0]}
                    },
                    "negative_sentiment": {
                        "$sum": 
                            {
                                "$cond": 
                                    [{
                                        "$eq": [
                                            "$negativeSentiment", 0
                                        ]
                                    }, 1, 0]}
                    },
                }
            },
            {
                "$sort":
                {
                    "_id": 1
                }
            }

        ]

    # Initialises the aggregation pipeline for week granularity
    def set_week_pipeline(self, keyword, date_from, date_until, username=None):
        # Check if a username has been passed in, if not do not filter on username
        match = {}
        if username is None:
            match = {"$match": {"$text": {"$search": f'\"{keyword}\"'}}}
        else:
            match = {"$match": {"username": username, "$text": {"$search": f'\"{keyword}\"'}}}
        self.week_pipeline = [
            match,  # The match filter (either containing username filter or not)
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": date_from,
                    "dateUntil": date_until,
                    "week": {"$toInt": {"$round": {"$divide": [{"$dayOfMonth": {"$dateFromString": {"dateString": "$date"}}}, 7]}}},
                    "positiveSentiment": {"$strcasecmp": ['$sentiment_label', 'positive']},
                    "negativeSentiment": {"$strcasecmp": ['$sentiment_label', 'negative']},

                }
            },
            {
                "$group":
                {
                    "_id": {"$week": "$wholeDate"},
                    "count": {"$sum": 1},
                    "positive_sentiment": {
                        "$sum": 
                            {
                                "$cond": 
                                    [{
                                        "$eq": [
                                            "$positiveSentiment", 0
                                        ]
                                    }, 1, 0]}
                    },
                    "negative_sentiment": {
                        "$sum": 
                            {
                                "$cond": 
                                    [{
                                        "$eq": [
                                            "$negativeSentiment", 0
                                        ]
                                    }, 1, 0]}
                    },
                }
            },
            {
                "$sort":
                {
                    "_id": 1
                }
            }

        ]

    # Initialises the aggregation pipeline for day granularity
    def set_day_pipeline(self, keyword, date_from, date_until, username=None):
        # Check if a username has been passed in, if not do not filter on username
        match = {}
        if username is None:
            match = {"$match": {"$text": {"$search": f'\"{keyword}\"'}}}
        else:
            match = {"$match": {"username": username, "$text": {"$search": f'\"{keyword}\"'}}}
        self.day_pipeline = [
            match,  # The match filter (either containing username filter or not)
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": date_from,
                    "dateUntil": date_until,
                    "day": {"$dayOfWeek": {"$dateFromString": {"dateString": "$date"}}},
                    "positiveSentiment": {"$strcasecmp": ['$sentiment_label', 'positive']},
                    "negativeSentiment": {"$strcasecmp": ['$sentiment_label', 'negative']},

                }
            },
            {
                "$group":
                {
                    "_id": {"day": "$day"},
                    "count": {"$sum": 1},
                    "positive_sentiment": {
                        "$sum": 
                            {
                                "$cond": 
                                    [{
                                        "$eq": [
                                            "$positiveSentiment", 0
                                        ]
                                    }, 1, 0]}
                    },
                    "negative_sentiment": {
                        "$sum": 
                            {
                                "$cond": 
                                    [{
                                        "$eq": [
                                            "$negativeSentiment", 0
                                        ]
                                    }, 1, 0]}
                    },
                }
            },
            {
                "$sort":
                {
                    "_id": 1
                }
            }
        ]
