import functools
import sys
from datetime import time

import requests
from memory_profiler import memory_usage


def profile_memory(msg='Memory info'):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            result = f(*args, **kwargs)
            mem = memory_usage((f, args, kwargs))
            print(msg, f'({f.__name__}):  {max(mem)}')
            return result

        return deco

    return internal


def cache_lfu(max_limit=100):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in deco._cache:
                deco._cache[cache_key]["counter"] += 1
                return deco._cache[cache_key]["result"]



            if len(deco._cache) >= max_limit:
                del deco._cache[min(deco._cache, key=lambda cache_key: deco._cache[cache_key]["counter"])]

            result = f(*args, **kwargs)

            deco._cache[cache_key]["counter"] = 1
            deco._cache[cache_key]["result"] = result

            return result

        deco._cache = {}
        return deco
    return internal

def profile(msg='Elapsed time', file=sys.stdout):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            start = time.time()
            result = f(*args, **kwargs)
            print(msg, f'({f.__name__}): {time.time() - start}s', file=file)
            return result
        return deco
    return internal

@cache_lfu
@profile
@profile_memory
def fetch_url(url, first_n=120):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://google.com')
fetch_url('https://ithillel.ua')
fetch_url('https://dou.ua')
fetch_url('https://ain.ua')
fetch_url('https://youtube.com')
