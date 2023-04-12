#!/usr/bin/env python3
"""
Module defines class Cache that interacts with a redis cache
"""
from functools import wraps
import redis
import uuid
from typing import Union, Callable, Any


def call_history(method: Callable) -> Callable:
    """
    decorator function stores the inputs and outputs of a function
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            output_keys = f'{method.__qualname__}:outputs'
            self._redis.rpush(output_keys, str(args), output)
        return output
    return invoker


def count_calls(method: Callable) -> Callable:
    """
    function counts the number of times a function is called
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        function increments value each time function is called
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


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

    @count_calls
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
