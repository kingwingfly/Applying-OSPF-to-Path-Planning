# This module includes the functions of routing
import queue


class Routing:
    def __init__(self, ID, LSA={}) -> None:
        self.ID = ID
        self.LSDB = {ID: LSA}
        self.adjacencies = []
        self.neighbors = list(self.LSDB[self.ID])
        self.hello_queue = queue.Queue()
        self.index_queue = queue.Queue()
        self.ask_queue = queue.Queue()
        self.LSA_queue = queue.Queue()
        self.from_adjacencies_queue = queue.Queue()

    def modify_LSA(self, routings, LSA):
        self.neighbors = list(self.LSDB[self.ID])
        self.LSDB[self.ID] = LSA
        for i in self.adjacencies:
            if i not in list(self.LSDB[self.ID]):
                self.adjacencies.remove(i)
        self._tell_adjacencies(routings, self.ID, LSA, [])

    async def send_hello(self, routings):
        for neighbor in list(self.LSDB[self.ID]):
            print(f'{self.ID} sends hello to {neighbor}')
            routings[neighbor].hello_queue.put((self.ID, self.LSDB[self.ID][neighbor]))

    async def check_connection(self, routings):
        while not self.hello_queue.empty():
            ID, cost = self.hello_queue.get()
            if not (ID in list(self.LSDB[self.ID]) or ID in self.neighbors):
                print(f'{self.ID} is one-way connected by {ID}')
            elif ID in list(self.LSDB[self.ID]) and ID not in self.neighbors:
                print(f'{self.ID} new connects with {ID}')
                self._tell_adjacencies(routings, self.ID, self.LSDB[self.ID], [])
            elif ID not in list(self.LSDB[self.ID]):
                print(
                    f'{self.ID} disconnects {ID}, but {ID} can still connect to {self.ID}'
                )
                self._tell_adjacencies(routings, self.ID, self.LSDB[self.ID], [])
        self.neighbors = list(self.LSDB[self.ID])

    async def send_LSA_index(self, routings):
        for neighbor in list(self.LSDB[self.ID]):
            print(f'{self.ID} sends LSA index to {neighbor}')
            routings[neighbor].index_queue.put((self.ID, list(self.LSDB)))

    async def receive_LSA_index_then_ask(self, routings):
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

    async def update_from_neighbors(self, routings):
        while not self.LSA_queue.empty():
            ID, LSA = self.LSA_queue.get()
            self.LSDB[ID] = LSA
            self._tell_adjacencies(routings, ID, LSA, [])

    async def get_adjacencies(self, routings):
        while not self.index_queue.empty():
            ID, LSA_index = self.index_queue.get()
            if ID not in self.adjacencies and set(self.LSDB) == set(LSA_index):
                self.adjacencies.append(ID)

    async def update_from_adjacencies(self, routings):
        while not self.from_adjacencies_queue.empty():
            ID, LSA, white_IDs = self.from_adjacencies_queue.get()
            self.LSDB[ID] = LSA
            self._tell_adjacencies(routings, ID, LSA, white_IDs[::])

    def _tell_adjacencies(self, routings, ID, LSA, white_IDs):
        white_IDs.append(self.ID)
        for adjacency in self.adjacencies:
            if adjacency in white_IDs:
                continue
            print(
                f'{self.ID} tells adjacency {adjacency} new LSA: {LSA} white_IDs: {white_IDs} {id(white_IDs)}'
            )
            routings[adjacency].from_adjacencies_queue.put((ID, LSA, white_IDs))

    async def show_info(self):
        print(f'{self.ID}:\n{self.LSDB}')
        print(f'{self.adjacencies}')
        print(f'{list(self.LSDB[self.ID])}')
