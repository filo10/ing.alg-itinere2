from NewGraph_AdjacencyList import GraphAdjacencyList


if __name__ == "__main__":
    graph = GraphAdjacencyList()

    graph.print()

    nodes = []
    node = graph.addNode(3)
    print("\nNodo inserito:", node)
    nodes.append(node)

    node = graph.addNode(15)
    print("Nodo inserito:", node)
    nodes.append(node)

    node = graph.addNode(2)
    print("Nodo inserito:", node)
    nodes.append(node)

    node = graph.addNode(6)
    print("Nodo inserito:", node)
    nodes.append(node)

    node = graph.addNode(4)
    print("Nodo inserito:", node)
    nodes.append(node)

    node = graph.addNode(9)
    print("Nodo inserito:", node)
    nodes.append(node)

    node = graph.addNode(8)
    print("Nodo inserito:", node)
    nodes.append(node)

    node = graph.addNode(7)
    print("Nodo inserito:", node)
    nodes.append(node)

    node = graph.addNode(5)
    print("Nodo inserito:", node)
    nodes.append(node)

    node = graph.addNode(10)
    print("Nodo inserito:", node, "\n")
    nodes.append(node)

    graph.print()

    graph.insertEdge(0, 1)
    graph.insertEdge(0, 2)
    graph.insertEdge(1, 3)
    graph.insertEdge(3, 4)
    graph.insertEdge(2, 4)
    graph.insertEdge(3, 5)
    graph.insertEdge(3, 6)
    graph.insertEdge(4, 7)
    graph.insertEdge(7, 6)
    graph.insertEdge(6, 9)
    graph.insertEdge(5, 8)

    # graph.insertEdge(2,3) #
    # questo e' un arco per verificare il comportamento dell'algoritmo in caso di piu' cammini minimi tra due nodi.
    # se inserito, il nodo 3 sara' ora visibile dal nodo 0 (come anche il nodo 5, adiacente a 3, ma non il nodo 8).

    print("\nNodi collegati.\n")
    graph.print()

    a = graph.maxGradoVisibilita()

    print("\ngraph.maxGradoVisibilita(): Il nodo con grado di visibilita' maggiore e':", a, "\n")
    for i in range(10):
        print("graph.gradoVisibilita(", i, "): Grado di visibilita' di", i, "=", graph.gradoVisibilita(i))
