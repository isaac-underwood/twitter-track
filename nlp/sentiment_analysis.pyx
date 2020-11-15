from __future__ import print_function
from transformers import pipeline
# from tokenizers import PreTrainedTokenizerFast
import tensorflow as tf
from flask_pymongo import PyMongo
from pymongo import MongoClient
import numpy as np
from cymem.cymem cimport Pool


cdef class SentimentAnalysis:
    cdef object nlp
    cdef object tokenizer
    cdef object db_conn

    def __cinit__(self, db_conn):
        self.nlp = pipeline('sentiment-analysis', device=0)  # Set pipeline and set device to use GPU (default is CPU)
        self.db_conn = db_conn

    # Performs sentiment analysis using a batch
    def analyse(self, batch):
        cdef list result = self.nlp(batch)
        return result

    # Updates each tweet in the batch adding the sentiment label and score
    def update_batch(self, batch, batch_ids):
        for i in range(len(batch)):
            sec_arg = {"$set": {"sentiment_label": batch[i]['label'], "sentiment_score": round(batch[i]['score'], 4)}}
            self.db_conn.update_one({"_id": batch_ids[i]}, sec_arg, upsert=False)

    # Requests tweets and performs SA, then updates tweets (in batches)
    def process_tweets(self):
        cdef list analysed
        cdef list batch = []
        cdef list batch_ids = []
        cdef int count = 0
        cdef int chunks = 0
        cdef int batchsize = 64
        cdef int total_processed = 0
        cdef bint remaining_tweets
        
        cdef object cursor = self.db_conn.find({"sentiment_label": {"$exists": False}}).batch_size(16384)
        for doc in cursor:
            remaining_tweets = cursor.alive  # Check if any more results can be returned from the cursor
            if remaining_tweets == False:
                # Set batch size to be current count, as initially set batch size is greater than amount of docs left
                batchsize = count + 1
            
            if count == batchsize:
                chunks += 1
                total_processed = chunks * batchsize
                print(f'{chunks} chunks completed (size: {batchsize}). {total_processed} total.')
                analysed = self.analyse(batch)
                self.update_batch(analysed, batch_ids)
                batch = []
                batch_ids = []
                count = 0
                
            batch.append(doc['tweet'])
            batch_ids.append(doc['_id'])
            count += 1