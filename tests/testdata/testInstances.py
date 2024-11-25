from src.witnessproblem import Graph, Instance, Testimony

def get_tiny_instances():
    with open('instances/tiny.txt') as inFile:
        instances: list[Instance] = Instance.schema().loads(inFile.readline(), many=True)
        [instance.graph.applyFloyd() for instance in instances]
    return instances

def grid_graph_instance():
    graph = Graph()
    graph.createGridGraph(3, 1)
    instance = Instance(graph, get_grid_graph_testimonies())
    return instance


def grid_graph_instance_2():
    graph = Graph()
    graph.createGridGraph(3, 1)
    instance = Instance(graph, [[testimony] for witness in get_grid_graph_testimonies() for testimony in witness])
    return instance


def get_grid_graph_testimonies():
    return [
        [
            Testimony(possibleVertices=[3], a=0, b=2),
            Testimony(possibleVertices=[1, 7], a=3, b=4),
        ],
        [
            Testimony(possibleVertices=[2, 4], a=1, b=1),
        ],
        [
            Testimony(possibleVertices=[1, 3], a=2, b=3),
            Testimony(possibleVertices=[8], a=0, b=2),
        ],
        [
            Testimony(possibleVertices=[6, 7], a=1, b=4),
            Testimony(possibleVertices=[1, 4], a=0, b=1),
        ],
        [
            Testimony(possibleVertices=[2, 5], a=2, b=3),
        ],
        [
            Testimony(possibleVertices=[3, 8], a=1, b=4),
            Testimony(possibleVertices=[1, 5], a=0, b=2),
        ],
        [
            Testimony(possibleVertices=[3, 5], a=1, b=1),
            Testimony(possibleVertices=[7], a=2, b=4),
        ],
    ]