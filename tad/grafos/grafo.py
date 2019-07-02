from tad.grafos.nodos import NodoGrafo as Nodo

from graph.GraphPro import GraphPro as Graph


class Grafo:
    def __init__(self):
        self.nodos = []

    def __str__(self):
        if self.nodos:
            return "\n".join([f"{i}{i.conecciones}" for i in self.nodos])
        else:
            raise Exception("El grafo esta vacio")

    def agregar_nodo(self, nombre):
        if not self.buscar(nombre):
            self.nodos.append(Nodo(nombre))
        else:
            raise Exception(f"El nodo '{nombre}' ya existe")

    def eliminar_nodo(self, nombre):
        nodo = self.buscar(nombre)
        if not nodo:
            raise Exception(f"El nodo {nombre} no existe")

        self.nodos.remove(nodo)

        for i in self.nodos:
            for j in range(len(i.conecciones)):
                for k in i.conecciones:
                    nodo = i.conecciones[k][0]
                    if nodo.nombre == nombre:
                        i.desconectar(nodo)
                        j -= 1
                        break

    def reemplazar_nodo(self, nombre, nuevo_nombre):
        nodo = self.buscar(nombre)
        nuevo_nodo = self.buscar(nuevo_nombre)

        if not nodo:
            raise Exception(f"El nodo {nombre} no existe")
        if nuevo_nodo:
            raise Exception(f'El nodo {nuevo_nombre} ya existe')

        nodo.nombre = nuevo_nombre

        for i in self.nodos:
            for j in i.conecciones:
                nodo = i.conecciones[j][0]
                if nodo.nombre == nombre:
                    nodo.nombre = nuevo_nombre

    def conectar_nodos(self, nombre_origen, nombre_destino, peso):
        nodo_origen = self.buscar(nombre_origen)
        nodo_destino = self.buscar(nombre_destino)

        if not nodo_origen:
            raise Exception("El nodo origen no existe")
        if not nodo_destino:
            raise Exception("El nodo destino no existe")

        for i in self.nodos:
            for j in i.conecciones:
                origen, destino = i, i.conecciones[j][0]
                if (nodo_origen, nodo_destino) == (origen, destino):
                    raise Exception("La coneccion ya existe")
                if (nodo_destino, nodo_origen) == (origen, destino):
                    raise Exception("La coneccion inversa ya existe")

        nodo_origen.conectar(nodo_destino, peso)

    def desconectar_nodos(self, nombre_origen, nombre_destino):
        nodo_origen = self.buscar(nombre_origen)
        nodo_destino = self.buscar(nombre_destino)

        if not nodo_origen:
            raise Exception("El nodo origen no existe")
        if not nodo_destino:
            raise Exception("El nodo destino no existe")

        for i in self.nodos:
            for j in i.conecciones:
                origen, destino = i, i.conecciones[j][0]
                if (nodo_origen, nodo_destino) == (origen, destino):
                    nodo_origen.desconectar(nodo_destino)
                    return

        raise Exception('La coneccion no existe')

    def reemplazar_coneccion(
        self, nombre_origen, nombre_destino, nuevo_origen, nuevo_destino, peso
    ):
        self.desconectar_nodos(nombre_origen, nombre_destino)
        self.conectar_nodos(nuevo_origen, nuevo_destino, peso)

    def buscar(self, nombre) -> Nodo:
        for i in self.nodos:
            if i.nombre == nombre:
                return i

    def graficar(self, dirigido=True):
        origenes = []
        destinos = []
        pesos = []

        for i in self.nodos:
            for j in i.conecciones:
                origen = i.nombre
                destino, peso = i.conecciones[j]

                origenes.append(origen)
                destinos.append(destino.nombre)
                pesos.append(peso)

        if origenes and destinos and pesos:
            graph = Graph(origenes, destinos, pesos, dirigido)
            print()
            graph.print_r()
            graph.draw()
        else:
            raise Exception('No hay conecciones en el grafo')
