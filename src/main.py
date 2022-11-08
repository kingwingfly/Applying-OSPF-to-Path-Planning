from routing import Routing
import asyncio
import time

num = 5
LSAs = [
    {2: 1},
    {2: 1, 3: 1},
    {0: 1, 1: 1, 3: 1},
    {1: 1, 2: 1, 4: 1},
    {3: 1},
]
routings = [Routing(ID, LSA) for (ID, LSA) in enumerate(LSAs)]


def count_time(func):
    def inner():
        start = time.time()
        asyncio.run(func())
        end = time.time()
        print(end - start)

    return inner


@count_time
async def main():
    await asyncio.gather(*(routing.send_hello(routings) for routing in routings))
    await asyncio.gather(*(routing.check_connection() for routing in routings))
    await asyncio.gather(*(routing.send_LSA_index(routings) for routing in routings))
    await asyncio.gather(
        *(routing.receive_LSA_index_then_ask(routings) for routing in routings)
    )
    await asyncio.gather(*(routing.respond_requets(routings) for routing in routings))
    await asyncio.gather(
        *(routing.receive_LSA_then_update(routings) for routing in routings)
    )


for i in range(5):
    main()
    time.sleep(0)
