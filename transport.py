from heapq import heappop, heappush
from math import inf


class TransportGraph:
    def __init__(self, directed=False):
        self.graph = {}
        self.directed = directed

    def add_station(self, name):
        if name not in self.graph:
            self.graph[name] = {}

    def add_route(self, from_station, to_station, weight):
        self.add_station(from_station)
        self.add_station(to_station)
        self.graph[from_station][to_station] = weight
        if not self.directed:
            self.graph[to_station][from_station] = weight

    def shortest_path_Dijkstra(self, start):
        if start not in self.graph:
            raise ValueError("Такой станции нет")
        for neighbors in self.graph.values():
            for weight in neighbors.values():
                if weight < 0:
                    raise ValueError("Дейкстра не работает с отрицательными весами")

        distances = {station: inf for station in self.graph}
        distances[start] = 0
        queue = [(0, start)]

        while queue:
            distance, station = heappop(queue)
            if distance > distances[station]:
                continue
            for neighbor, weight in self.graph[station].items():
                new_distance = distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heappush(queue, (new_distance, neighbor))
        return distances

    def shortest_path_BellmanFord(self, start):
        if start not in self.graph:
            raise ValueError("Такой станции нет")
        distances = {station: inf for station in self.graph}
        distances[start] = 0

        # Расслабляем все рёбра не более V - 1 раз.
        for _ in range(len(self.graph) - 1):
            changed = False
            for station in self.graph:
                for neighbor, weight in self.graph[station].items():
                    if distances[station] + weight < distances[neighbor]:
                        distances[neighbor] = distances[station] + weight
                        changed = True
            if not changed:
                break

        # Ещё одно улучшение означает достижимый отрицательный цикл.
        for station in self.graph:
            for neighbor, weight in self.graph[station].items():
                if distances[station] + weight < distances[neighbor]:
                    raise ValueError("Обнаружен отрицательный цикл")
        return distances

    def all_pairs_shortest_paths_FloydWarshall(self):
        stations = list(self.graph)
        size = len(stations)
        indexes = {name: i for i, name in enumerate(stations)}
        distances = [[inf] * size for _ in range(size)]

        for i in range(size):
            distances[i][i] = 0
        for station in self.graph:
            for neighbor, weight in self.graph[station].items():
                i, j = indexes[station], indexes[neighbor]
                distances[i][j] = min(distances[i][j], weight)

        for k in range(size):
            for i in range(size):
                for j in range(size):
                    distances[i][j] = min(
                        distances[i][j], distances[i][k] + distances[k][j]
                    )

        for i in range(size):
            if distances[i][i] < 0:
                raise ValueError("Обнаружен отрицательный цикл")
        return distances


class NetworkOptimizer:
    def __init__(self, graph):
        if graph.directed:
            raise ValueError("Остовное дерево строится для неориентированного графа")
        self.graph = graph.graph

    def minimum_spanning_tree_Kruskal(self):
        # Берём каждое неориентированное ребро только один раз.
        edges = []
        visited = set()
        for station in self.graph:
            visited.add(station)
            for neighbor, weight in self.graph[station].items():
                if neighbor not in visited:
                    edges.append((station, neighbor, weight))
        edges.sort(key=lambda edge: edge[2])

        parent = {station: station for station in self.graph}

        def find(station):
            while parent[station] != station:
                parent[station] = parent[parent[station]]
                station = parent[station]
            return station

        tree = []
        total = 0
        for first, second, weight in edges:
            root_first, root_second = find(first), find(second)
            if root_first != root_second:
                parent[root_first] = root_second
                tree.append((first, second, weight))
                total += weight

        if self.graph and len(tree) != len(self.graph) - 1:
            raise ValueError("Граф несвязный: соединить все станции нельзя")
        return tree, total

    def minimum_spanning_tree_Prim(self):
        if not self.graph:
            return [], 0
        start = next(iter(self.graph))
        visited = {start}
        queue = []
        for neighbor, weight in self.graph[start].items():
            heappush(queue, (weight, start, neighbor))

        tree = []
        total = 0
        while queue:
            weight, first, second = heappop(queue)
            if second in visited:
                continue
            visited.add(second)
            tree.append((first, second, weight))
            total += weight
            for neighbor, edge_weight in self.graph[second].items():
                if neighbor not in visited:
                    heappush(queue, (edge_weight, second, neighbor))

        if len(visited) != len(self.graph):
            raise ValueError("Граф несвязный: соединить все станции нельзя")
        return tree, total
