#!/usr/bin/env python3
"""
module contains function to update a document based on a name
"""


def update_topics(mongo_collection, name, topics):
    """
    function updates a collection with given topics
    """
    mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
