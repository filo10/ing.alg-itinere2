"""
    Briscese Filippo Maria
    0228612

    Prova Pratica - Seconda Prova in Itinere
    Traccia 1 - Grado di visibilita'
        Sia dato un grafo diretto aciclico pesato G, in cui ad ogni nodo n e' associato un valore
        numerico intero n.value e ad ogni arco e' associato un peso unitario. Un nodo n2 in G e' detto
        visibile da un nodo n1 in G se e solo se valgono entrambe le seguenti condizioni:
            - n1 != n2
            - n2 e' adiacente a n1 oppure n1 e' connesso a n2 DA UN CAMMINO MINIMO tale che il valore
              massimo M dei nodi intermedi, se presenti, e' M <= n2.value .
        Si assuma che il cammino minimo, se esiste, e' unico.
        Il grado di visibilita' di un nodo n e' il numero di nodi visibili da n.

        Progettare e implementare un algoritmo che, dato un grafo diretto aciclico non pesato G,
        restituisca il nodo n* avente il massimo grado di visibilita'.


    Base di partenza: graph.Graph_AdjacencyList.py
    Ora GraphAdjacencyList ha un nuovo attributo, distanze.
    Sono state apportate modifiche ai metodi:
        - addNode           a partire da riga 69
        - deleteNode        a partire da riga 82
        - insertEdge        a partire da riga 136
        - deleteEdge        a partire da riga 151

    Sono stati aggiunti nuovi metodi (distanzaDaNodo, aggiornaDistanze, gradoVisibilita, maxGradoVisibilita,
    randomGrafoAciclico) a partire da riga 257.

    Python 3.6
"""

from graph.Graph import GraphBase
from graph.base import Edge
from queue.Queue import CodaArrayList_deque as Queue
from stack.Stack import PilaArrayList as Stack
from list.DoubleLinkedList import ListaDoppiamenteCollegata as List
import random

random.seed()


