from transport import TransportGraph


STATIONS = [
    "Центральный вокзал",
    "Пл. Ленина",
    "Автостанция-1",
    "Университет",
    "Вокзал-Северный",
    "Автостанция-2",
    "Парковая",
    "Портовая",
]

TYPES = ["ж/д", "метро", "автобус", "метро", "ж/д", "автобус", "метро", "автобус"]

# None означает отсутствие прямого маршрута. Расстояния в километрах.
MATRIX = [
    [0,    1.2,  3.5,  None, 4.0,  None, None, None],
    [1.2,  0,    2.1,  0.8,  None, 3.0,  1.5,  None],
    [3.5,  2.1,  0,    None, None, 5.4,  None, 4.2],
    [None, 0.8,  None, 0,    2.7,  1.9,  None, None],
    [4.0,  None, None, 2.7,  0,    None, 3.3,  6.0],
    [None, 3.0,  5.4,  1.9,  None, 0,    2.5,  None],
    [None, 1.5,  None, None, 3.3,  2.5,  0,    None],
    [None, None, 4.2,  None, 6.0,  None, None, 0],
]


def create_city_graph():
    graph = TransportGraph()
    for station in STATIONS:
        graph.add_station(station)
    for i in range(len(STATIONS)):
        for j in range(i + 1, len(STATIONS)):
            if MATRIX[i][j] is not None:
                graph.add_route(STATIONS[i], STATIONS[j], MATRIX[i][j])
    return graph


def create_bus_graph():
    # Отдельный ориентированный пример: отрицательный вес — условный бонус,
    # а не физическое расстояние. Отрицательных циклов здесь нет.
    graph = TransportGraph(directed=True)
    graph.add_route("Главный вокзал", "Автостанция", 4)
    graph.add_route("Главный вокзал", "Пересадка", 5)
    graph.add_route("Пересадка", "Автостанция", -3)
    graph.add_route("Автостанция", "Порт", 2)
    return graph
