# ing.alg-itinere2
Algorithm engineering, midterm 2 project



### Traccia 1 - Grado di visibilitá

Sia dato un grafo diretto aciclico pesato *G*, in cui ad ogni nodo *n* è associato un valore 
numerico intero *n.value* e ad ogni arco è associato un <u>peso unitario</u>. Un nodo *n2* in *G* é detto 
<u>visibile</u> da un nodo *n1* in *G* se e solo se valgono <u>entrambe</u> le seguenti condizioni:

- *n1 != n2*
- *n2* è adiacente a *n1* <u>oppure</u> *n1* è connesso a *n2* da un <u>cammino minimo</u> tale che il 
    valore massimo *M* dei nodi intermedi, se presenti, è *M <= n2.value*. 

Si assuma che il cammino minimo, se esiste, è unico.

Il <u>grado di visibilità</u> di un nodo *n* è il numero di nodi visibili da *n*. 

Progettare e implementare un algoritmo che, dato un grafo diretto aciclico non pesato *G*, 
restituisca il nodo *n\** avente il <u>massimo grado di visibilitá</u>.
