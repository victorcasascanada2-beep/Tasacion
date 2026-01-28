import streamlit as st
from google import genai
from google.genai import types
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
        except: continue

    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 40px; color: #333; line-height: 1.6; background-color: #f0f2f0; }}
            .container {{ background: #fff; padding: 35px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 950px; margin: auto; border-top: 8px solid #2e7d32; }}
            .header {{ border-bottom: 2px solid #eee; padding-bottom: 15px; margin-bottom: 25px; display: flex; justify-content: space-between; align-items: center; }}
            h1 {{ color: #2e7d32; margin: 0; font-size: 26px; }}
            .ficha-tecnica {{ display: grid; grid-template-columns: 1fr 1fr; gap: 15px; background: #f1f8e9; padding: 20px; border-radius: 8px; border: 1px solid #dcedc8; }}
            .section-title {{ color: #1b5e20; border-bottom: 2px solid #a5d6a7; padding-bottom: 5px; margin-top: 35px; font-weight: bold; text-transform: uppercase; }}
            .resultado-ia {{ background: #ffffff; padding: 15px; border-radius: 5px; font-size: 14px; white-space: pre-wrap; }}
            .footer {{ margin-top: 50px; font-size: 11px; color: #777; text-align: center; border-top: 1px solid #eee; padding-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div><h1>INFORME DE PERITAJE TÉCNICO</h1><div style="color: #2e7d32; font-weight: bold;">Agrícola Noroeste</div></div>
                <div style="text-align: right; font-size: 13px;"><strong>Fecha:</strong> {time.strftime("%d/%m/%Y")}</div>
            </div>
            <div class="ficha-tecnica">
                <div><strong>🚜 Marca y Modelo:</strong> {marca} {modelo}</div>
                <div><strong>📅 Año:</strong> {anio}</div>
                <div><strong>⏳ Horas:</strong> {horas}</div>
            </div>
            <div class="section-title">Análisis de Mercado y Valoración IA</div>
            <div class="resultado-ia">{resultado_ia}</div>
            <div class="section-title">Evidencia Fotográfica</div>
            <div style="text-align: center;">{fotos_html}</div>
            <div class="footer">Este informe es una estimación generada mediante IA profesional.</div>
        </div>
    </body>
    </html>
    """
    return html

# --- INTERFAZ ---
st.title("🚜 Peritaje Profesional Agrícola Noroeste")

c1, c2, c3, c4 = st.columns(4)
with c1: marca = st.text_input("Marca")
with c2: modelo = st.text_input("Modelo")
with c3: anio = st.text_input("Año")
with c4: horas = st.number_input("Horas", min_value=0)
observaciones = st.text_area("Extras e Incidencias (Pala, GPS, Ruedas...)")

fotos_subidas = st.file_uploader("📸 Fotos del Tractor (mínimo 5)", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

if st.button("🚀 REALIZAR TASACIÓN PROFESIONAL"):
    if not marca or not modelo or len(fotos_subidas) < 5:
        st.warning("⚠️ Rellena los datos y sube al menos 5 fotos.")
    else:
        try:
            # USAMOS EL NUEVO CLIENTE QUE HAS DESCUBIERTO
            client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
            
            # Preparamos el paquete de contenido (Texto + Fotos)
            prompt = f"""
            Actúa como experto tasador de Agrícola Noroeste.
            Analiza este {marca} {modelo} del año {anio} con {horas} horas.
            
            TAREAS:
            1. Analiza el estado visual a través de las fotos adjuntas.
            2. Busca precios reales de mercado en Agriaffaires, Tractorpool y E-farm para unidades similares.
            3. Genera una tabla comparativa de 10-15 unidades.
            4. Calcula:
               - Precio Venta (Aterrizaje).
               - Precio Compra recomendado para Agrícola Noroeste.
            
            Notas adicionales: {observaciones}
            """
            
            # Convertimos las fotos al formato que pide el nuevo cliente
            contenidos = [prompt]
            for f in fotos_subidas:
                img = Image.open(f)
                contenidos.append(img)

            with st.spinner('🔍 Analizando fotos y mercado europeo...'):
                # Usamos el nombre de modelo que viste en tu Model Garden
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=contenidos
                )

            st.success("✅ Tasación Finalizada")
            st.markdown(response.text)
            
            informe_html = generar_html_informe(marca, modelo, anio, horas, observaciones, response.text, fotos_subidas)
            st.download_button("📥 Descargar Informe PDF/HTML", data=informe_html, file_name=f"Tasacion_{modelo}.html", mime="text/html")

        except Exception as e:
            st.error(f"❌ Error crítico: {e}")
