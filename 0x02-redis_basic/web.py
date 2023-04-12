#!/usr/bin/env python3
"""
module contains function and decorator function
that caches requests in redis cache
"""
import redis
import requests
from typing import Callable
from functools import wraps


cache = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    decorator function caches web requests
    """
    @wraps(method)
    def invoker(url) -> str:
        """
        function returns saves requests and returns cached requests
        """
        cache.incr(f'count:{url}')
        result = cache.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        cache.set(f'count:{url}', 0)
        cache.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    function gets html content
    """
    return requests.get(url).text
