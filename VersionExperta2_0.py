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

# 1. Configuración de la API
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("⚠️ No se encontró 'GOOGLE_API_KEY' en los Secrets.")
except Exception as e:
    st.error(f"Error de configuración: {e}")

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
            .fotos-grid {{ text-align: center; margin-top: 25px; background: #f9f9f9; padding: 15px; border-radius: 8px; }}
            .footer {{ margin-top: 50px; font-size: 11px; color: #777; text-align: center; border-top: 1px solid #eee; padding-top: 15px; font-style: italic; }}
            pre {{ white-space: pre-wrap; word-wrap: break-word; font-family: inherit; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div>
                    <h1>INFORME DE PERITAJE TÉCNICO</h1>
                    <div style="color: #2e7d32; font-weight: bold;">Agrícola Noroeste</div>
                </div>
                <div style="text-align: right; font-size: 13px; color: #666;">
                    <strong>ID Informe:</strong> AN-{int(time.time())}<br>
                    <strong>Fecha:</strong> {time.strftime("%d/%m/%Y")}
                </div>
            </div>
            <div class="ficha-tecnica">
                <div><strong>🚜 Marca y Modelo:</strong> {marca} {modelo}</div>
                <div><strong>📅 Año de Fab.:</strong> {anio}</div>
                <div><strong>⏳ Horas de uso:</strong> {horas} Horas</div>
                <div><strong>📍 Ubicación:</strong> Zamora (Sede Central)</div>
            </div>
            <div class="section-title">Equipamiento e Incidencias (Declarado)</div>
            <p style="font-size: 14px; color: #555; padding: 0 10px;">{observaciones if observaciones else "No se han declarado extras adicionales."}</p>
            <div class="section-title">Estudio Estadístico de Mercado y Valoración IA</div>
            <div class="resultado-ia"><pre>{resultado_ia}</pre></div>
            <div class="section-title">Evidencia Fotográfica de la Inspección</div>
            <div class="fotos-grid">{fotos_html}</div>
            <div class="footer">Este informe es una estimación estadística generada mediante IA profesional.</div>
        </div>
    </body>
    </html>
    """
    return html

# --- INTERFAZ DE USUARIO ---
st.title("🚜 Peritaje Profesional V2.0")

marca = st.text_input("Marca*", placeholder="Ej: John Deere")
modelo = st.text_input("Modelo*", placeholder="Ej: 6175M")
anio = st.text_input("Año*", placeholder="Ej: 2018")
horas = st.number_input("Horas de uso*", min_value=0)
observaciones = st.text_area("Incidencias y Extras", placeholder="Pala, tripuntal, estado de ruedas...")

st.subheader("📸 Fotografías (Mínimo 5)")
fotos_subidas = st.file_uploader("Subir archivos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if st.button("🚀 REALIZAR TASACIÓN PROFESIONAL"):
    if not marca or not modelo or not anio or not horas:
        st.warning("⚠️ Complete los campos obligatorios.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Se requieren al menos 5 fotografías.")
    else:
        try:
            # Seleccionamos el modelo profesional de Vertex
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Realiza una tasación experta para un {marca} {modelo} del {anio} con {horas} horas. Analiza las fotos y extras: {observaciones}."

            with st.spinner('🔍 Analizando...'):
                paquete = [prompt]
                for f in fotos_subidas:
                    paquete.append(Image.open(f))
                
                response = model.generate_content(paquete)
            
            st.success("✅ Informe Generado")
            informe_html = generar_html_informe(marca, modelo, anio, horas, observaciones, response.text, fotos_subidas)
            
            st.download_button("📥 Descargar Informe", data=informe_html, file_name="tasacion.html", mime="text/html")
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
