import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
QLabel, QPushButton, QFrame)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QLocale, QDate 


#Constantes globales 
COLOR_PRINCIPAL = "#2e8b57" 
COLOR_FONDO_NAV = "#000080" 
LOCALE_ESPANOL = QLocale(QLocale.Language.Spanish, QLocale.Country.Chile)
FORMATO_FECHA_ESPANOL = "dd 'de' MMMM 'de' yyyy"

QLocale.setDefault(LOCALE_ESPANOL)

#Clase base o padre de todo el sistema de reservas, de aqui se define el layout principal, encabezado y la barra de navegacion de pasos
class VentanaBase(QWidget):
  
    COLOR_PRINCIPAL = COLOR_PRINCIPAL
    COLOR_FONDO_NAV = COLOR_FONDO_NAV
    
    def __init__(self, main_window, parent=None):
        super().__init__(parent)
        self.main_window = main_window 
        self.layout_maestro = QVBoxLayout(self)
        self.layout_maestro.setContentsMargins(0, 0, 0, 0)
        
        #Añade un encabezado 
        self.layout_maestro.addWidget(self._crear_header())

        #Layout para la navegación de pasos 
        self.layout_pasos = QHBoxLayout()
        self.layout_maestro.addLayout(self.layout_pasos)
        
        #Linea divisora después de la navegación de pasos
        self.layout_maestro.addWidget(QFrame(frameShape=QFrame.Shape.HLine, 
        styleSheet="background-color: #D3D3D3; height: 1px;"))
        
    def _crear_header(self):

        frame = QFrame(styleSheet=f"background-color: {self.COLOR_FONDO_NAV}; padding: 10px;")
        diseno_header = QHBoxLayout(frame)
        diseno_header.setContentsMargins(20, 10, 20, 10)
        
        logo = QLabel(f'<span style="color: {self.COLOR_PRINCIPAL}; font-weight: bold;">ECO</span><span style="font-size: 18pt; color: white;">🌴</span><span style="color: {self.COLOR_PRINCIPAL};">ISLAS</span>', 
        font=QFont("Calibri", 20))
        diseno_header.addWidget(logo)
        diseno_header.addStretch()
        
        diseno_header.addWidget(QPushButton("Menú ☰", 
        styleSheet="color: white; background-color: transparent; border: 1px solid white; border-radius: 10px; padding: 5px 10px;"))
        return frame 
    
    #Metodo responsable de generar esa negrita en cada ventana de la barra. 
    def crear_pasos_navegacion(self, paso_actual):
       
        while self.layout_pasos.count():
            item = self.layout_pasos.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        self.layout_pasos.setContentsMargins(50, 20, 50, 20)
        pasos_texto = {1: "Paso 1\nBoletos", 2: "Paso 2\nEmbarques", 3: "Paso 3\nAsientos", 4: "Paso 4\nResumen"}
        
        for num, texto in pasos_texto.items():
            etiqueta = QLabel(texto, alignment=Qt.AlignmentFlag.AlignCenter, font=QFont("Calibri", 12))
            
            if num == paso_actual:
                estilo = "color: #000080; font-weight: bold; border-bottom: 3px solid #000080;"
            else:
                estilo = "color: gray;"
            
            etiqueta.setStyleSheet(estilo)
            self.layout_pasos.addWidget(etiqueta)
            
            if num < 4: 
                self.layout_pasos.addStretch()