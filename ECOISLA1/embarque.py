import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
QLabel, QPushButton, QFrame, QMessageBox, QDateEdit)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QDate 

from base_ui import VentanaBase, LOCALE_ESPANOL, FORMATO_FECHA_ESPANOL

class VentanaEmbarques(VentanaBase): 
    
    FORMATO_FECHA_ESPANOL = FORMATO_FECHA_ESPANOL 

    def __init__(self, ventana_principal, parent=None):
        super().__init__(ventana_principal, parent) 
        self.setWindowTitle("ECO ISLAS - Paso 2: Selección de Viaje")
        self.setMinimumSize(800, 650) 
        
        self.cant_boletos = 0

        self.fecha_seleccionada = LOCALE_ESPANOL.toString(QDate.currentDate(), self.FORMATO_FECHA_ESPANOL)
        self.embarcacion_seleccionada = None
        self.horario_seleccionado = None
        
        self.embarcaciones = {
            "Esmeralda": ["Mañana", "Tarde", "Noche"],
            "Goleta": ["Mañana", "Tarde", "Noche"],
            "Covadonga": ["Mañana", "Tarde", "Noche"]
        }
        
        self.cards = {}
        self.botones_horario = {} 
        
        self.armar_ventana()
        
    def actualizar_datos(self, cant_boletos):
        self.cant_boletos = cant_boletos
        self.embarcacion_seleccionada = None
        self.horario_seleccionado = None
        for card in self.cards.values():
            card.setStyleSheet(self._get_card_style(False))
        for btn in self.botones_horario.values():
            btn.setStyleSheet(self._get_horario_style(False))


    def _get_card_style(self, activo):
        base = "border: 1px solid #D3D3D3; border-radius: 12px; padding: 15px; background-color: white;"
        if activo:
            return "border: 3px solid #000080; border-radius: 12px; padding: 15px; background-color: #e0f0ff;"
        return base

    def _get_horario_style(self, activo):
        base = "font: 12pt Calibri; font-weight: bold; border-radius: 5px; padding: 5px 10px;"
        if activo:
            return base + f"background-color: {self.COLOR_PRINCIPAL}; color: white; border: 1px solid #38761D;" 
        return base + "background-color: #D3D3D3; color: #333; border: 1px solid #D3D3D3;"

    def _seleccionar_horario(self, nombre_embarcacion, horario):
        
        self.embarcacion_seleccionada = nombre_embarcacion
        self.horario_seleccionado = horario
        
        for card_name, card in self.cards.items():
            card.setStyleSheet(self._get_card_style(card_name == nombre_embarcacion))
            
        for e_name, horarios in self.embarcaciones.items():
            for h_name in horarios:
                btn = self.botones_horario[(e_name, h_name)]
                is_active = (e_name == nombre_embarcacion and h_name == horario)
                btn.setStyleSheet(self._get_horario_style(is_active))
                
        self._validar_y_avanzar()

    def _validar_y_avanzar(self):
        if not self.fecha_seleccionada or not self.embarcacion_seleccionada or not self.horario_seleccionado:
            return

        self.main_window.registrar_viaje(
            embarcacion=self.embarcacion_seleccionada, 
            horario=self.horario_seleccionado
        )


    def armar_ventana(self):
        self.crear_pasos_navegacion(2) 
        
        diseno_contenido = QVBoxLayout()
        diseno_contenido.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        diseno_contenido.setContentsMargins(50, 20, 50, 20) 

        titulo = QLabel("Selecciona la Fecha, Embarcación y Horario de tu Viaje", 
                        font=QFont("Calibri", 22, QFont.Weight.Bold), 
                        alignment=Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("color: #000080; margin-bottom: 20px;")
        diseno_contenido.addWidget(titulo)
        
        diseno_contenido.addLayout(self._crear_panel_fecha())
        diseno_contenido.addSpacing(30)
        
        diseno_contenido.addLayout(self._crear_panel_embarcaciones())
        
        diseno_contenido.addStretch()
        self.layout_maestro.addLayout(diseno_contenido)
        
        self.layout_maestro.addLayout(self._crear_pie_pagina())

    def _crear_panel_fecha(self):
        diseno_fecha = QHBoxLayout()
        diseno_fecha.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        
        label_fecha = QLabel("📅 <b>Fecha del Viaje:</b>", font=QFont("Calibri", 14))
        
        self.campo_fecha = QDateEdit(calendarPopup=True, date=QDate.currentDate(), minimumDate=QDate.currentDate())
        self.campo_fecha.setDisplayFormat("dd MMMM yyyy") 
        self.campo_fecha.setStyleSheet("QDateEdit {padding: 3px 8px; border: 1px solid #000080; border-radius: 4px; min-width: 150px;}")
        
        self.campo_fecha.dateChanged.connect(lambda d: 
            setattr(self, 'fecha_seleccionada', LOCALE_ESPANOL.toString(d, self.FORMATO_FECHA_ESPANOL)))
        
        diseno_fecha.addWidget(label_fecha)
        diseno_fecha.addWidget(self.campo_fecha)
        return diseno_fecha

    def _crear_panel_embarcaciones(self):
        diseno_embarques = QHBoxLayout()
        diseno_embarques.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        diseno_embarques.setSpacing(20) 
        
        for nombre, horarios in self.embarcaciones.items():
            card = self._crear_tarjeta_embarcacion(nombre, horarios)
            diseno_embarques.addWidget(card)
        return diseno_embarques

    def _crear_tarjeta_embarcacion(self, nombre, horarios_disponibles):
        
        tarjeta = QFrame(styleSheet=self._get_card_style(False))
        diseno_vertical = QVBoxLayout(tarjeta)
        diseno_vertical.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop) 
        diseno_vertical.setSpacing(15) 

        diseno_vertical.addWidget(QLabel(f"<b>{nombre}</b>", 
                                        font=QFont("Calibri", 18, QFont.Weight.Bold), 
                                        alignment=Qt.AlignmentFlag.AlignCenter))
        
        diseno_vertical.addSpacing(15)
        
        diseno_vertical.addWidget(QLabel("Horarios Disponibles", 
                                        font=QFont("Calibri", 14, QFont.Weight.Bold), 
                                        alignment=Qt.AlignmentFlag.AlignCenter))
        
        diseno_horarios = QVBoxLayout()
        diseno_horarios.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        diseno_horarios.setSpacing(5)
        
        for horario in horarios_disponibles:
            btn_horario = QPushButton(horario, styleSheet=self._get_horario_style(False))
            btn_horario.clicked.connect(lambda checked, h=horario, e=nombre: self._seleccionar_horario(e, h))
            self.botones_horario[(nombre, horario)] = btn_horario
            diseno_horarios.addWidget(btn_horario, alignment=Qt.AlignmentFlag.AlignCenter)
            
        diseno_vertical.addLayout(diseno_horarios)
        diseno_vertical.addStretch()
        self.cards[nombre] = tarjeta
        return tarjeta

    def _crear_pie_pagina(self):
        diseno_pie = QHBoxLayout()
        diseno_pie.setContentsMargins(50, 20, 50, 20) 
        estilo_btn = "font: 14pt Calibri; font-weight: bold; border-radius: 8px; padding: 10px 20px;"

        btn_atras = QPushButton("← Atrás", styleSheet=f"background-color: gray; color: white; {estilo_btn}")
        btn_atras.clicked.connect(lambda: self.main_window.goto_paso(0)) 
        diseno_pie.addWidget(btn_atras)

        diseno_pie.addStretch()

        btn_siguiente = QPushButton("Siguiente Paso →", styleSheet=f"background-color: {self.COLOR_PRINCIPAL}; color: white; {estilo_btn}")
        btn_siguiente.clicked.connect(self._validar_y_avanzar) 
        diseno_pie.addWidget(btn_siguiente)

        return diseno_pie