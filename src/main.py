from routing import Routing
import asyncio
import time


LSAs = [
    {2: 1},
    {2: 1, 3: 1},
    {0: 1, 1: 1, 3: 1},
    {1: 1, 2: 1, 4: 1},
    {3: 1},
]
DR = 2
BDR = 3
routings = [Routing(ID, LSA) for (ID, LSA) in enumerate(LSAs)]


def count_time(func):
    def inner():
        start = time.time()
        asyncio.run(func())
        end = time.time()
        print(end - start)
        print('=' * 30)

    return inner


@count_time
async def main():
    await asyncio.gather(*(routing.send_hello(routings) for routing in routings))
    await asyncio.gather(*(routing.check_connection(routings) for routing in routings))
    await asyncio.gather(*(routing.send_LSA_index(routings) for routing in routings))
    await asyncio.gather(
        *(routing.receive_LSA_index_then_ask(routings) for routing in routings)
    )
    await asyncio.gather(*(routing.respond_requets(routings) for routing in routings))
    await asyncio.gather(
        *(routing.update_from_neighbors(routings) for routing in routings)
    )
    await asyncio.gather(
        *(routing.update_from_adjacencies(routings) for routing in routings)
    )
    await asyncio.gather(*(routing.send_LSA_index(routings) for routing in routings))
    await asyncio.gather(*(routing.get_adjacencies(routings) for routing in routings))
    await asyncio.gather(*(routing.show_info() for routing in routings))


def modify_LSAs():
    print('=' * 150)
    routings[0].modify_LSA(routings, {2: 1, 4: 1})
    routings[1].modify_LSA(routings, {3: 1})
    routings[2].modify_LSA(routings, {0: 1, 3: 1})
    routings[3].modify_LSA(routings, {1: 1, 2: 1, 0: 1})
    routings[4].modify_LSA(routings, {3: 1, 0: 1})


if __name__ == '__main__':
    for i in range(5):
        main()
        time.sleep(0)
    modify_LSAs()
    for i in range(8):
        main()
        time.sleep(0)
