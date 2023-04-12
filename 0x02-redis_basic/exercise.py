#!/usr/bin/env python3
"""
Module defines class Cache that interacts with a redis cache
"""
import redis
import uuid
from typing import Union


class Cache:
    """
    Class Cache is used to interact with a redis cache
    """

    def __init__(self) -> None:
        """
        Instantiates a new Cache class
        """
        self._redis = redis.Redis().flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a unique id and stores data to redis cache
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
