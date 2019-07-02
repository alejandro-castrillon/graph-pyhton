from tad.grafos import Grafo, dijkstra
from utilities import clear, read_binary_file, write_binary_file

"""
- matplotlib==3.0.3
- networkx
"""


def test1():
    grafo = Grafo()
    for i in range(1, 6):
        grafo.agregar_nodo(i)

    grafo.conectar_nodos(1, 2, 100)
    grafo.conectar_nodos(1, 3, 30)
    grafo.conectar_nodos(2, 3, 20)
    grafo.conectar_nodos(3, 4, 10)
    grafo.conectar_nodos(3, 5, 60)
    grafo.conectar_nodos(4, 2, 15)
    grafo.conectar_nodos(4, 5, 50)

    return grafo


def test2():
    grafo = Grafo()

    grafo.agregar_nodo("Ca")
    grafo.agregar_nodo("Bo")
    grafo.agregar_nodo("Ct")
    grafo.agregar_nodo("Ba")
    grafo.agregar_nodo("Pe")
    grafo.agregar_nodo("Sa")
    grafo.agregar_nodo("Rn")
    grafo.agregar_nodo("Cu")

    grafo.conectar_nodos("Ca", "Bo", 320)
    grafo.conectar_nodos("Ca", "Pe", 295)
    grafo.conectar_nodos("Ca", "Ct", 2035)
    grafo.conectar_nodos("Ca", "Sa", 1170)
    grafo.conectar_nodos("Bo", "Rn", 500)
    grafo.conectar_nodos("Bo", "Ba", 905)
    grafo.conectar_nodos("Bo", "Cu", 550)
    grafo.conectar_nodos("Ct", "Ba", 415)
    grafo.conectar_nodos("Ba", "Sa", 770)

    return grafo


if __name__ == "__main__":
    clear()

    grafo = test1()

    # write_binary_file("file.ext", grafo)

    print(grafo)
    grafo.eliminar_nodo(3)
    print()
    print(grafo)
    # grafo.graficar()

    # print(read_binary_file("file.ext"))

    # dijkstra.solucionar(grafo)
