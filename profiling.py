from NewGraph_AdjacencyList import GraphAdjacencyList
from time import time


def exp(n):
    """
        Genera 10 grafi aciclici casuali; per ogni grafo esegue 10 volte maxGradoVisibilita() e valuta il tempo medio.
        Infine stampa il tempo medio sui tempi medi dei 10 grafici.

        :param n: il numero di nodi dei grafi che verranno creati
    """
    print("exp(", n, "):")
    tempi = []
    for i in range(20):  # per 20 volte
        graph = GraphAdjacencyList()
        graph.randomGrafoAciclico(n)    # crea un grafo casuale
        total = 0
        for j in range(10):  # misura 10 volte il tempo per quel determinato grafo
            start = time()
            max = graph.maxGradoVisibilita()
            end = time() - start
            total = total + end
        tempi.append(total / 10)
        print("\t\tgrafo", i+1, "tempo medio:", total/10)
    sommamedia = 0
    for t in tempi:
        sommamedia = sommamedia + t
    print("Tempo medio per", n, "nodi :", sommamedia / 20, "\n")  # tempo medio per n nodi


if __name__ == "__main__":

    input = [10, 25, 50]  # 10, 25, 50, 100, 150, 200, 250, 300, 350]
    for i in input:
        exp(i)
