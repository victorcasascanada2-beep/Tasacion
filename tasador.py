import streamlit as st
import os

# Asegúrate de que el nombre sea exacto y sin espacios
VERSION = "VersionExperta2_0.py"

if os.path.exists(VERSION):
    with open(VERSION, "r", encoding="utf-8") as f:
        code = f.read()
        exec(code, globals())
else:
    st.error(f"No se encuentra {VERSION}")
