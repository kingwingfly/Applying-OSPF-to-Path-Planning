# This module includes the functions of routing
import queue


class Routing:
    def __init__(self, ID, LSA={}) -> None:
        self.ID = ID
        self.LSDB = {ID: LSA}
        self.adjacencies = []
        self.neighbors = list(self.LSDB[self.ID])
        self.hello_queue = queue.Queue()
        self.ask_queue = queue.Queue()
        self.index_queue = queue.Queue()
        self.LSA_queue = queue.Queue()

    async def send_hello(self, routings):
        for neighbor in self.neighbors:
            print(f'{self.ID} sends hello to {neighbor}')
            routings[neighbor].hello_queue.put(self.ID)

    async def check_connection(self):
        neighbors = self.neighbors[::]
        while not self.hello_queue.empty():
            temp = self.hello_queue.get()
            if temp not in self.neighbors:
                self.neighbors.append(temp)
                # 新邻居 cost 1
                self.LSDB[self.ID][temp] = 1
            else:
                neighbors.remove(temp)
        for i in neighbors:
            # 断路
            self.neighbors.remove(i)
            self.LSDB[self.ID].pop(i)

    async def send_LSA_index(self, routings):
        for neighbor in self.neighbors:
            print(f'{self.ID} sends LSA index to {neighbor}')
            routings[neighbor].index_queue.put((self.ID, list(self.LSDB)))

    async def receive_LSA_index_then_ask(self, routings):
        # TODO 此任务应当一直运行
        while not self.index_queue.empty():
            source, IDs = self.index_queue.get()
            for ID in IDs:
                if ID not in list(self.LSDB):
                    print(f'{self.ID} asks {source} for {ID}\'s LSA')
                    routings[source].ask_queue.put((self.ID, ID))

    async def respond_requets(self, routings):
        while not self.ask_queue.empty():
            needer, ID = self.ask_queue.get()
            print(f'{self.ID} sends {needer} {ID}\'s LSA')
            routings[needer].LSA_queue.put((ID, self.LSDB[ID]))

    async def receive_LSA_then_update(self, routings):
        # TODO 触发更新时向邻接发送更新信息
        while not self.LSA_queue.empty():
            ID, LSA = self.LSA_queue.get()
            self.LSDB[ID] = LSA


# TODO 判断是否邻接
