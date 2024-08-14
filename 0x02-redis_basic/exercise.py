#!/usr/bin/env python3
'''create a Cache class'''
import redis
import uuid
from typing import Union


class Cache:
    '''start Caching the redis'''
    def __init__(self):
        '''the init method'''
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb()

    def store(self, data: Union[str, int, bytes, float]) -> str:
        '''store method to return the key value as a string'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
