from ospf import Routing
import asyncio
import time


def count_time(func):
    def inner():
        start = time.time()
        func()
        end = time.time()
        print(end - start)
        print('=' * 30)

    return inner


@count_time
def main():
    routings = [Routing(i, 0, 0, '0.1.0', []) for i in range(5)]
    loop = asyncio.get_event_loop()
    coros = (
        [routing.send_hello() for routing in routings]
        + [routing.process_hello() for routing in routings]
        + [routing.process_hello() for routing in routings]
    )

    coro = asyncio.wait(coros)
    loop.run_until_complete(coro)
    loop.close()


if __name__ == '__main__':
    main()
