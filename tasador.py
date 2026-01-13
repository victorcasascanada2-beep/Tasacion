import streamlit as st
import importlib

# AQUÍ es donde mandas tú. 
# Si el archivo se llama VersionEstable1_0.py, ponlo aquí sin el .py
VERSION_ACTIVA = "VersionEstable1_0" 

def cargar_app(nombre_modulo):
    try:
        # Aquí el programa busca el archivo que elegiste arriba
        importlib.import_module(nombre_modulo)
    except Exception as e:
        # Si te equivocas al escribir el nombre, te avisará aquí
        st.error(f"No he podido encontrar el archivo: {nombre_modulo}. Asegúrate de que el nombre en GitHub es exacto.")
        st.info("Error técnico: " + str(e))

# Esto arranca la versión elegida
cargar_app(VERSION_ACTIVA)