class GraphAdjacencyList(GraphBase):
    """
        Un grafo, implementato con liste di adiacenza.
        Ogni nodo u ha una lista contenente i suoi nodi adiacenti,
        che sono i nodi v tali che esiste un arco (u,v).
        Inoltre il grafo ha un attributo "distanze" in cui sono salvate le distanze tra due nodi.
    """

    def __init__(self):    # nuovo codice qui
        """
        Constructor.
        """
        super().__init__()
        self.adj = {} # adjacency lists {nodeID:listOfAdjacentNodes}
        self.distanze = {}  # dizionario di dizionari {nodeID1:{nodeID2:distanza} ( == {nodeID2:{nodeID1:distanza} )
        # {ID1:{ID2:dist} => ID1 dista da ID 2: dist
        # in self.distanze e' possibile quindi trovare velocemente le distanze tra due nodi.

    def numEdges(self):
        """
        Return the number of edges.
        :return: the number of edges.
        """
        return sum(len(adj_list) for adj_list in self.adj.values())

    def addNode(self, elem):    # nuovo codice qui
        """
        Add a new node with the specified value.
        :param elem: the node value.
        :return: the create node.
        """
        newnode = super().addNode(elem) # create a new node with the correct ID

        self.nodes[newnode.id] = newnode # add the new node to the dictionary
        self.adj[newnode.id] = List() # create the adjacency list for the new node
        self.distanze.update({newnode.id: {newnode.id: 0}}) # un nodo e' distante da se stesso 0.
        return newnode

    def deleteNode(self, nodeId):   # nuovo codice qui
        """
        Remove the specified node.
        :param nodeId: the node ID (integer).
        :return: void.
        """

        # look for the node
        found = False
        for node in self.nodes.items():
            if nodeId == node[0]:
                found = True
                break

        # if node does not exist, return
        if not found: return

        # remove the node from the set of nodes, that is to remove the node
        # from the dictionary nodes
        del self.nodes[nodeId]

        # remove all edges starting from the node, that is to remove the
        # adjacency list for the node
        del self.adj[nodeId]

        # rimuovi le distanze ora inesistenti
        self.distanze.pop(nodeId)   # rimuovo dal dizionario distanze il dizionario con le distanze da nodeId
        for key in self.distanze.keys():    # rimuovo le distanze degli altri nodi a nodeId
            self.distanze[key].pop(nodeId, None)

        # remove all edges pointing to the node, that is to remove the node
        # from all the adjacency lists
        for adj in self.adj.values():
            curr = adj.getFirstRecord()
            while curr is not None:
                if curr.elem == nodeId:
                    adj.deleteRecord(curr)
                curr = curr.next

    def getNode(self, id):
        """
        Return the node, if exists.
        :param id: the node ID (integer).
        :return: the node, if exists; None, otherwise.
        """
        return None if id not in self.nodes else self.nodes[id]

    def getNodes(self):
        """
        Return the list of nodes.
        :return: the list of nodes.
        """
        return list(self.nodes.values())

    def insertEdge(self, tail, head, weight=None):  # nuovo codice qui
        """
        Add a new edge.
        :param tail: the tail node ID (integer).
        :param head: the head node ID (integer).
        :param weight: the (optional) edge weight (floating-point).
        :return: the created edge, if created; None, otherwise.
        """
        # if tail and head exist, add the entry into the adjacency list
        if tail in self.nodes and head in self.nodes: #TODO overwrite if edge already exists
            self.adj[tail].addAsLast(head)
        # se collego due nodi, la distanza tra loro sara' 1
        self.distanze[tail].update({head:1})
        self.distanze[head].update({tail: 1})

    def deleteEdge(self, tail, head):   # nuovo codice qui
        """
        Remove the specified edge.
        :param tail: the tail node ID (integer).
        :param head: the head node ID (integer).
        :return: void.
        """
        # if tail and head exist, delete the edge
        if tail in self.nodes and head in self.nodes:
            curr = self.adj[tail].getFirstRecord()
            while curr is not None:
                if curr.elem == head:
                    self.adj[tail].deleteRecord(curr)
                    break
                curr = curr.next
        if head in self.distanze[tail].keys():  # se l'arco (tail, head) esiste, rimuovo la distanza tra tail e head
            self.distanze[tail].pop(head)
        if tail in self.distanze[head].keys():
            self.distanze[head].pop(tail)

    def getEdge(self, tail, head):
        """
        Return the node, if exists.
        :param tail: the tail node ID (integer).
        :param head: the head node ID (integer).
        :return: the edge, if exists; None, otherwise.
        """
        if tail in self.nodes and head in self.nodes:
            curr = self.adj[tail].getFirstRecord()
            while curr is not None:
                if curr.elem == head:
                    return Edge(tail, head, None)
                curr = curr.next
        return None

    def getEdges(self):
        """
        Return the list of edges.
        :return: the list of edges.
        """
        edges = []
        for adj_item in self.adj.items():
            curr = adj_item[1].getFirstRecord()
            while curr is not None:
                edges.append(Edge(adj_item[0], curr.elem, None))
                curr = curr.next
        return edges

    def isAdj(self, tail, head):
        """
        Checks if two nodes ar adjacent.
        :param tail: the tail node ID (integer).
        :param head: the head node ID (integer).
        :return: True, if the two nodes are adjacent; False, otherwise.
        """
        # if tail and head exist, look for the entry in the adjacency list
        if super().isAdj(tail, head) == True:
            curr = self.adj[tail].getFirstRecord()
            while curr is not None:
                nodeId = curr.elem
                if nodeId == head:
                    return True
                curr = curr.next

        # else, return False
        return False

    def getAdj(self, nodeId):
        """
        Return all nodes adjacent to the one specified.
        :param nodeId: the node id.
        :return: the list of nodes adjacent to the one specified.
        """
        result = []
        curr = self.adj[nodeId].getFirstRecord()
        while curr is not None:
            result.append(curr.elem)
            curr = curr.next
        return result

    def deg(self, nodeId):
        """
        Return the node degree.
        :param nodeId: the node id.
        :return: the node degree.
        """
        if nodeId not in self.nodes:
            return 0
        else:
            return len(self.adj[nodeId])

    def print(self):
        """
        Print the graph.
        :return: void.
        """
        # if the adjacency list is empty ...
        if self.isEmpty():
            print ("Adjacency List: EMPTY")
            return

        # else ...
        print("Adjacency Lists:")
        for adj_item in self.adj.items():
            print("{}:{}".format(adj_item[0], adj_item[1]))

