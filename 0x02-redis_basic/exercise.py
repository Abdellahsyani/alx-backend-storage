#!/usr/bin/env python3
'''Create a Cache class'''
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    '''Start caching with Redis'''

    def __init__(self) -> None:
        '''The init method'''

        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, int, bytes, float]) -> str:
        '''Store method to return the key value as a string'''

        key_data = str(uuid.uuid4())
        self._redis.set(key_data, data)
        return key_data

    def get(self,
            key_data: str,
            fn: Callable = None) -> Union[str, int, bytes, float]:
        '''retrieve the data from cache by using the callable'''
        key = self._redis.get(key_data)
        if key is not None and fn is not None:
            return fn(key)
        return key

    def get_str(self, key_data: str) -> str:
        '''retreive data as a string'''
        return self.get(key_data, lambda d: d.decode('utf-8'))

    def get_int(self, key_data: str) -> int:
        return self.get(key_data, int)
