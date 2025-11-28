import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
QLabel, QPushButton, QFrame, QMessageBox)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QSize

from base_ui import VentanaBase, COLOR_PRINCIPAL, FORMATO_FECHA_ESPANOL

class VentanaBoletos(VentanaBase):
    
    ESTILO_BTN_CANTIDAD = "QPushButton { border: 1px solid #000080; border-radius: 8px; font-size: 16pt; background-color: #f0f8ff; color: #000080; } QPushButton:hover { background-color: #e6f3ff; }"
    ESTILO_CONTADOR = "border: 1px solid #D3D3D3; border-radius: 8px; background-color: white; font-size: 14pt; color: #333333;"

    def __init__(self, ventana_principal, parent=None):
        super().__init__(ventana_principal, parent) 
        self.setWindowTitle("ECO ISLAS - Paso 1: Boletos")
        self.setMinimumSize(650, 500) 
        
        self.cant_adulto = 0 
        self.precio_adulto = 15000 

        self.armar_ventana()

    def armar_ventana(self):
        self.crear_pasos_navegacion(1) 
        
        diseno_contenido = QVBoxLayout()
        diseno_contenido.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        diseno_contenido.setContentsMargins(50, 20, 50, 20) 

        titulo = QLabel("Selecciona tus boletos", font=QFont("Calibri", 24, QFont.Weight.Bold))
        titulo.setStyleSheet("color: #000080; margin-bottom: 10px;")
        diseno_contenido.addWidget(titulo, alignment=Qt.AlignmentFlag.AlignCenter)
        diseno_contenido.addSpacing(20)
        
        self.crear_fila_boleto(diseno_contenido)

        self.eti_total = QLabel("Total: $0")
        self.eti_total.setFont(QFont("Calibri", 16, QFont.Weight.Bold))

        self.eti_total.setStyleSheet(f"color: {self.COLOR_PRINCIPAL}; padding: 10px; border: 1px dashed {self.COLOR_PRINCIPAL}; border-radius: 5px; margin-top: 15px;")
        diseno_contenido.addWidget(self.eti_total, alignment=Qt.AlignmentFlag.AlignCenter)

        diseno_contenido.addStretch()
        self.layout_maestro.addLayout(diseno_contenido)

        self.crear_pie_pagina(self.layout_maestro)

    def crear_fila_boleto(self, layout_padre):
        fila_boleto = QHBoxLayout()
        fila_boleto.setContentsMargins(50, 0, 50, 0) 
        fila_boleto.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        
        precio_formato = "{:,.0f}".format(self.precio_adulto).replace(",", ".")
        eti_precio = QLabel(f"<span style='font-size: 16pt; font-weight: bold;'>Boleto Adulto</span> "
            f"<span style='font-size: 14pt; color: gray;'>(${precio_formato})</span>")
        
        fila_boleto.addWidget(eti_precio)
        fila_boleto.addStretch() 

        diseno_cantidad = QHBoxLayout()

        self.btn_menos = QPushButton("-")
        self.btn_menos.setFixedSize(40, 40)
        self.btn_menos.setStyleSheet(self.ESTILO_BTN_CANTIDAD)
        self.btn_menos.clicked.connect(lambda: self.actualizar_conteo(-1))
        
        self.eti_contador = QLabel(str(self.cant_adulto))
        self.eti_contador.setFixedSize(40, 40)
        self.eti_contador.setStyleSheet(self.ESTILO_CONTADOR)
        self.eti_contador.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_mas = QPushButton("+")
        self.btn_mas.setFixedSize(40, 40)
        self.btn_mas.setStyleSheet(self.ESTILO_BTN_CANTIDAD)
        self.btn_mas.clicked.connect(lambda: self.actualizar_conteo(1))
        
        diseno_cantidad.addWidget(self.btn_menos)
        diseno_cantidad.addWidget(self.eti_contador)
        diseno_cantidad.addWidget(self.btn_mas)
        
        fila_boleto.addLayout(diseno_cantidad)
        
        layout_padre.addLayout(fila_boleto) 

    def crear_pie_pagina(self, layout_padre):
        diseno_pie = QHBoxLayout()
        diseno_pie.setContentsMargins(50, 20, 50, 20)
        diseno_pie.addStretch()

        btn_siguiente = QPushButton("Siguiente Paso →")
        btn_siguiente.setFont(QFont("Calibri", 14, QFont.Weight.Bold))
        btn_siguiente.setStyleSheet(f"background-color: {self.COLOR_PRINCIPAL}; color: white; border-radius: 8px; padding: 10px 20px;")
        
        btn_siguiente.clicked.connect(self.ir_a_paso2) 
        
        diseno_pie.addWidget(btn_siguiente)

        layout_padre.addLayout(diseno_pie)
        
    def actualizar_conteo(self, cambio):
        nuevo_conteo = self.cant_adulto + cambio
        if 0 <= nuevo_conteo <= 10:
            self.cant_adulto = nuevo_conteo
            self.eti_contador.setText(str(self.cant_adulto))
            self.calcular_total() 
        else:
            QMessageBox.warning(self, "Límite", "Solo puedes seleccionar entre 1 y 10 boletos.")

    def calcular_total(self):
        total = self.cant_adulto * self.precio_adulto
        total_formato = "{:,.0f}".format(total).replace(",", ".")
        self.eti_total.setText(f"Total: ${total_formato}")

    def ir_a_paso2(self):
        if self.cant_adulto == 0:
            QMessageBox.warning(self, "Requerido", "Debes seleccionar al menos 1 boleto para continuar.")
            return
        
        self.main_window.registrar_boletos(self.cant_adulto)