import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Tasador Pro - Agrícola Noroeste", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    .block-container {padding-top: 2rem;}
    </style>
    """, unsafe_allow_html=True)

# 1. Configuración de la API con manejo de errores profesional
try:
    # Usamos la clave de los Secrets de Streamlit
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Error: No se encontró 'GOOGLE_API_KEY' en los Secrets de Streamlit.")

# --- FUNCIÓN PARA GENERAR EL INFORME HTML ---
def generar_html_informe(marca, modelo, anio, horas, observaciones, resultado_ia, fotos):
    fotos_html = ""
    for foto in fotos:
        try:
            img = Image.open(foto)
            img.thumbnail((500, 500)) 
            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=85)
            encoded_string = base64.b64encode(buffered.getvalue()).decode()
            fotos_html += f'''
                <div style="display: inline-block; margin: 10px; text-align: center; border: 1px solid #ddd; padding: 5px; border-radius: 5px; background: #fff;">
                    <img src="data:image/jpeg;base64,{encoded_string}" style="width:220px; height:160px; object-fit: cover; border-radius: 3px;">
                </div>'''
        except Exception:
            continue

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 40px; color: #333; line-height: 1.6; background-color: #f0f2f0; }}
            .container {{ background: #fff; padding: 35px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 950px; margin: auto; border-top: 8px solid #2e7d32; }}
            .header {{ border-bottom: 2px solid #eee; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; }}
            h1 {{ color: #2e7d32; margin: 0; font-size: 26px; letter-spacing: -1px; }}
            .ficha-tecnica {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; background: #f1f8e9; padding: 20px; border-radius: 8px; border: 1px solid #dcedc8; }}
            .section-title {{ color: #1b5e20; border-bottom: 2px solid #a5d6a7; padding-bottom: 5px; margin-top: 35px; font-weight: bold; text-transform: uppercase; font-size: 16px; }}
            .resultado-ia {{ background: #ffffff; padding: 10px; border-radius: 5px; font-size: 14px; color: #444; }}
            .fotos-grid {{ text-align: center; margin-top: 25px; background: #f9f9f9;
