from tad.grafos.grafo import Grafo

P = "P"
T = "T"


def solucionar(origen, unGrafo):
    if not unGrafo.nodos:
        raise Exception('No hay nodos en el grafo')

    tabla = [[origen, [0, None], P]]
    visitados = [origen]

    funcion(origen, tabla, visitados, 0)

    mostrar_tabla(tabla)

    return tabla


def funcion(nodo, tabla, visitados, ui):
    for i in nodo.conecciones:

        j, dij = nodo.conecciones[i]

        if j not in visitados:
            ui += int(dij)
            etiqueta = [ui, nodo]

            repetidos = []
            tabla.append([j, etiqueta, T])
            for k in range(len(tabla)):
                if tabla[k][0] == j:
                    repetidos.append(tabla[k])

            if len(repetidos) > 1:
                for k in range(len(repetidos)):
                    for l in range(k+1,len(repetidos)):
                        _i = repetidos[k][1][0]
                        _j = repetidos[l][1][0]
                        if _i <= _j:
                            tabla.remove(repetidos[l])
                            repetidos.remove(repetidos[l])
                            l -= 1
                        else:
                            tabla.remove(repetidos[l])
                            repetidos.remove(repetidos[l])
                            k -= 1

                    # if k + 1 < len(repetidos):
                    #     k -= 1

            print(i)
            visitados.append(j)
            if j.conecciones:
                funcion(j, tabla, visitados, ui)


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