# - Nuovi metodi -------------------------------------------------------------------------------------------------------

    def distanzeDaNodo(self, rootId):
        """
        Visita il grafo in ampiezza (BFS), e lungo il tragitto aggiorna le distanze dei nodi da root.

        :param rootId: ID del nodo dal quale si vogliono sapere le distanze
        :return: La lista dei nodi visitati in ampiezza
                 + SIDE EFFECT: aggiorna self.distanze per (root, u), per ogni u appartenenente a V
        """

        # se root non esiste, ritorna None
        if rootId not in self.nodes:
            return None

        # inizializzazioni
        bfs_nodes = []
        q = Queue()
        q.enqueue([rootId, 0])

        explored = {rootId}  # nodes already explored

        while not q.isEmpty():  # finche' ci sono nodi da esplorare
            node = q.dequeue()  # prendi il nodo dalla coda
            self.distanze[rootId].update({node[0]: node[1]})
            self.distanze[node[0]].update({rootId: node[1]})
            explored.add(node[0])  # segnalo come esplorato
            # aggiungi tutti i nodi adiacenti inesplorati alla coda
            for adj_node in self.getAdj(node[0]):
                if adj_node not in explored:
                    q.enqueue([adj_node, node[1] + 1])
                    explored.add(adj_node)  # questa linea risolve un bug nel codice visto in aula per le visite BFS...
            bfs_nodes.append(node)
        return bfs_nodes    # continua riga 288: ...il bug consisteva nell'aggiungere 2 volte in bfs_nodes l'ultimo nodo

    def aggiornaDistanze(self):
        """
        Aggiorna tutte le distanze (u, v) per ogni u, v appartenenti a V.

        :return: SIDE EFFECT
        """
        for id in self.nodes.keys():
            self.distanzeDaNodo(id)

    def gradoVisibilita(self, rootId):
        """
        Visita il grafo in "pseudo-profondita'" (ovvero continua la sua visita in profondita' solo se un nodo viene
        visitato dal cammino minimo che lo unisce al nodo di partenza) per sapere il numero di nodi visibili da root.

        :param rootId: ID del nodo di cui bisogna calcolare il grado di visibilita'.
        :return: Il grado di visibilita' di root.
        """
        # se la radice non esiste, ritorna None
        if rootId not in self.nodes:
            return None

        # vedo quanto distano ogni nodo del grafo da root
        self.distanzeDaNodo(rootId)

        # inizializzazione lista
        visibili = []

        # inizializzazione stack
        f = Stack()  # first stack; utilizzato perche' i nodi subito adiacenti a root sono visibili indipendentemente...
        # ...dal loro valore, quindi non devono essere esaminati con i controlli del secondo while
        s = Stack()  # second stack; per analizzare gli altri nodi

        d = 0  # distanza da root
        f.push({rootId: d})

        explored = {rootId}  # nodi gia' esplorati

        while not f.isEmpty():
            node = f.pop()  # un dizionario con una sola coppia chiave:valore
            nodo = node.popitem()  # tupla: (id, distanza)
            idnodo = nodo[0]  # id
            explored.add(idnodo)  # aggiorna il dizionario explored con gli elementi del dizionario node
            # aggiungi tutti i nodi adiacenti alla radice inesplorati al second stack
            for adj_node in self.getAdj(idnodo):
                if adj_node not in explored:
                    s.push({adj_node: nodo[1] + 1})
            visibili.append(idnodo)

        while not s.isEmpty():
            node = s.pop()  # un dizionario con una sola coppia chiave:valore
            nodo = node.popitem()  # tupla: (id, distanza)
            idnodo = nodo[0]  # id
            explored.add(idnodo)  # aggiorna il dizionario explored con gli elementi del dizionario node
            # aggiungi tutti i nodi adiacenti inesplorati che stai visitando passando per un cammino minimo allo stack
            for adj_node in self.getAdj(idnodo):
                if self.getNode(adj_node).value > self.getNode(idnodo).value: # and adj_node not in explored:
                    actDist = nodo[1] + 1  # distanza di adj_node da root passando per questo cammino
                    # per verificare se sto visitando adj_node passando dal cammino minimo
                    if actDist == self.distanze[rootId][adj_node]:
                        s.push({adj_node: actDist})
            visibili.append(idnodo)

        return len(visibili) - 1  # -1 perche' in visibili e' compreso il nodo stesso

    def maxGradoVisibilita(self):
        """
        Trova il nodo con grado di visibilita' massimo.

        :return: ID del nodo con grado di visibilita' massimo.
        """
        max = 0
        idmax = None
        for id in self.nodes.keys():
            deg = self.gradoVisibilita(id)
            if deg > max:
                max = deg
                idmax = id
        return idmax

    def randomGrafoAciclico(self, n):
        """
            Crea un grafo diretto aciclico casuale.
            Un grafo e' aciclico se la sua matrice di adiacenza e' triangolare superiore
            ovvero se non esistono archi (u, v) con u > v. [ da dimostrare...]
            (l'ordine degli indici della matrice deve essere l'ordinamento topologico)

            Il grafo generato dalla funzione qui sotto non crea necessariamente un grafo con nodi collegati
            tra loro da cammini minimi unici.
            Esistera' almeno un nodo senza archi entranti e uno senza archi uscenti.

            Per semplicita' gli archi avranno peso None.

            :param n: numero di nodi
            :return: grafo creato
        """
        if self.nodes.keys():   # se il grafo ha dei nodi gia' inseriti
            print('Il grafo deve essere "vuoto"')
            return None
        for i in range(n):  # creo i nodi
            valore = random.randint(0, 1000)
            self.addNode(valore)
        for i in range(n - 1):  # collego i nodi; non verranno creati archi (u, v) tali che u > v.
            successivi = range(i + 1, n)  # intervallo (i, n)
            numPuntati = random.randint(0, n - 1 - i)  # quanti archi usciranno da i; | puntati | = numPuntati
            puntati = random.sample(successivi, numPuntati)  # scegli quali nodi "puntare"
            for s in puntati:  # inserisci quindi gli archi
                self.insertEdge(i, s)
        # cerca i nodi che non hanno alcun arco entrante e uscente, collegali con un arco al grafo
        pozzi = set()  # qui ci andranno tutti i nodi dai quali non esce alcun arco
        for nodo in self.nodes.keys():
            if not self.getAdj(nodo):
                pozzi.add(nodo)
        nodiNonPuntati = set()  # qui ci andranno tutti i nodi nei quali non entra alcun arco
        for id in self.nodes.keys():    # nodiNonPuntati inizialmente sara' la lista di tutti i nodi
            nodiNonPuntati.add(id)
        for puntatore in self.nodes.keys():
            for puntato in self.getAdj(puntatore):  # se un nodo e' "puntato"
                nodiNonPuntati.discard(puntato)     # rimuovilo dall'insieme dei nodi non puntati
        nodiIsolati = pozzi.intersection(nodiNonPuntati)   # intersezione tra pozzi e nodiNonPuntati sono i nodi voluti
        for isolato in nodiIsolati:     # per ogni nodo isolato, fai in modo che sia connesso al grafo
            if isolato - 1 < 1:
                self.insertEdge(isolato, random.randint(isolato + 1, n - 1))
            else:
                puntatore = random.randint(0, isolato - 1)
                self.insertEdge(puntatore, isolato)
        return self


