import functools


import requests
from memory_profiler import memory_usage


def profile_memory(msg='Memory info'):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            result = f(*args, **kwargs)
            result_to_memorize = tuple(result)
            mem = memory_usage(proc=result_to_memorize)
            print(msg, f'({f.__name__}):  {mem}')
            return result

        return deco

    return internal


def cache_lfu(max_limit=100):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            deco._cache[cache_key]["counter"] = 1
            if cache_key in deco._cache:
                deco._cache[cache_key]["counter"] += 1
                return deco._cache[cache_key]

            result = f(*args, **kwargs)

            if len(deco._cache) >= max_limit:
                del deco._cache[min(deco._cache, key=lambda cache_key: deco._cache[cache_key]["counter"])]
            deco._cache[cache_key]["result"] = result
            return result
        deco._cache = {}
        return deco
    return internal



@cache_lfu(max_limit=30)
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
