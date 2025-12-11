import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
 QFrame, QGridLayout, QMessageBox,
QSpacerItem, QSizePolicy)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QLocale, QDate 

from base_ui import VentanaBase, LOCALE_ESPANOL, FORMATO_FECHA_ESPANOL

#Paso 3 
class VentanaAsientos(VentanaBase):
    
    COLUMNAS = ['A', 'B', 'C', 'D', 'E']

    def __init__(self, ventana_principal, parent=None):
        super().__init__(ventana_principal, parent)
        self.setWindowTitle("ECO ISLAS - Paso 3: Selección de Asientos")
        self.setMinimumSize(800, 600)
        
        self.cant_boletos = 0
        self.fecha_viaje = ""
        self.embarcacion = ""
        self.horario = ""
        
        self.asientos_seleccionados = {}  # Diccionario para rastrear los asientos elegidos 
        self.max_asientos = 0
        self.botones_asientos = {} # Diccionario para acceder a los QPushButtons de la cuadrícula
        
        self.armar_ventana()
        
    #Metodo llamado de main.py nuevamente, recibe y actualiza los datos del viaje.
    def actualizar_datos(self, cant_boletos, fecha, embarcacion, horario):
        self.cant_boletos = cant_boletos
        self.fecha_viaje = fecha
        self.embarcacion = embarcacion
        self.horario = horario
        
        self.max_asientos = cant_boletos
        self.asientos_seleccionados = {}
        
        self._actualizar_contador()
        self._actualizar_resumen_viaje()
        self._reiniciar_estilos_asientos()

    def _actualizar_resumen_viaje(self):
        resumen_viaje = f"Pasajeros a bordo: <b>{self.cant_boletos}</b>. Viaje: <b>{self.embarcacion}</b> el <b>{self.fecha_viaje}</b> a las <b>{self.horario}</b>."
        self.resumen_label.setText(resumen_viaje)

    def _reiniciar_estilos_asientos(self):
        for btn in self.botones_asientos.values():
            btn.setStyleSheet(self._get_asiento_style('DISPONIBLE'))

    def _get_asiento_style(self, estado):
        base = "font: 12pt Calibri; border-radius: 5px; padding: 10px; min-width: 45px; min-height: 40px; font-weight: bold; margin: 3px;"
        if estado == 'DISPONIBLE':
            return base + "background-color: #E8F5E9; color: #38761D; border: 1px solid #7CB342;"
        elif estado == 'SELECCIONADO':
            return base + "background-color: #000080; color: white; border: 2px solid #2e8b57;"
        
    #Metodo que maneja si un asiento esta seleccionado o no
    def _toggle_asiento(self, asiento_id):
        if asiento_id in self.asientos_seleccionados:

            del self.asientos_seleccionados[asiento_id]
            self.botones_asientos[asiento_id].setStyleSheet(self._get_asiento_style('DISPONIBLE'))
        else:
            if len(self.asientos_seleccionados) < self.max_asientos:
                self.asientos_seleccionados[asiento_id] = True
                self.botones_asientos[asiento_id].setStyleSheet(self._get_asiento_style('SELECCIONADO'))
            else:
                QMessageBox.warning(self, "Límite Excedido", 
                                    f"Solo puedes seleccionar {self.max_asientos} asientos.")
        self._actualizar_contador()

    def _actualizar_contador(self):
        conteo = len(self.asientos_seleccionados)
        asientos_str = ", ".join(sorted(self.asientos_seleccionados.keys()))
        self.contador_label.setText(f"Asientos seleccionados: <b>{conteo} / {self.max_asientos}</b> ({asientos_str})")
        
        self.btn_avanzar.setEnabled(conteo == self.max_asientos)
        estilo_base = "font: 14pt Calibri; font-weight: bold; border-radius: 8px; padding: 10px 20px;"
        
        if conteo == self.max_asientos:
            self.btn_avanzar.setStyleSheet(f"background-color: {self.COLOR_PRINCIPAL}; color: white; {estilo_base}")
        else:
            self.btn_avanzar.setStyleSheet(f"background-color: gray; color: white; {estilo_base}")


    def _validar_y_avanzar(self):
        if len(self.asientos_seleccionados) != self.max_asientos:
            return

        self.main_window.registrar_asientos(sorted(self.asientos_seleccionados.keys()))

    def armar_ventana(self):
        self.crear_pasos_navegacion(3) 
        
        titulo = QLabel("Paso 3: Selecciona tus Asientos", 
                        font=QFont("Calibri", 22, QFont.Weight.Bold), 
                        alignment=Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("color: #000080; margin-top: 10px;")
        self.layout_maestro.addWidget(titulo)
        
        self.resumen_label = QLabel("", font=QFont("Calibri", 14), alignment=Qt.AlignmentFlag.AlignCenter)
        self.resumen_label.setStyleSheet("padding: 10px; color: #333;")
        self.layout_maestro.addWidget(self.resumen_label)
        
        self.layout_maestro.addSpacing(15)
        
        mapa_asientos = self._crear_panel_asientos()
        
        # Contenedor para el mapa de asientos
        vbox_wrap = QVBoxLayout()
        vbox_wrap.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        vbox_wrap.addWidget(mapa_asientos)
        
        self.layout_maestro.addLayout(vbox_wrap)
        self.layout_maestro.addStretch() 

        self.layout_maestro.addLayout(self._crear_pie_pagina())
        
        self._actualizar_contador()

    #Creacion del mapa de asientos 
    def _crear_panel_asientos(self):
        panel = QWidget()
        diseno_asientos = QGridLayout(panel)
        diseno_asientos.setSpacing(10) 
        
        for fila_idx, fila_num in enumerate(range(1, 6), 1):
            
            label_fila = QLabel(str(fila_num), alignment=Qt.AlignmentFlag.AlignCenter)
            diseno_asientos.addWidget(label_fila, fila_idx, 0) 
            
            for col_idx, col_letra in enumerate(self.COLUMNAS, 1):
                
                if fila_idx == 1:
                    label_col = QLabel(col_letra, alignment=Qt.AlignmentFlag.AlignCenter)
                    label_col.setFont(QFont("Calibri", 12, QFont.Weight.Bold))
                    diseno_asientos.addWidget(label_col, 0, col_idx) 
           

                asiento_id = f"{fila_num}{col_letra}"
                btn = QPushButton(asiento_id)
                btn.setStyleSheet(self._get_asiento_style('DISPONIBLE'))
                btn.clicked.connect(lambda checked, a=asiento_id: self._toggle_asiento(a))
                self.botones_asientos[asiento_id] = btn
                
                diseno_asientos.addWidget(btn, fila_idx, col_idx) 
        
        diseno_asientos.setRowStretch(len(self.COLUMNAS), 1) 
        
        return panel

    def _crear_pie_pagina(self):
        diseno_pie = QHBoxLayout()
        diseno_pie.setContentsMargins(50, 20, 50, 20)
        
        btn_atras = QPushButton("← Atrás", styleSheet="font: 14pt Calibri; font-weight: bold; border-radius: 8px; padding: 10px 20px; background-color: gray; color: white;")
        btn_atras.clicked.connect(lambda: self.main_window.goto_paso(1))
        diseno_pie.addWidget(btn_atras)
        
        self.contador_label = QLabel("", font=QFont("Calibri", 12))
        self.contador_label.setStyleSheet("padding-left: 20px; color: #000080;")
        diseno_pie.addWidget(self.contador_label)
        
        diseno_pie.addStretch()

        self.btn_avanzar = QPushButton("Finalizar Selección y Pagar →")
        self.btn_avanzar.setEnabled(False) 
        self.btn_avanzar.clicked.connect(self._validar_y_avanzar) 
        
        estilo_btn = "font: 14pt Calibri; font-weight: bold; border-radius: 8px; padding: 10px 20px;"
        self.btn_avanzar.setStyleSheet(f"background-color: gray; color: white; {estilo_btn}")
        
        diseno_pie.addWidget(self.btn_avanzar)

        return diseno_pie