if __name__ == "__main__":
    graph = GraphAdjacencyList()

    graph.print()

    # add nodes
    nodes = []
    for i in range(3):
        node = graph.addNode(i)
        print("Node inserted:", node)
        nodes.append(node)

    graph.print()

    # connect all nodes
    for node_src in nodes:
        for node_dst in nodes:
            if node_src != node_dst:
                print("---")
                print("Adjacent nodes {},{}: {}"
                      .format(node_src.id, node_dst.id,
                              graph.isAdj(node_src.id, node_dst.id)))
                graph.insertEdge(node_src.id, node_dst.id,
                                 node_src.id + node_dst.id)
                print("Edge inserted: from {} to {}".format(node_src.id,
                                                            node_dst.id))
                print("Adjacent nodes {},{}: {}"
                      .format(node_src.id, node_dst.id,
                              graph.isAdj(node_src.id, node_dst.id)))
                graph.print()
                print("---")

    # num nodes/edges
    print("Num Nodes:", graph.numNodes())
    print("Num Edges:", graph.numEdges())

    # degree
    for node in nodes:
        print("Degree node {}: {}".format(node.id, graph.deg(node.id)))

    # get specific node
    for node in nodes:
        print("Node {}: {}".format(node.id, graph.getNode(node.id)))

    # get all nodes
    print("Nodes:", [str(i) for i in graph.getNodes()])

    # get specific edge
    for node_src in nodes:
        for node_dst in nodes:
            print("Edge {},{}: {}".format(node_src.id, node_dst.id, graph.getEdge(node_src.id, node_dst.id)))

    # get all edges
    print("Edges:", [str(i) for i in graph.getEdges()])

    # execute a generic search
    for node in nodes:
        tree = graph.genericSearch(node.id)
        s = tree.BFS()
        print("Generic Search with root {}: {}".format(node.id,
                                               [str(item) for item in s]))

    # execute a BFS
    for node in nodes:
        s = graph.bfs(node.id)
        print("BFS with root {}: {}".format(node.id,
                                               [str(item) for item in s]))

    # execute a DFS
    for node in nodes:
        s = graph.dfs(node.id)
        print("DFS with root {}: {}".format(node.id,
                                               [str(item) for item in s]))

    # remove all nodes
    for node in nodes:
        graph.deleteNode(node.id)
        print("Node removed:", node.id)
        graph.print()