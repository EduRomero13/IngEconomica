"""
Módulo de gestión de datos para la aplicación de evaluación económica.
Maneja la persistencia y validación de datos en session_state.
"""

import streamlit as st
import json

# Variable global para almacenar backup de datos
_data_backup = {}

class DataManager:
    """Gestor centralizado de datos del proyecto"""
    
    # Valores por defecto
    DEFAULTS = {
        "costo_tanque": 750.0,
        "costo_bomba": 600.0,
        "costo_instalacion": 400.0,
        "vida_util": 8,
        "ahorro_anual": 700.0,
        "mantenimiento_anual": 100.0,
        "tmar_porcentaje": 10.0,
        "financiado": False,
        "tasa_nominal": 12.0,
        "periodos_capitalizacion": 12,
        "plazo_meses": 24
    }
    
    @staticmethod
    def initialize():
        """Inicializa session_state con valores por defecto si no existen"""
        # Intentar restaurar desde backup primero (ANTES de todo)
        DataManager.restore_from_backup()
        
        # Solo inicializar valores que NO existen (preserva cambios del usuario)
        for key, value in DataManager.DEFAULTS.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
        # Valores calculados (siempre actualizar)
        if "tmar_porcentaje" in st.session_state:
            st.session_state["tmar"] = st.session_state["tmar_porcentaje"] / 100
        
        if all(k in st.session_state for k in ["costo_tanque", "costo_bomba", "costo_instalacion"]):
            st.session_state["inversion_inicial"] = (
                st.session_state["costo_tanque"] +
                st.session_state["costo_bomba"] +
                st.session_state["costo_instalacion"]
            )
        
        st.session_state["data_initialized"] = True
        
        # Hacer backup de los datos
        DataManager.backup_data()
    
    @staticmethod
    def backup_data():
        """Guarda los datos actuales en un backup global"""
        global _data_backup
        _data_backup = {}
        for key in DataManager.DEFAULTS.keys():
            if key in st.session_state:
                _data_backup[key] = st.session_state[key]
    
    @staticmethod
    def restore_from_backup():
        """Restaura los datos desde el backup si existen"""
        global _data_backup
        if _data_backup:
            for key, value in _data_backup.items():
                if key not in st.session_state:
                    st.session_state[key] = value
            return True
        return False
    
    @staticmethod
    def update_inversion_inicial():
        """Actualiza la inversión inicial total"""
        st.session_state["inversion_inicial"] = (
            st.session_state.get("costo_tanque", 0) +
            st.session_state.get("costo_bomba", 0) +
            st.session_state.get("costo_instalacion", 0)
        )
        DataManager.backup_data()
    
    @staticmethod
    def update_tmar():
        """Actualiza TMAR en formato decimal"""
        st.session_state["tmar"] = st.session_state.get("tmar_porcentaje", 10.0) / 100
        DataManager.backup_data()
    
    @staticmethod
    def get_value(key, default=None):
        """Obtiene un valor de session_state de forma segura"""
        return st.session_state.get(key, default if default is not None else DataManager.DEFAULTS.get(key))
    
    @staticmethod
    def set_value(key, value):
        """Establece un valor en session_state"""
        st.session_state[key] = value
        
        # Actualizar valores derivados si es necesario
        if key in ["costo_tanque", "costo_bomba", "costo_instalacion"]:
            DataManager.update_inversion_inicial()
        elif key == "tmar_porcentaje":
            DataManager.update_tmar()
    
    @staticmethod
    def reset_to_defaults():
        """Resetea todos los valores a sus defaults"""
        for key, value in DataManager.DEFAULTS.items():
            st.session_state[key] = value
        DataManager.update_inversion_inicial()
        DataManager.update_tmar()
    
    @staticmethod
    def get_all_data():
        """Retorna un diccionario con todos los datos actuales"""
        data = {}
        for key in DataManager.DEFAULTS.keys():
            data[key] = st.session_state.get(key, DataManager.DEFAULTS[key])
        
        data["tmar"] = st.session_state.get("tmar", 0.10)
        data["inversion_inicial"] = st.session_state.get("inversion_inicial", 1750.0)
        
        return data
    
    @staticmethod
    def validate_data():
        """Valida que los datos sean coherentes"""
        errors = []
        
        # Validar valores numéricos positivos
        numeric_keys = ["costo_tanque", "costo_bomba", "costo_instalacion", 
                       "ahorro_anual", "mantenimiento_anual"]
        for key in numeric_keys:
            value = st.session_state.get(key, 0)
            if value < 0:
                errors.append(f"{key} no puede ser negativo")
        
        # Validar vida útil
        if st.session_state.get("vida_util", 0) <= 0:
            errors.append("La vida útil debe ser mayor a 0")
        
        # Validar TMAR
        if st.session_state.get("tmar_porcentaje", 0) < 0 or st.session_state.get("tmar_porcentaje", 0) > 100:
            errors.append("TMAR debe estar entre 0% y 100%")
        
        # Validar que ahorro sea mayor que mantenimiento
        if st.session_state.get("ahorro_anual", 0) < st.session_state.get("mantenimiento_anual", 0):
            errors.append("⚠️ El ahorro anual es menor que el mantenimiento (flujo neto negativo)")
        
        return errors
