import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Tasador Pro - Agrícola Noroeste", layout="wide")

# 1. Configuración de la API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("⚠️ Error: Configura GOOGLE_API_KEY en los Secrets.")

# --- FUNCIÓN PARA GENERAR EL INFORME HTML ---
def generar_html_informe(marca, modelo, anio, horas, observaciones, resultado_ia, fotos):
    fotos_html = ""
    for foto in fotos:
        try:
            img = Image.open(foto)
            img.thumbnail((400, 400)) 
            buffered = BytesIO()
            img.save(buffered, format="JPEG", quality=80)
            encoded_string = base64.b64encode(buffered.getvalue()).decode()
            fotos_html += f'<img src="data:image/jpeg;base64,{encoded_string}" style="width:200px; margin:5px; border-radius:5px;">'
        except: continue

    html = f"""
    <html>
    <body style="font-family: sans-serif; padding: 20px;">
        <h1 style="color: #2e7d32;">INFORME DE TASACIÓN - AGRÍCOLA NOROESTE</h1>
        <p><strong>🚜 Equipo:</strong> {marca} {modelo} ({anio}) - {horas} horas</p>
        <hr>
        <h3>Análisis de Mercado e IA:</h3>
        <div style="background: #f9f9f9; padding: 15px; border-radius: 10px; white-space: pre-wrap;">{resultado_ia}</div>
        <hr>
        <h3>Evidencia Fotográfica:</h3>
        {fotos_html}
    </body>
    </html>
    """
    return html

# --- INTERFAZ ---
st.title("🚜 Tasador Profesional (Vertex AI)")

marca = st.text_input("Marca")
modelo = st.text_input("Modelo")
anio = st.text_input("Año")
horas = st.number_input("Horas", min_value=0)
observaciones = st.text_area("Notas técnicas")

fotos_subidas = st.file_uploader("Fotos (mínimo 5)", type=['jpg', 'png'], accept_multiple_files=True)

if st.button("🚀 REALIZAR TASACIÓN"):
    if len(fotos_subidas) < 5:
        st.warning("Sube al menos 5 fotos.")
    else:
        try:
            # PRUEBA 1: Nombre estándar
            model_name = 'gemini-1.5-flash'
            
            # Si el error 404 persiste, Google Cloud a veces requiere este formato:
            # model_name = 'publishers/google/models/gemini-1.5-flash'
            
            model = genai.GenerativeModel(model_name)
            
            with st.spinner('Conectando con Vertex AI...'):
                paquete = [f"Tasación técnica para {marca} {modelo}. Analiza mercado y fotos. Extras: {observaciones}"]
                for f in fotos_subidas:
                    paquete.append(Image.open(f))
                
                response = model.generate_content(paquete)
            
            st.success("✅ Tasación completada")
            st.markdown(response.text)
            
            html = generar_html_informe(marca, modelo, anio, horas, observaciones, response.text, fotos_subidas)
            st.download_button("📥 Descargar Informe", data=html, file_name="informe.html", mime="text/html")
            
        except Exception as e:
            st.error(f"❌ El modelo no responde: {e}")
            st.info("💡 Consejo: Si el error es 404, ve a tu Google Cloud y asegúrate de que 'Generative Language API' esté habilitada en el proyecto Tasador-Profesional-2026.")
