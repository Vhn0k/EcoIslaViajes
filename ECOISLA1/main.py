import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
QLabel, QPushButton, QFrame, QMainWindow, QStackedWidget,QMessageBox)
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt, QSize, QDate

import base_ui 

from boletos import VentanaBoletos
from embarque import VentanaEmbarques
from asientos import VentanaAsientos
from resumen import VentanaResumen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECO ISLAS - Sistema de Reserva Centralizado")
        self.setFixedSize(1000, 750)
        
        self.COLOR_PRINCIPAL = base_ui.COLOR_PRINCIPAL
        self.COLOR_FONDO_NAV = base_ui.COLOR_FONDO_NAV
        self.LOCALE_ESPANOL = base_ui.LOCALE_ESPANOL
        self.FORMATO_FECHA_ESPANOL = base_ui.FORMATO_FECHA_ESPANOL

        fecha_ini = self.LOCALE_ESPANOL.toString(QDate.currentDate(), self.FORMATO_FECHA_ESPANOL)
        self.datos_viaje = {
            'cant_boletos': 0,
            'fecha': fecha_ini,
            'embarcacion': None,
            'horario': None,
            'asientos': []
        }
        
        self.contenedor_principal = QStackedWidget()
        self.setCentralWidget(self.contenedor_principal)
        
        self.ventana_acceso = self._crear_ventana_acceso()
        self.contenedor_principal.addWidget(self.ventana_acceso)
        
        self.stack_pasos = self._crear_stack_pasos()
        self.contenedor_principal.addWidget(self.stack_pasos)

        self.contenedor_principal.setCurrentWidget(self.ventana_acceso)

    def _crear_ventana_acceso(self):
        widget = QWidget()
        Diseño_Principal = QVBoxLayout(widget)
        Diseño_Principal.setContentsMargins(0, 0, 0, 0)

        verde = self.COLOR_PRINCIPAL
        
        EstiloBoton1 = f"QPushButton {{ color: {verde}; background-color: transparent; border: 2px solid {verde}; border-radius: 15px; padding: 5px 15px; }} QPushButton:hover {{ background-color: rgba(46, 139, 87, 0.1); }}"
        EstiloBusqueda = f"QPushButton {{ background-color: rgba(173, 216, 230, 0.7); border-radius: 25px; padding: 10px 20px; border: none; color: #36454F; text-align: left; }}"
        
        Encabezado = QHBoxLayout()
        Encabezado.setContentsMargins(20, 15, 20, 15)
        
        logo = QLabel(f'<span style="color: {verde}; font-weight: bold;">ECO</span><span style="font-size: 24pt; color: {verde};">🌴</span><span style="color: {verde}; font-weight: bold;">ISLAS</span>', font=QFont("Calibri", 24))
        Encabezado.addWidget(logo)
        Encabezado.addStretch()

        Encabezado.addWidget(QPushButton("Iniciar Sesión", styleSheet=EstiloBoton1))
        Encabezado.addWidget(QPushButton("Registrar", styleSheet=EstiloBoton1))
        Encabezado.addWidget(QPushButton("Menú ☰", styleSheet=EstiloBoton1))
        
        Diseño_Principal.addLayout(Encabezado)
        Diseño_Principal.addWidget(QFrame(frameShape=QFrame.Shape.HLine, styleSheet="background-color: #A9A9A9; height: 1px;"))
        
        Cuerpo_Ventana = QVBoxLayout()
        Cuerpo_Ventana.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        
        Titulo1 = QLabel("CONOCE Y RESERVA TU\n VIAJE CON ECOISLAS 🌴")
        Titulo1.setFont(QFont("Calibri", 30, QFont.Weight.Bold))
        Titulo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        Titulo1.setStyleSheet(f"color: {self.COLOR_FONDO_NAV}; margin-bottom: 20px;")
        
        Cuerpo_Ventana.addWidget(Titulo1)
        
        botondebusqueda = QPushButton("🔍 ¿Cual es tu próximo destino?")
        botondebusqueda.setFont(QFont("Segoe Print", 16, QFont.Weight.Light)) 
        botondebusqueda.setStyleSheet(EstiloBusqueda)
        botondebusqueda.setFixedSize(QSize(500, 60)) 
        
        botondebusqueda.clicked.connect(self.iniciar_reserva)
        
        Cuerpo_Ventana.addWidget(botondebusqueda, alignment=Qt.AlignmentFlag.AlignCenter)
        Cuerpo_Ventana.addStretch()

        Diseño_Principal.addLayout(Cuerpo_Ventana)
        return widget

    def _crear_stack_pasos(self):
        stacked = QStackedWidget()

        self.v_paso1 = VentanaBoletos(self) 
        self.v_paso2 = VentanaEmbarques(self) 
        self.v_paso3 = VentanaAsientos(self)
        self.v_paso4 = VentanaResumen(self)
        
        stacked.addWidget(self.v_paso1)
        stacked.addWidget(self.v_paso2)
        stacked.addWidget(self.v_paso3)
        stacked.addWidget(self.v_paso4)
        
        return stacked


    def iniciar_reserva(self):
        self.contenedor_principal.setCurrentWidget(self.stack_pasos)
        self.stack_pasos.setCurrentIndex(0) 
        
    def goto_paso(self, index):
        if 0 <= index < self.stack_pasos.count():
            self.stack_pasos.setCurrentIndex(index)
        
    def registrar_boletos(self, cant_boletos):
        self.datos_viaje['cant_boletos'] = cant_boletos
        self.v_paso2.actualizar_datos(cant_boletos=cant_boletos)
        self.goto_paso(1) 

    def registrar_viaje(self, embarcacion, horario):
        self.datos_viaje['embarcacion'] = embarcacion
        self.datos_viaje['horario'] = horario
        
        self.v_paso3.actualizar_datos(
            cant_boletos=self.datos_viaje['cant_boletos'],
            fecha=self.datos_viaje['fecha'],
            embarcacion=embarcacion,
            horario=horario
        )
        self.goto_paso(2) 

    def registrar_asientos(self, asientos_seleccionados):
        self.datos_viaje['asientos'] = asientos_seleccionados
        self.v_paso4.actualizar_datos(self.datos_viaje)
        self.goto_paso(3) 
        
    def finalizar_compra(self):
        QMessageBox.information(self, "¡Compra Exitosa!", 
                                f"Total pagado: ${self.datos_viaje['cant_boletos'] * 15000:,.0f}\n"
                                f"Recibirás los detalles de tu reserva ({self.datos_viaje['embarcacion']} - {self.datos_viaje['horario']}) en tu correo.")
        QApplication.quit()

    def volver_a_acceso(self):
        self.contenedor_principal.setCurrentWidget(self.ventana_acceso)
        
def iniciar_app():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    iniciar_app()