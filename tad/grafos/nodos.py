class NodoGrafo:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conecciones = {}

    def __str__(self):
        return f"{self.nombre}"

    def __repr__(self):
        return str(self)

    def __eq__(self, nodoGrafo):
        return (
            isinstance(nodoGrafo, NodoGrafo) and self.nombre == nodoGrafo.nombre
        )

    def conectar(self, nodo, peso):
        self.conecciones[nodo.nombre] = [nodo, peso]

    def desconectar(self, nodo):
        del self.conecciones[nodo.nombre]
