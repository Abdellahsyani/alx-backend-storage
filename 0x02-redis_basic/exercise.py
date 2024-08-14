#!/usr/bin/env python3
'''Create a Cache class'''
import redis
import uuid
from typing import Union


class Cache:
    '''Start caching with Redis'''
    def __init__(self):
        '''The init method'''
        self._redis = redis.Redis(host='localhost', port=6379, db=0)
        self._redis.flushdb(True)

    def store(self, data: Union[str, int, bytes, float]) -> Union[str, None, None, None]:
        '''Store method to return the key value as a string'''
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
