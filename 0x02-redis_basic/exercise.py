#!/usr/bin/env python3
'''Create a Cache class'''
import redis
import uuid
from typing import Union, Callable
import functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(fn: Callable) -> None:
    '''Displays the call history of a Cache class' method.
    '''
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    '''Start caching with Redis'''

    def __init__(self) -> None:
        '''The init method'''

        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @call_history
    @count_calls
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
        '''retrieve data as integer'''
        return self.get(key_data, int)
