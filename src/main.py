from ospf import Routing
import asyncio
import time


def count_time(func):
    def inner():
        start = time.time()
        asyncio.run(func())
        end = time.time()
        print(end - start)
        print('=' * 30)

    return inner



