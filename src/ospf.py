from __future__ import annotations
import asyncio


states = {
    1: 'Down',
    1.5: 'Attempt',
    2: 'Init',
    3: '2-way',
    4: 'Exstart',
    5: 'Exchange',
    6: 'Loading',
    7: 'Full',
}

status = {
    1: 'DR',
    2: 'BDR',
    3: 'RTothers',
    4: 'ABR',
    5: 'ASBR',
}

LSA_types = {
    1: [1, 2, 3, 4, 5],
    2: [1, 2, 3, 4, 5],
    3: [1, 2, 3, 5],
    4: [1, 2, 3, 4, 5],
    5: [1, 2],
    7: [5],
}

Area_types = {
    1: 'Area0',
    2: 'AreaOtherNotStub',
    3: 'Stub',
    4: 'TotalStub',
    5: 'Nssa',
}


class Routing:
    # todo auth与password认证
    def __init__(
        self,
        Id: int,
        priority: int,
        AreaId: int,
        version: str,
        neighbors: list[Routing],
    ) -> None:
        self.Id = Id
        self.priority = priority
        self.AreaId = AreaId
        self.version = version
        self.neighbors: dict[int, Routing] = {}
        self.connection_states: dict[int, int] = {}
        for neighbor in neighbors:
            self.save(neighbor)
            self.chstt(neighbor, 1)
        self.statu = 2 if self.priority != 0 else 3
        self.DR = None
        self.BDR = Id if self.priority != 0 else None
        self.wait_time = 1
        self.hello_queue = asyncio.Queue()

    def modify_neighbors(self, neighbors: list[Routing]):
        """修改邻居

        Args:
            neighbors list[Routing]: 新的邻居的Routing对象列表
        """
        self.neighbors: dict[int, Routing] = {}
        for neighbor in neighbors:
            self.save(neighbor)
            self.chstt(neighbor, 1)

    def modify_Id(self, Id: int):
        self.Id = Id

    def modify_AreaId(self, AreaId: int):
        self.AreaId = AreaId

    def modify_priority(self, priority: int):
        self.priority = priority

    def generate_hello(self):
        """Hello包,
        用于发现和维持邻居关系, 选举DR和BDR
        """
        return (
            self.statu,
            self.Id,
            self.priority,
            self.AreaId,
            self.version,
            self,
            self.neighbors.values(),
            self.DR,
            self.BDR,
        )

    def generate_DBD():
        """数据库描述包(DBD),
        用于向邻居发送摘要信息以同步链路状态数据库
        """
        ...

    def generate_LSR():
        """链路状态请求包(LSR),
        在路由器收到包含新信息的DBD后发送, 用于请求更详细的信息
        """
        ...

    def generate_LSU():
        """链路状态更新包(LSU),
        收到LSR后发送链路状态通告(LSA), 一个LSU数据包可能包含几个LSA
        """
        ...

    def generate_LSAck():
        """链路状态确认包(LSAck),
        确认已经收到DBD/LSU, 每个LSA需要被分别确认
        """
        ...

    def save(self, neighbor: Routing):
        """传入一个Routing对象
        将其Id与其关联并存于neighbors中

        Args:
            neighbor (Routing): Routing对象
        """
        self.neighbors[neighbor.Id] = neighbor

    def chstt(self, neighbor: Routing, state: int):
        """change state 的缩写
        修改与neighbor的连接状态

        Args:
            neighbor (Routing): 需要修改连接状态的Routing对象
            state (int): 修改后的状态码
        """
        self.connection_states[neighbor.Id] = state

    def get_neighbor(self, Id: id) -> Routing:
        """通过Id从neighbors中取得Routing对象

        Args:
            Id (int): 想取得的Routing对象的Id

        Returns:
            Routing: 对应Id的Routing对象
        """
        return self.neighbors[Id]

    def get_state(self, Id: int) -> int:
        """通过Id取得于该Id对应Routing对象连接的状态码

        Args:
            Id (int): 需要被获取连接状态码的Routing对象

        Returns:
            int: 状态码
        """
        return self.connection_states[Id]

    async def send_hello(self):
        while True:
            msg = self.generate_hello()
            for neighbor in self.neighbors.values():
                neighbor.hello_queue.put_nowait(msg)
                # 发送信息未得到回应，链路状态为attempt
                self.chstt(neighbor, 1.5)
            await asyncio.sleep(self.wait_time)
        # todo 四轮hello没有得到回应，状态从attempt回到down

    async def process_hello(self):
        while True:
            (
                statu,
                Id,
                priority,
                AreaId,
                version,
                neighbor,
                neighbors,
                dr,
                bdr,
            ) = await self.hello_queue.get()
            if Id == self.Id or AreaId != self.AreaId or version != self.version:
                continue
            self.save(neighbor)
            if self not in neighbors:
                # 收到邻居的hello，但自身不在对方邻居列表中，链路状态为init
                self.chstt(neighbor, 2)
            else:
                # 收到邻居的hello，自身在对方邻居列表中，链路状态为2-way
                self.chstt(neighbor, 3)
            if self.get_state(Id) == 3 and 3 > statu:
                if priority > self.priority:
                    # 对方优先级高，自己不再是BDR
                    self.statu = max(self.statu, 3)
                    self.BDR = bdr
                elif priority == self.priority:
                    if Id > self.Id:
                        self.statu = max(self.statu, 3)
                        self.BDR = bdr


class Area:
    def __init__(self):
        ...


def get_neighbors(routings: list[Routing], lst: list[int]):
    for i in lst:
        yield routings[i]


if __name__ == '__main__':
    routings = [Routing(i, 0, 0, '0.1.0', []) for i in range(5)]
    routing = Routing(5, 0, 0, '0.1.0', [])
    rest = routing
    print(rest)
