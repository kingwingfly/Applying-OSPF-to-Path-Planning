import asyncio
from queue import Queue

class Routing:
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
        3: 'ABR',
        4: 'ASBR',
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

    def __init__(self, Id) -> None:
        self.state_code = 1
        self.Id = Id
        self.neighbors: list[Routing] = []
        self.hello_queue = Queue()

    def generate_hello(self):
        """Hello包,
        用于发现和维持邻居关系, 选举DR和BDR
        """
        return (self, self.neighbors)

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

    def send_hello(self):
        msg = self.generate_hello()
        for neighbor in self.neighbors:
            neighbor.hello_queue.put(msg)
            self.state_code = 1.5
        for (sender, neighbors) in self.hello_queue:
            if self not in neighbors:
                self.state_code = 2
                self.neighbors.append(sender)
            else:
                self.state_code = 3

    def 
        


class Area():
    def __init__(self):
        ...

if __name__ == '__main__':
    routing = Routing(1)
    rest = routing
    print(rest)
