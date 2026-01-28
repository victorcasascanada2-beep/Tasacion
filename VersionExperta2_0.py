import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO
import time  # <--- ERROR CORREGIDO: Importación necesaria para la fecha

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

# 1. Configuración de la API (Asegúrate de tener la KEY en Secrets de Streamlit)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("Configuración de API no encontrada. Verifica los Secrets.")

# --- FUNCIÓN PARA GENERAR EL INFORME HTML ---
def generar_html_informe(marca, modelo, anio, horas, observaciones, resultado_ia, fotos):
    # Procesamiento de fotos a HTML (Base64)
    fotos_html = ""
    for foto in fotos:
        try:
            # Redimensionar para que el HTML no pese demasiado y sea fluido
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

    # Estructura del documento profesional
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
            .resultado-ia {{ background: #ffffff; padding: 10px; border-radius: 5px; font-size: 14px; color: #444; overflow-x: auto; }}
            .fotos-grid {{ text-align: center; margin-top: 25px; background: #f9f9f9; padding: 15px; border-radius: 8px; }}
            .footer {{ margin-top: 50px; font-size: 11px; color: #777; text-align: center; border-top: 1px solid #eee; padding-top: 15px; font-style: italic; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            th {{ background-color: #2e7d32; color: white; padding: 12px; text-align: left; font-size: 13px; }}
            td {{ padding: 10px; border-bottom: 1px solid #eee; font-size: 13px; }}
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
            <div class="resultado-ia">
                <pre>{resultado_ia}</pre>
            </div>

            <div class="section-title">Evidencia Fotográfica de la Inspección</div>
            <div class="fotos-grid">
                {fotos_html}
            </div>

            <div class="footer">
                Este informe es una estimación estadística generada mediante IA (Gemini 2.5 Flash). 
                Agrícola Noroeste no se hace responsable de variaciones de mercado post-emisión.
            </div>
        </div>
    </body>
    </html>
    """
    return html

# --- INTERFAZ DE USUARIO ---
st.title("🚜 Peritaje Profesional V2.0")

with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        marca = st.text_input("Marca*", placeholder="Ej: John Deere")
    with c2:
        modelo = st.text_input("Modelo*", placeholder="Ej: 6175M")
    with c3:
        anio = st.text_input("Año*", placeholder="Ej: 2018")
    with c4:
        horas = st.number_input("Horas de uso*", min_value=0)

    observaciones = st.text_area("Incidencias y Extras (Campo Crítico)", 
                                 placeholder="Describa aquí: Pala, tripuntal, estado de ruedas, GPS...")

st.divider()

st.subheader("📸 Fotografías del Peritaje (Mínimo 5)")
fotos_subidas = st.file_uploader("Subir archivos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if fotos_subidas:
    cols = st.columns(5)
    for i, foto in enumerate(fotos_subidas[:10]):
        with cols[i % 5]:
            st.image(foto, use_container_width=True)

st.divider()

if st.button("🚀 REALIZAR TASACIÓN PROFESIONAL"):
    if not marca or not modelo or not anio or not horas:
        st.warning("⚠️ Complete todos los campos obligatorios.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Se requieren al menos 5 fotografías para validar la unidad.")
    else:
        try:
            # Usamos el modelo configurado
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            
            prompt_instrucciones = f"""
            ### ROL: EXPERTO TASADOR DE MAQUINARIA AGRÍCOLA (AGRÍCOLA NOROESTE)
            Realiza un informe técnico-estadístico detallado para un {marca} {modelo} del año {anio} con {horas} HORAS.
            
            INSTRUCCIONES CRÍTICAS:
            1. Analiza las fotos para confirmar anclajes, estado de neumáticos y limpieza.
            2. Busca y genera una tabla comparativa de 15 unidades en Agriaffaires, Tractorpool y E-Farm con +/- 1000 horas.
            3. PROHIBIDO usar 'kilómetros'. Siempre usa 'Horas'.
            4. Extras declarados: {observaciones}

            ESTRUCTURA DE SALIDA:
            - Resumen del estado visual.
            - Tabla de mercado europeo.
            - Valoración final (Precio Aterrizaje y Precio Compra Agrícola Noroeste).
            """

            with st.spinner('🔍 Analizando fotos y rastreando precios en portales europeos...'):
                paquete = [prompt_instrucciones]
                for f in fotos_subidas:
                    # Cargamos las imágenes para la IA
                    img_ia = Image.open(f)
                    paquete.append(img_ia)
                
                response = model.generate_content(paquete)
            
            st.success("✅ Informe Generado con Éxito")
            
            # Previsualización en Streamlit
            with st.expander("👀 Ver Informe Preliminar"):
                st.markdown(response.text)
            
            # Generación del archivo HTML con los datos corregidos
            informe_html = generar_html_informe(marca, modelo, anio, horas, observaciones, response.text, fotos_subidas)
            
            # Botón de descarga
            st.download_button(
                label="📥 Descargar Informe Oficial HTML (Con Fotos)",
                data=informe_html,
                file_name=f"Informe_Tasacion_{marca}_{modelo}_{time.strftime('%Y%m%d')}.html",
                mime="text/html"
            )
            
        except Exception as e:
            st.error(f"❌ Error en el proceso: {e}")
