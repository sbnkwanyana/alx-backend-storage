#!/usr/bin/env python3
"""
module contains function that returns list with topics
"""


def schools_by_topic(mongo_collection, topic):
    """
    function finds topics in a collection of documents
    """
    topics = { "topics": {"$elemMatch": {"$eq": topic }}}
    return [document for document in mongo_collection.find(topics)]
