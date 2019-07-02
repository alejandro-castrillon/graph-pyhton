import os
import sys

from PyQt5 import QtCore, QtWidgets, uic

from dialogs import DialogArco, DialogMensaje, DialogNodo, DialogDijkstra
from tad.grafos import Grafo
from utilities import clear, read_binary_file, write_binary_file


class MainWindowGrafo(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.grafo = Grafo()
        self.guardado = None

        self.init_components()
        self.init_events()

    def init_components(self):
        uic.loadUi('gui/mainWindow_graph.ui', self)

        self.listWidget_nodos: QtWidgets.QListWidget
        self.tableWidget_arcos: QtWidgets.QTableView
        self.tableWidget_dijkstra: QtWidgets.QTabWidget

        self.center_location()
        self.tableWidget_arcos.verticalHeader().hide()

    def center_location(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        widget = self.geometry()
        x = screen.width() - widget.width()
        y = screen.height() - widget.height()
        self.move(x / 2, y / 2)

    def init_events(self):
        # ---------------------------------------------------------------------
        self.action_nuevo_grafo.triggered.connect(self.nuevo_grafo)
        self.action_guardar_grafo.triggered.connect(self.guardar_grafo)
        self.action_guardar_grafo_como.triggered.connect(
            self.guardar_grafo_como
        )
        self.action_abrir_grafo.triggered.connect(self.abrir_grafo)
        self.action_salir.triggered.connect(self.salir)

        # ---------------------------------------------------------------------
        self.action_agregar_nodo.triggered.connect(self.agregar_nodo)
        self.action_editar_nodo.triggered.connect(self.editar_nodo)
        self.action_eliminar_nodo.triggered.connect(self.eliminar_nodo)

        # ---------------------------------------------------------------------
        self.action_agregar_arco.triggered.connect(self.agregar_arco)
        self.action_editar_arco.triggered.connect(self.editar_arco)
        self.action_eliminar_arco.triggered.connect(self.eliminar_arco)

        # ---------------------------------------------------------------------
        self.action_graficar_grafo.triggered.connect(self.graficar_grafo)

        # ---------------------------------------------------------------------
        self.pushButton_agregar_nodo.clicked.connect(self.agregar_nodo)
        self.pushButton_editar_nodo.clicked.connect(self.editar_nodo)
        self.pushButton_eliminar_nodo.clicked.connect(self.eliminar_nodo)

        # ---------------------------------------------------------------------
        self.pushButton_agregar_arco.clicked.connect(self.agregar_arco)
        self.pushButton_editar_arco.clicked.connect(self.editar_arco)
        self.pushButton_eliminar_arco.clicked.connect(self.eliminar_arco)

        # ---------------------------------------------------------------------
        self.pushButton_graficar_grafo.clicked.connect(self.graficar_grafo)

        # ---------------------------------------------------------------------
        self.pushButton_resolver.clicked.connect(self.resolver)

    def nuevo_grafo(self):
        if self.guardado == None:
            pass
        elif self.guardado == False:
            pass
        else:
            self.listWidget_nodos.clear()
            self.tableWidget_arcos.setRowCount(0)
            self.guardado = False

    # TODO: Guardar los cambios hechos en el grafo
    def guardar_grafo(self):
        if self.guardado == None:
            self.guardar_grafo_como()
        elif self.guardado == False:
            self.guardado = True

    def guardar_grafo_como(self):
        try:
            path = QtWidgets.QFileDialog.getSaveFileName()[0]
            if path:
                write_binary_file(path, self.grafo)
        except:
            DialogMensaje(
                'Error al guardar', 'No fue posible guardar el archivo'
            )

    def abrir_grafo(self):
        if self.guardado != False:
            ruta = QtWidgets.QFileDialog.getOpenFileName()[0]

            if ruta:
                self.grafo = read_binary_file(ruta)
                self.nuevo_grafo()
                self.cargar_grafo()
            else:
                DialogMensaje(
                    'Error al abrir', 'No fue posible abrir el archivo'
                )

    def cargar_grafo(self):
        for i in self.grafo.nodos:
            nodo = QtWidgets.QListWidgetItem(i.nombre)
            self.listWidget_nodos.addItem(nodo)

            for j in i.conecciones:
                destino, peso = i.conecciones[j]

                self.agregar_fila([i.nombre, destino.nombre, peso])

        if self.guardado:
            self.guardado = False

    def closeEvent(self, event):
        self.salir()

    # TODO: Verificacion de guardado del archivo
    def salir(self):
        if self.guardado:
            sys.exit()
        else:
            dialog_mensaje = DialogMensaje(
                'Salir del programa', 'Guardar antes de Salir?'
            )
            dialog_mensaje.buttonBox.accepted.connect(self.guardar_grafo)
            dialog_mensaje.buttonBox.accepted.connect(sys.exit)
            dialog_mensaje.buttonBox.rejected.connect(sys.exit)
            dialog_mensaje.exec()

    def agregar_nodo(self):
        dialog_nodo = DialogNodo('Nuevo Nodo', 'Nombre del nuevo nodo:')
        dialog_nodo.exec()

        nodo = dialog_nodo.nodo
        if nodo:
            try:
                self.grafo.agregar_nodo(nodo)
                item = QtWidgets.QListWidgetItem(nodo)
                self.listWidget_nodos.addItem(item)
                if self.guardado:
                    self.guardado = False
            except Exception as e:
                DialogMensaje('Error al agregar un nodo', str(e)).exec()

    def editar_nodo(self):
        item = self.listWidget_nodos.currentItem()
        if item:
            text = item.text()
            dialog_nodo = DialogNodo(
                'Editar Nodo', 'Nuevo nombre del nodo:', text
            )
            dialog_nodo.exec()

            nodo = dialog_nodo.nodo
            if nodo:
                self.reemplazar_nodo_lista(text, nodo)

                if self.guardado:
                    self.guardado = False

    def reemplazar_nodo_lista(self, anterior, nuevo):
        try:
            self.grafo.reemplazar_nodo(anterior, nuevo)
            self.listWidget_nodos.currentItem().setText(nuevo)

            self.tableWidget_arcos.setRowCount(0)
            for i in self.grafo.nodos:
                for j in i.conecciones:
                    k, l = i.conecciones[j]
                    self.agregar_fila([i.nombre, k.nombre, l])
        except Exception as e:
            DialogMensaje('Error al editar un nodo', str(e)).exec()

    def eliminar_nodo(self):
        items = self.listWidget_nodos.selectedItems()
        if items:
            item = items[0]
            if item:
                dialog_mensaje = DialogMensaje(
                    'Eliminar Nodo',
                    f"Eliminar el nodo '{item.data(0)}' y sus posibles conecciones?",
                )
                dialog_mensaje.buttonBox.accepted.connect(
                    lambda: self.eliminar_nodo_lista(item.data(0))
                )
                dialog_mensaje.exec()

    def eliminar_nodo_lista(self, nodo):
        self.listWidget_nodos.takeItem(self.listWidget_nodos.currentRow())
        self.grafo.eliminar_nodo(nodo)

        self.tableWidget_arcos.setRowCount(0)
        for i in self.grafo.nodos:
            for j in i.conecciones:
                k, l = i.conecciones[j]
                self.agregar_fila([i.nombre, k.nombre, l])

        if self.guardado:
            self.guardado = False

    def agregar_arco(self):
        dialog_arco = DialogArco(
            'Nuevo Arco',
            'Realize la coneccion entre 2 nodos:',
            self.grafo.nodos,
        )
        dialog_arco.exec()

        arco = dialog_arco.arco
        if arco:
            try:
                self.grafo.conectar_nodos(*arco)
                self.agregar_fila(arco)
                if self.guardado:
                    self.guardado = False
            except Exception as e:
                DialogMensaje('Error al conectar los nodos', str(e)).exec()

    def agregar_fila(self, fila):
        row_count = self.tableWidget_arcos.rowCount()

        origen = QtWidgets.QTableWidgetItem(fila[0])
        destino = QtWidgets.QTableWidgetItem(fila[1])
        peso = QtWidgets.QTableWidgetItem(fila[2])

        self.tableWidget_arcos.setRowCount(row_count + 1)

        self.tableWidget_arcos.setItem(row_count, 0, origen)
        self.tableWidget_arcos.setItem(row_count, 1, destino)
        self.tableWidget_arcos.setItem(row_count, 2, peso)

    def editar_arco(self):
        try:
            row = self.tableWidget_arcos.currentRow()
            anterior = [
                self.tableWidget_arcos.item(row, 0).text(),
                self.tableWidget_arcos.item(row, 1).text(),
                self.tableWidget_arcos.item(row, 2).text(),
            ]

            dialog_nodo = DialogArco(
                'Editar Arco', 'Nuevo arco:', self.grafo.nodos, anterior
            )
            dialog_nodo.exec()

            nuevo = dialog_nodo.arco
            try:
                if nuevo and anterior != nuevo:
                    self.reemplazar_arco(row, anterior, nuevo)
            except Exception as e:
                DialogMensaje('Error al editar un nodo', str(e)).exec()

            if self.guardado:
                self.guardado = False
        except Exception as e:
            print(str(e))

    def reemplazar_arco(self, row, anterior, nuevo):
        self.grafo.desconectar_nodos(anterior[0], anterior[1])
        self.grafo.conectar_nodos(*nuevo)
        self.tableWidget_arcos.setItem(
            row, 0, QtWidgets.QTableWidgetItem(nuevo[0])
        )
        self.tableWidget_arcos.setItem(
            row, 1, QtWidgets.QTableWidgetItem(nuevo[1])
        )
        self.tableWidget_arcos.setItem(
            row, 2, QtWidgets.QTableWidgetItem(nuevo[2])
        )

    def eliminar_arco(self):
        row = self.tableWidget_arcos.currentRow()
        if row >= 0:
            origen = self.tableWidget_arcos.item(row, 0).text()
            destino = self.tableWidget_arcos.item(row, 1).text()
            peso = self.tableWidget_arcos.item(row, 2).text()

            dialog_mensaje = DialogMensaje(
                'Eliminar Nodo',
                f"Eliminar el arco ({origen}) --[{peso}]-> ({destino})?",
            )
            dialog_mensaje.buttonBox.accepted.connect(
                lambda: self.eliminar_arco_tabla(row, origen, destino)
            )
            dialog_mensaje.exec()

    def eliminar_arco_tabla(self, row, origen, destino):
        self.tableWidget_arcos.removeRow(row)
        self.grafo.desconectar_nodos(origen, destino)
        if self.guardado:
            self.guardado = False

    def graficar_grafo(self):
        try:
            self.grafo.graficar()
        except Exception as e:
            DialogMensaje('Error al graficar un grafo', str(e)).exec()

    def resolver(self):
        DialogDijkstra(self.grafo).exec()


if __name__ == '__main__':
    clear()
    app = QtWidgets.QApplication(sys.argv)
    mainWindow_grafo = MainWindowGrafo()
    mainWindow_grafo.show()
    app.exec()
