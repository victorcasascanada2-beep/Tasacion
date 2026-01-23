import streamlit as st
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO

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
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# --- FUNCIÓN PARA GENERAR EL INFORME HTML ---
def generar_html_informe(marca, modelo, anio, horas, observaciones, resultado_ia, fotos):
    # Procesamiento de fotos a HTML (Base64)
    fotos_html = ""
    for foto in fotos:
        try:
            # Redimensionar para que el HTML no pese demasiado
            img = Image.open(foto)
            img.thumbnail((400, 400)) 
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            encoded_string = base64.b64encode(buffered.getvalue()).decode()
            fotos_html += f'''
                <div style="display: inline-block; margin: 10px; text-align: center; border: 1px solid #ddd; padding: 5px; border-radius: 5px;">
                    <img src="data:image/jpeg;base64,{encoded_string}" style="width:200px; height:150px; object-fit: cover;">
                </div>'''
        except:
            continue

    # Estructura del documento
    html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 40px; color: #333; line-height: 1.6; background-color: #f4f4f4; }}
            .container {{ background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 0 20px rgba(0,0,0,0.1); max-width: 900px; margin: auto; }}
            .header {{ border-bottom: 4px solid #2e7d32; padding-bottom: 10px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
            h1 {{ color: #2e7d32; margin: 0; font-size: 24px; }}
            .ficha-tecnica {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; background: #e8f5e9; padding: 15px; border-radius: 5px; }}
            .section-title {{ color: #2e7d32; border-left: 5px solid #2e7d32; padding-left: 10px; margin-top: 30px; font-weight: bold; text-transform: uppercase; }}
            .resultado-ia {{ background: #ffffff; border: 1px solid #eee; padding: 20px; border-radius: 5px; white-space: pre-line; }}
            .fotos-grid {{ text-align: center; margin-top: 20px; }}
            .footer {{ margin-top: 40px; font-size: 10px; color: #999; text-align: center; border-top: 1px solid #eee; padding-top: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 12px; }}
            th {{ background-color: #2e7d32; color: white; padding: 10px; text-align: left; }}
            td {{ padding: 8px; border-bottom: 1px solid #eee; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>INFORME DE PERITAJE PROFESIONAL</h1>
                <span style="color: #666;">Agrícola Noroeste</span>
            </div>
            
            <div class="ficha-tecnica">
                <div><strong>Modelo:</strong> {marca} {modelo}</div>
                <div><strong>Año de fabricación:</strong> {anio}</div>
                <div><strong>Horas de uso:</strong> {horas} Horas</div>
                <div><strong>Fecha tasación:</strong> {time.strftime("%d/%m/%Y")}</div>
            </div>

            <div class="section-title">Incidencias y Extras Declarados</div>
            <p style="font-size: 14px;">{observaciones if observaciones else "Sin extras adicionales declarados."}</p>

            <div class="section-title">Análisis Estadístico y Valoración IA</div>
            <div class="resultado-ia">{resultado_ia}</div>

            <div class="section-title">Evidencias Fotográficas del Peritaje</div>
            <div class="fotos-grid">
                {fotos_html}
            </div>

            <div class="footer">
                Documento generado mediante Inteligencia Artificial Gemini 2.5 Flash para uso exclusivo de Agrícola Noroeste. 
                Los valores son estimaciones estadísticas basadas en el mercado europeo actual.
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
                                 placeholder="Describa aquí pala, tripuntal, estado de ruedas...")

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
        st.warning("⚠️ Complete todos los campos marcados con *.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Se requieren al menos 5 fotografías para validar el estado.")
    else:
        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt_instrucciones = f"""
            ### ROL: EXPERTO TASADOR DE MAQUINARIA AGRÍCOLA (AGRÍCOLA NOROESTE)
            Realiza un informe técnico-estadístico para un {marca} {modelo} del año {anio} con {horas} HORAS.
            
            INSTRUCCIONES:
            1. Analiza las fotos para detectar extras (Tripuntal, Pala, GPS) o daños.
            2. Simula una muestra de 15 unidades de Agriaffaires, Tractorpool y E-Farm con +/- 1000 horas.
            3. Prohibido usar el término 'kilómetros'. Siempre usa 'Horas'.
            4. Extras declarados por el usuario: {observaciones}

            FORMATO: Devuelve el texto estructurado con tablas Markdown.
            """

            with st.spinner('🔍 Generando informe pericial y analizando mercado...'):
                paquete = [prompt_instrucciones]
                for f in fotos_subidas:
                    paquete.append(Image.open(f))
                
                response = model.generate_content(paquete)
            
            st.success("✅ Informe Generado")
            
            # Mostrar resultado en la App
            with st.expander("👀 Previsualizar Informe de la IA", expanded=True):
                st.markdown(response.text)
            
            # Generar y ofrecer descarga de HTML
            informe_html = generar_html_informe(marca, modelo, anio, horas, observaciones, response.text, fotos_subidas)
            
            st.download_button(
                label="📥 Descargar Informe Oficial (HTML con Fotos)",
                data=informe_html,
                file_name=f"Peritaje_{marca}_{modelo}.html",
                mime="text/html"
            )
            
        except Exception as e:
            st.error(f"❌ Error en el proceso: {e}")
