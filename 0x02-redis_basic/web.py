#!/usr/bin/env python3
"""
module contains function and decorator function
that caches requests in redis cache
"""
import redis
import requests
from typing import Callable
from functools import wraps


store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """
    decorator function caches web requests
    """
    @wraps(method)
    def invoker(url) -> str:
        """
        function returns saves requests and returns cached requests
        """
        def wrapper(url):
            data = store.get(url)
            if data:
                return data.decode("utf-8")
            count = f"count: {url}"
            html = method(url)
            store.incr(count)
            store.set(url, html)
            store.expire(url, 10)
            return html
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """
    function gets html content
    """
    return requests.get(url).text
