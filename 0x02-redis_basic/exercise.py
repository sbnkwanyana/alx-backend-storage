#!/usr/bin/env python3
"""
Module defines class Cache that interacts with a redis cache
"""
import redis
import uuid
from typing import Union, Callable


class Cache:
    """
    Class Cache is used to interact with a redis cache
    """

    def __init__(self) -> None:
        """
        Instantiates a new Cache class
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generates a unique id and stores data to redis cache
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """
        function gets data from redis cache and calls function to convert
        to original data type
        """
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        """
        function converts data into string
        """
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """
        function converts data into int
        """
        return self.get(key, lambda x: int(x))
