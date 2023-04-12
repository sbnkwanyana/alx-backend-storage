#!/usr/bin/env python3
"""
Module defines class Cache that interacts with a redis cache
"""
from functools import wraps
import redis
import uuid
from typing import Union, Callable, Any


def replay(fn: Callable) -> None:
    """
    function prints out the number of times a function is called
    and the history of its inputs and outputs
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    fn_name = fn.__qualname__
    cache = getattr(fn.__self__, '_redis', None)
    if not isinstance(cache, redis.Redis):
        return
    called = 0
    if cache.exists(fn_name) != 0:
        called = int(cache.get(fn_name))
    print(f'{fn_name} was called {called} times:')
    inputs = cache.lrange(f'{fn_name}:inputs', 0, -1)
    outputs = cache.lrange(f'{fn_name}:outputs', 0, -1)
    for input, output in zip(inputs, outputs):
        print(f'{fn_name}(*{input.decode("utf-8")}) -> {output}')


def call_history(method: Callable) -> Callable:
    """
    decorator function stores the inputs and outputs of a function
    """
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """
        stores both the input and output values of the function call
        """
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(f'{method.__qualname__}:inputs', str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(f'{method.__qualname__}:outputs', output)
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

    @call_history
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
