#!/usr/bin/env python3
"""
Module contains function that inserts new document in a collection
"""


def insert_school(mongo_collection, **kwargs):
    """
    function returns the id of the newly added document in the collection
    """
    return mongo_collection.insert_one(kwargs).inserted_id
