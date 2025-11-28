import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
 QLabel, QPushButton, QFrame, QMessageBox)
from PyQt6.QtGui import QFont

from PyQt6.QtCore import Qt, QDate 
import os 

from base_ui import VentanaBase, FORMATO_FECHA_ESPANOL, LOCALE_ESPANOL

class VentanaResumen(VentanaBase):
    
    PRECIO_UNITARIO = 15000 
    NOMBRE_ARCHIVO_VENTAS = "ventas.txt" 

    def __init__(self, ventana_principal, parent=None):
        super().__init__(ventana_principal, parent)
        self.setWindowTitle("ECO ISLAS - Paso 4: Resumen y Pago")
        self.setMinimumSize(800, 600)
        
        self.datos = {
            'cant_boletos': 0,
            'fecha': "",
            'embarcacion': "",
            'horario': "",
            'asientos': []
        }
        self.costo_total = 0
        
        self.armar_ventana()
        
    def actualizar_datos(self, datos_viaje):
        self.datos = datos_viaje
        self.costo_total = self.datos['cant_boletos'] * self.PRECIO_UNITARIO
        
        self._actualizar_panel_resumen()

    def guardar_reserva_en_archivo(self):
        try:
            linea_venta = (
                f"--- NUEVA COMPRA ---\n"
                f"FECHA COMPRA: {LOCALE_ESPANOL.toString(QDate.currentDate(), FORMATO_FECHA_ESPANOL)}\n" 
                f"BOLETOS: {self.datos['cant_boletos']} x ${self.PRECIO_UNITARIO:,.0f}\n"
                f"EMBARCACION: {self.datos['embarcacion']} ({self.datos['horario']} del {self.datos['fecha']})\n"
                f"ASIENTOS: {', '.join(self.datos['asientos'])}\n"
                f"TOTAL PAGADO: ${self.costo_total:,.0f}\n"
                f"----------------------\n\n"
            )

            with open(self.NOMBRE_ARCHIVO_VENTAS, 'a', encoding='utf-8') as f:
                f.write(linea_venta)
            
            print(f"Reserva guardada exitosamente en {self.NOMBRE_ARCHIVO_VENTAS}")
            return True
        except Exception as e:
            print(f"ERROR al guardar la reserva: {e}")
            QMessageBox.critical(self, "Error de Archivo", f"No se pudo guardar la reserva. Detalles: {e}")
            return False

    def finalizar_compra_y_guardar(self):
        if self.guardar_reserva_en_archivo():
            QMessageBox.information(self, "¡Compra Exitosa!", 
                                    f"Total pagado: ${self.costo_total:,.0f}\n"
                                    f"(Datos guardados en {self.NOMBRE_ARCHIVO_VENTAS})")
            QApplication.quit()
        else:
            pass



    def armar_ventana(self):
        self.crear_pasos_navegacion(4) 
        
        titulo = QLabel("Paso 4: Resumen de tu Viaje", 
                        font=QFont("Calibri", 22, QFont.Weight.Bold), 
                        alignment=Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("color: #000080; margin-top: 15px; margin-bottom: 20px;")
        self.layout_maestro.addWidget(titulo)
        
        self.panel_resumen = QWidget()
        self.layout_maestro.addWidget(self.panel_resumen, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.layout_maestro.addStretch()
        self.layout_maestro.addLayout(self._crear_pie_pagina())
        
        self._actualizar_panel_resumen() 


    def _crear_item_simple(self, titulo, valor):
        return QLabel(f"<b>{titulo}:</b> {valor}", font=QFont("Calibri", 16))

    def _actualizar_panel_resumen(self):
        if self.panel_resumen.layout():
            layout = self.panel_resumen.layout()
            while layout.count():
                item = layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
        else:
            layout = QVBoxLayout(self.panel_resumen)
            layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            layout.setContentsMargins(50, 30, 50, 30)

        asientos_str = ", ".join(self.datos['asientos']) if self.datos['asientos'] else "Aún no seleccionados"
        
        layout.addWidget(self._crear_item_simple("Boletos", f"{self.datos['cant_boletos']} boleto(s) de adulto"))
        layout.addWidget(self._crear_item_simple("Fecha", self.datos['fecha']))
        layout.addWidget(self._crear_item_simple("Embarcación", self.datos['embarcacion']))
        layout.addWidget(self._crear_item_simple("Horario", self.datos['horario']))
        layout.addWidget(self._crear_item_simple("Asientos Seleccionados", asientos_str))
        
        layout.addSpacing(30)
        
        tarjeta_total = QWidget(styleSheet=f"background-color: #E8F5E9; border-radius: 10px; border: 2px solid {self.COLOR_PRINCIPAL};")
        diseno_total = QHBoxLayout(tarjeta_total)
        diseno_total.setContentsMargins(20, 10, 20, 10)
        
        label_total_titulo = QLabel("Total a Pagar:", font=QFont("Calibri", 18, QFont.Weight.Bold))
        label_total_titulo.setStyleSheet(f"color: {self.COLOR_PRINCIPAL};")
        
        total_formato = "{:,.0f}".format(self.costo_total).replace(",", ".")
        label_total_valor = QLabel(f"${total_formato}", font=QFont("Calibri", 24, QFont.Weight.ExtraBold))
        label_total_valor.setStyleSheet("color: #000080;")
        
        diseno_total.addWidget(label_total_titulo)
        diseno_total.addStretch()
        diseno_total.addWidget(label_total_valor)
        
        layout.addWidget(tarjeta_total, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addStretch()

    def _crear_pie_pagina(self):
        diseno_pie = QHBoxLayout()
        diseno_pie.setContentsMargins(50, 20, 50, 20)
        
        btn_regresar = QPushButton("← Regresar y Editar")
        estilo_regresar = "font: 14pt Calibri; font-weight: bold; border-radius: 8px; padding: 10px 20px; background-color: gray; color: white;"
        btn_regresar.setStyleSheet(estilo_regresar)
        btn_regresar.clicked.connect(lambda: self.main_window.goto_paso(2)) 
        diseno_pie.addWidget(btn_regresar)
        
        diseno_pie.addStretch()

        total_formato = "{:,.0f}".format(self.costo_total).replace(",", ".")
        btn_pagar = QPushButton(f"Pagar ${self.costo_total:,.0f} Ahora")
        estilo_pagar = f"font: 16pt Calibri; font-weight: bold; border-radius: 10px; padding: 12px 30px; background-color: #ff9900; color: white;"
        btn_pagar.setStyleSheet(estilo_pagar)

        btn_pagar.clicked.connect(self.finalizar_compra_y_guardar)
        diseno_pie.addWidget(btn_pagar)

        return diseno_pie