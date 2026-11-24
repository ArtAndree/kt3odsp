from data import STATIONS, TYPES, create_city_graph, create_bus_graph
from transport import TransportGraph, NetworkOptimizer


def print_distances(title, distances):
    print("\n" + title)
    for station, distance in distances.items():
        print(f"{station}: {distance:.2f}")


def print_tree(title, result):
    tree, total = result
    print("\n" + title)
    for first, second, weight in tree:
        print(f"{first} — {second}: {weight:.2f} км")
    print(f"Суммарный вес: {total:.2f} км")


def main():
    graph = create_city_graph()
    start = STATIONS[0]
    print("ГОРОДСКАЯ ТРАНСПОРТНАЯ СЕТЬ")
    for i in range(len(STATIONS)):
        print(f"{i + 1}. {STATIONS[i]} ({TYPES[i]})")

    print_distances("Дейкстра от Центрального вокзала (км):",
                    graph.shortest_path_Dijkstra(start))
    print_distances("Беллман — Форд от Центрального вокзала (км):",
                    graph.shortest_path_BellmanFord(start))

    matrix = graph.all_pairs_shortest_paths_FloydWarshall()
    print("\nФлойд — Уоршелл: расстояния в км. Номера соответствуют списку станций.")
    print("    " + "".join(f"{i + 1:>7}" for i in range(len(STATIONS))))
    for i in range(len(matrix)):
        print(f"{i + 1:>3} " + "".join(f"{distance:>7.2f}" for distance in matrix[i]))

    optimizer = NetworkOptimizer(graph)
    print_tree("Минимальная сеть: Крускал", optimizer.minimum_spanning_tree_Kruskal())
    print_tree("Минимальная сеть: Прим", optimizer.minimum_spanning_tree_Prim())

    bus = create_bus_graph()
    print_distances("Автобусный пример с бонусом -3 (условная стоимость):",
                    bus.shortest_path_BellmanFord("Главный вокзал"))

    # Отдельно демонстрируем обнаружение отрицательного цикла.
    cycle = TransportGraph(directed=True)
    cycle.add_route("A", "B", 1)
    cycle.add_route("B", "C", -3)
    cycle.add_route("C", "A", 1)
    print("\nПроверка примера с отрицательным циклом:")
    try:
        cycle.shortest_path_BellmanFord("A")
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()
