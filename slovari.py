import functools
import sys
import time

import requests


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


def cache(f):
    @functools.wraps(f)
    def deco(*args):
        if args in deco._cache:
            return deco._cache[args]

        result = f(*args)

        deco._cache[args] = result

        return result

    deco._cache = {}

    return deco

@profile(msg='Elapsed time')
@cache
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
