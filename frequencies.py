from multiprocessing import Process
from flask_pymongo import PyMongo
from datetime import datetime


class Frequency:
    def __init__(self, conn):
        self.mongo = conn

        
        
        # self.year_query_old = """{{
        #     $match:
        #     {{
        #         $text: {{ $search: "{keyword}" }}
        #     }}
        #     }},
        #     {{
        #         $project:
        #         {{
        #             wholeDate: {{ $dateFromString: {{ dateString: "$date" }} }},
        #             year: {{ $year: {{ $dateFromString: {{ dateString: "$date" }} }} }},
        #         }}
        #     }},
        #     {{
        #         $match:
        #         {{
        #             wholeDate: {{ "$gte": "{date_from_}", "$lte": {date_until_} }}
        #         }}
        #     }},
        #     {{
        #         $group:
        #         {{
        #             _id : {{
        #             year: "$year",
        #             }},
        #             count: {{ $sum: 1 }}
        #         }}
        #     }}"""
        # self.month_query = """{{
        #     $match:
        #     {{
        #         $text: {{ $search: "{keyword}" }}
        #     }}
        #     }},
        #     {{
        #         $project:
        #         {{
        #             wholeDate: {{ $dateFromString: {{ dateString: "$date" }} }},
        #             year: {{ $year: {{ $dateFromString: {{ dateString: "$date" }} }} }},
        #             month: {{ $month: {{ $dateFromString: {{ dateString: "$date" }} }} }},
        #         }}
        #     }},
        #     {{
        #         $match:
        #         {{
        #             wholeDate: {{ "$gte": "{date_from_}", "$lte": {date_until_} }}
        #         }}
        #     }},
        #     {{
        #         $group:
        #         {{
        #             _id : {{
        #             year: "$year",
        #             month: "$month",
        #             }},
        #             count: {{ $sum: 1 }}
        #         }}
        #     }}"""
        # self.day_query = """{{
        #     $match:
        #     {{
        #         $text: {{ $search: "{keyword}" }}
        #     }}
        #     }},
        #     {{
        #         $project:
        #         {{
        #             wholeDate: {{ $dateFromString: {{ dateString: "$date" }} }},
        #             year: {{ $year: {{ $dateFromString: {{ dateString: "$date" }} }} }},
        #             month: {{ $month: {{ $dateFromString: {{ dateString: "$date" }} }} }},
        #             day: {{ $dayOfMonth: {{ $dateFromString: {{ dateString: "$date" }} }} }}
        #         }}
        #     }},
        #     {{
        #         $match:
        #         {{
        #             wholeDate: {{ "$gte": "{date_from_}", "$lte": {date_until_} }}
        #         }}
        #     }},
        #     {{
        #         $group:
        #         {{
        #             _id : {{
        #             year: "$year",
        #             month: "$month",
        #             day: "$day",
        #             }},
        #             count: {{ $sum: 1 }}
        #         }}
        #     }}"""

    # Function returns a JSON of total tweets per year for given dates
    def get_year_total(self, username, search_keyword, date_from, date_until):
        print(search_keyword, date_from, date_until)
        self.set_year_pipeline(username, search_keyword, date_from, date_until)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.year_pipeline)
        return results

    # Function returns a JSON of total tweets per month for given dates
    def get_month_total(self, username, search_keyword, date_from, date_until):
        print(search_keyword, date_from, date_until)
        self.set_month_pipeline(username, search_keyword, date_from, date_until)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.month_pipeline)
        return results

    # Function returns a JSON of total tweets per day for given dates
    def get_day_total(self, username, search_keyword, date_from, date_until):
        print(search_keyword, date_from, date_until)
        self.set_day_pipeline(username, search_keyword, date_from, date_until)
        results = self.mongo.test.aggregate(aggregate="test", pipeline=self.day_pipeline)
        return results

    def set_year_pipeline(self, username, keyword, date_from, date_until):
        print(datetime.strptime(date_from, '%Y-%m-%d'))
        self.year_pipeline = [
            {
                "$match": {"username": username, "$text": {"$search": keyword}}
            },
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": {"$dateFromString": {"dateString": date_from}},
                    "dateUntil": {"$dateFromString": {"dateString": date_until}},
                    "year": {"$year": {"$dateFromString": {"dateString": "$date"}}},
                }
            },
            # {
            #     "$match": {"wholeDate": {"$gte": "dateFrom", "$lte": "dateUntil"}}
            # },
            {
                "$group":
                {
                    "_id": {"year": "$year"},
                    "count": {"$sum": 1}
                }
            }
        ]

    def set_month_pipeline(self, username, keyword, date_from, date_until):
        self.month_pipeline = [
            {
                "$match": {"username": username, "$text": {"$search": keyword}}
            },
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": {"$dateFromString": {"dateString": date_from}},
                    "dateUntil": {"$dateFromString": {"dateString": date_until}},
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

    def set_day_pipeline(self, username, keyword, date_from, date_until):
        self.day_pipeline = [
            {
                "$match": {"username": username, "$text": {"$search": keyword}}
            },
            {
                "$project":
                {
                    "wholeDate": {"$dateFromString": {"dateString": "$date"}},
                    "dateFrom": {"$dateFromString": {"dateString": date_from}},
                    "dateUntil": {"$dateFromString": {"dateString": date_until}},
                    "year": {"$year": {"$dateFromString": {"dateString": "$date"}}},
                    "month": {"$month": {"$dateFromString": {"dateString": "$date"}}},
                    "day": {"$day": {"$dateFromString": {"dateString": "$date"}}},
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