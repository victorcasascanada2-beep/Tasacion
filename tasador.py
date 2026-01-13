import streamlit as st
import importlib.util
import sys

# 1. Nombre del archivo (SIN el .py)
VERSION_ACTIVA = "VersionExperta2_0" 

def cargar_modulo(nombre_archivo):
    spec = importlib.util.spec_from_file_location(nombre_archivo, f"{nombre_archivo}.py")
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nombre_archivo] = modulo
    spec.loader.exec_module(modulo)

try:
    cargar_modulo(VERSION_ACTIVA)
except Exception as e:
    st.error(f"Error cargando la aplicación: {e}")
    st.info("Asegúrate de que el archivo VersionExperta2_0.py existe en GitHub.")
