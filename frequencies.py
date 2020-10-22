from multiprocessing import Process
from flask_pymongo import PyMongo
from datetime import datetime


# Gets frequencies of tweets using MongoDB aggregation
class Frequency:
    def __init__(self, conn):
        self.mongo = conn

    # Function returns a JSON of total tweets per year for given dates
    def get_year_total(self, username, search_keyword, date_from, date_until):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_until = datetime.strptime(date_until, "%Y-%m-%d")
        self.set_year_pipeline(username, search_keyword, date_from, date_until)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.year_pipeline)
        return results

    # Function returns a JSON of total tweets per month for given dates
    def get_month_total(self, username, search_keyword, date_from, date_until):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_until = datetime.strptime(date_until, "%Y-%m-%d")
        self.set_month_pipeline(username, search_keyword, date_from, date_until)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.month_pipeline)
        return results

    # Function returns a JSON of total tweets per week for given dates
    def get_week_total(self, username, search_keyword, date_from, date_until):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_until = datetime.strptime(date_until, "%Y-%m-%d")
        self.set_week_pipeline(username, search_keyword, date_from, date_until)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.week_pipeline)
        return results

    # Function returns a JSON of total tweets per day for given dates
    def get_day_total(self, username, search_keyword, date_from, date_until):
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_until = datetime.strptime(date_until, "%Y-%m-%d")
        self.set_day_pipeline(username, search_keyword, date_from, date_until)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.day_pipeline)
        return results

    # Initialises the aggregation pipeline for year granularity
    def set_year_pipeline(self, username, keyword, date_from, date_until):
        #print(datetime.strptime(date_from, '%Y-%m-%d'))
        self.year_pipeline = [
            {
                "$match": {"username": username, "$text": {"$search": keyword}}
            },
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": date_from,
                    "dateUntil": date_until,
                    "year": {"$year": {"$dateFromString": {"dateString": "$date"}}},
                }
            },
            {
                "$match": {"wholeDate": {"$gte": date_from, "$lte": date_until}}
            },
            {
                "$group":
                {
                    "_id": {"year": "$year"},
                    "count": {"$sum": 1}
                }
            }
        ]

    # Initialises the aggregation pipeline for month granularity
    def set_month_pipeline(self, username, keyword, date_from, date_until):
        self.month_pipeline = [
            {
                "$match": {"username": username, "$text": {"$search": keyword}}
            },
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": date_from,
                    "dateUntil": date_until,
                    "year": {"$year": {"$dateFromString": {"dateString": "$date"}}},
                    "month": {"$month": {"$dateFromString": {"dateString": "$date"}}},
                }
            },
            # {
            #     "$match": {"wholeDate": {"$gte": "dateFrom", "$lte": "dateUntil"}}
            # },
            {
                "$group":
                {
                    "_id": {"year": "$year", "month": "$month"},
                    "count": {"$sum": 1}
                }
            }
        ]

    # Initialises the aggregation pipeline for week granularity
    def set_week_pipeline(self, username, keyword, date_from, date_until):
        self.week_pipeline = [
            {
                "$match": {"username": username, "$text": {"$search": keyword}}
            },
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": date_from,
                    "dateUntil": date_until,
                    "year": {"$year": {"$dateFromString": {"dateString": "$date"}}},
                    "month": {"$month": {"$dateFromString": {"dateString": "$date"}}},
                    "week": {"$toInt": {"$round": {"$divide": [{"$dayOfMonth": {"$dateFromString": {"dateString": "$date"}}}, 7]}}},
                }
            },
            # {
            #     "$match": {"wholeDate": {"$gte": "dateFrom", "$lte": "dateUntil"}}
            # },
            {
                "$group":
                {
                    "_id": {"year": "$year", "month": "$month", "week": "$week"},
                    "count": {"$sum": 1}
                }
            }
        ]

    # Initialises the aggregation pipeline for day granularity
    def set_day_pipeline(self, username, keyword, date_from, date_until):
        self.day_pipeline = [
            {
                "$match": {"username": username, "$text": {"$search": keyword}}
            },
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": date_from,
                    "dateUntil": date_until,
                    "year": {"$year": {"$dateFromString": {"dateString": "$date"}}},
                    "month": {"$month": {"$dateFromString": {"dateString": "$date"}}},
                    "day": {"$dayOfMonth": {"$dateFromString": {"dateString": "$date"}}},
                }
            },
            # {
            #     "$match": {"wholeDate": {"$gte": "dateFrom", "$lte": "dateUntil"}}
            # },
            {
                "$group":
                {
                    "_id": {"year": "$year", "month": "$month", "day": "$day"},
                    "count": {"$sum": 1}
                }
            }
        ]