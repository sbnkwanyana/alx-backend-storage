#!/usr/bin/env python3
"""
Module contains function list_all that returns
a list of all documents in a collection
"""


def list_all(mongo_collection):
    """
    function returns list of documents or
    an empty list from a mongodb collection
    """
    return [document for document in mongo_collection.find()]
