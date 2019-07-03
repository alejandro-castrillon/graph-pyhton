from PyQt5 import QtWidgets, QtCore, uic

from tad.grafos import Grafo, solucionar


class DialogMensaje(QtWidgets.QDialog):
    def __init__(self, titulo: str, mensaje: str):
        super().__init__()
        self.titulo = titulo
        self.mensaje = mensaje

        self.__init_components()

    def __init_components(self):
        uic.loadUi('gui/dialog_message.ui', self)

        self.setWindowTitle(self.titulo)
        self.label.setText(self.mensaje)


class DialogNodo(QtWidgets.QDialog):
    def __init__(self, titulo, mensaje, nodo=None):
        super().__init__()
        self.titulo = titulo
        self.mensaje = mensaje
        self.nodo = nodo

        self.__init_components()
        self.__init_events()

    def __init_components(self):
        uic.loadUi('gui/dialog_node.ui', self)

        self.setWindowTitle(self.titulo)
        self.label.setText(self.mensaje)

        if self.nodo:
            self.lineEdit.setText(self.nodo)

    def __init_events(self):
        self.buttonBox.accepted.connect(self.finish)
        self.buttonBox.rejected.connect(self.reset)

    def finish(self):
        text = self.lineEdit.text()
        if text:
            self.nodo = text
        else:
            DialogMensaje(
                'Error al agregar el nodo', 'Nombre del nuevo nodo invalido'
            ).exec()
            self.reset()

    def reset(self):
        self.nodo = None


class DialogArco(QtWidgets.QDialog):
    def __init__(self, titulo, mensaje, nodos, arco=None):
        super().__init__()
        self.titulo = titulo
        self.mensaje = mensaje
        self.nodos = nodos
        self.arco = arco

        self.__init_components()
        self.__init_events()

    def __init_components(self):
        uic.loadUi('gui/dialog_edge.ui', self)

        self.setWindowTitle(self.titulo)
        self.label.setText(self.mensaje)

        if self.nodos:
            nodos = [i.nombre for i in self.nodos]
            self.comboBox_nodos_origen.addItems(nodos)
            self.comboBox_nodos_destino.addItems(nodos)

            if self.arco:
                self.cargar_arco()

    def cargar_arco(self):
        origen, destino, peso = self.arco

        index_origen = self.comboBox_nodos_origen.findText(
            origen, QtCore.Qt.MatchFixedString
        )
        index_destino = self.comboBox_nodos_origen.findText(
            destino, QtCore.Qt.MatchFixedString
        )

        try:
            if index_origen < 0:
                raise Exception('El nodo origen no existe')
            elif index_destino < 0:
                raise Exception('El nodo destino no existe')
            elif not peso or not peso.isdigit():
                raise Exception(
                    'El peso de la coneccion debe ser un valor numerico'
                )
            self.comboBox_nodos_origen.setCurrentIndex(index_origen)
            self.comboBox_nodos_destino.setCurrentIndex(index_destino)
            self.lineEdit.setText(peso)
        except Exception as e:
            DialogMensaje('Error al cargar el arco', str(e)).exec()
            self.close()

    def __init_events(self):
        self.buttonBox.accepted.connect(lambda: self.finish())
        self.buttonBox.rejected.connect(self.reset)

    def finish(self):
        origen = str(self.comboBox_nodos_origen.currentText())
        destino = str(self.comboBox_nodos_destino.currentText())
        peso = self.lineEdit.text()

        try:
            if not origen or not destino:
                raise Exception('No hay nodos para conectar')
            elif origen == destino:
                raise Exception('Un nodo no debe conectarse a si mismo')
            elif not peso or not peso.isdigit():
                raise Exception(
                    'El peso de la coneccion debe ser un valor numerico'
                )
            self.arco = [origen, destino, peso]
        except Exception as e:
            DialogMensaje('Error al conectar los nodos', str(e)).exec()
            self.reset()

    def reset(self):
        self.arco = None


class DialogDijkstra(QtWidgets.QDialog):
    def __init__(self, grafo):
        super().__init__()
        self.grafo: Grafo = grafo

        self.init_components()
        self.init_events()

    def init_components(self):
        uic.loadUi('gui/dialog_dijkstra.ui', self)

        self.tableWidget_dijkstra.verticalHeader().hide()
        
        for i in self.grafo.nodos:
            if i.conecciones:
                self.comboBox_nodos.addItem(i.nombre)

    def init_events(self):
        self.pushButton_resolver.clicked.connect(self.solucionar)

        self.pushButton_graficar_solucion.clicked.connect(
            self.graficar_solucion
        )

        self.pushButton_limpiar.clicked.connect(self.limpiar)

    def solucionar(self):
        self.limpiar()

        origen = str(self.comboBox_nodos.currentText())
        origen = self.grafo.buscar(origen)
        tabla = solucionar(origen, self.grafo)

        for fila in tabla:
            row_count = self.tableWidget_dijkstra.rowCount()

            nodo = QtWidgets.QTableWidgetItem(fila[0].nombre)
            etiqueta = QtWidgets.QTableWidgetItem(str(fila[1]))
            estado = QtWidgets.QTableWidgetItem(fila[2])

            self.tableWidget_dijkstra.setRowCount(row_count + 1)

            self.tableWidget_dijkstra.setItem(row_count, 0, nodo)
            self.tableWidget_dijkstra.setItem(row_count, 1, etiqueta)
            self.tableWidget_dijkstra.setItem(row_count, 2, estado)


    def graficar_solucion(self):
        self.grafo.graficar()

    def limpiar(self):
        self.tableWidget_dijkstra.setRowCount(0)

