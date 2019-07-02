from tad.grafos.grafo import Grafo


def solucionar(grafo):
    P = "P"
    T = "T"
    tabla = []

    nodos = grafo.nodos
    if not nodos:
        raise Exception('No hay nodos en el grafo')

    origen = nodos[0]
    etiqueta = [0, None]

    tabla.append([origen, etiqueta, P])

    for i in nodos:
        for j in i.conecciones:
            ui = 0

            k, dij = i.conecciones[j]
            etiqueta = [ui + int(dij), i]

            tabla.append([k, etiqueta, T])

    mostrar_tabla(tabla)
    ordenar_tabla(tabla)
    mostrar_tabla(tabla)


def mostrar_tabla(tabla):
    print()
    for i in tabla:
        for j in i:
            print(j, end=" ")
        print()


def ordenar_tabla(tabla):
    _len = len(tabla)
    for i in range(_len):
        for j in range(i, _len):
            if tabla[i][0].nombre > tabla[j][0].nombre:
                tabla[i], tabla[j] = tabla[j], tabla[i]
                i -= 1

