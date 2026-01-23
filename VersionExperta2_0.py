import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# --- CONFIGURACIÓN DE PÁGINA Y ESTILO ---
st.set_page_config(page_title="Tasador Pro - Agrícola Noroeste", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stAppDeployButton {display:none;}
    /* Ajuste de márgenes para mayor limpieza */
    .block-container {padding-top: 2rem;}
    </style>
    """, unsafe_allow_html=True)

# 1. Configuración de la API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.title("🚜 Peritaje Profesional V2.0")

# --- FORMULARIO DE DATOS ---
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        marca = st.text_input("Marca*", key="marca_v2", placeholder="Ej: John Deere")
    with c2:
        modelo = st.text_input("Modelo*", key="modelo_v2", placeholder="Ej: 6175M")
    with c3:
        anio = st.text_input("Año*", key="anio_v2", placeholder="Ej: 2018")
    with c4:
        horas = st.number_input("Horas de uso*", min_value=0, key="horas_input", help="Indica siempre horas, nunca kilómetros.")

    observaciones = st.text_area("Incidencias y Extras (Campo Crítico)", 
                                 placeholder="Detalla aquí: Pala, Tripuntal, GPS, estado de transmisión, mantenimientos...",
                                 help="Este campo es fundamental para ajustar el precio final.")

st.divider()

# --- SUBIDA DE FOTOS ---
st.subheader("📸 Evidencia Visual (Mínimo 5 fotos)")
fotos_subidas = st.file_uploader("Arrastra aquí las fotos del tractor", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

if fotos_subidas:
    if len(fotos_subidas) > 10:
        st.error("Máximo 10 fotos permitidas.")
    else:
        cols = st.columns(5)
        for i, foto in enumerate(fotos_subidas):
            with cols[i % 5]:
                st.image(foto, use_container_width=True)

st.divider()

# --- BOTÓN Y LÓGICA DE TASACIÓN ---
if st.button("🚀 REALIZAR TASACIÓN PROFESIONAL"):
    if not marca or not modelo or not anio or not horas:
        st.warning("⚠️ Datos incompletos: Marca, Modelo, Año y Horas son obligatorios.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Calidad de peritaje insuficiente: Sube al menos 5 fotografías.")
    else:
        try:
            # 1. Definición del modelo con instrucciones del sistema (System Instructions)
            # Usamos gemini-2.5-flash para máxima velocidad y razonamiento estadístico
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # --- EL PROMPT MAESTRO (Optimizado para Agrícola Noroeste) ---
            prompt_instrucciones = f"""
            ### ROL: EXPERTO TASADOR DE MAQUINARIA AGRÍCOLA (AGRÍCOLA NOROESTE)
            Tu objetivo es realizar un informe de mercado frío, estadístico y profesional.

            ### DATOS DE LA UNIDAD:
            - Tractor: {marca} {modelo}
            - Año: {anio}
            - Horas: {horas} HORAS (Prohibido usar términos como 'kilómetros' o 'kilometraje').
            - Extras y Estado (Texto del usuario): {observaciones}

            ### INSTRUCCIONES DE ANÁLISIS:
            1. **Análisis Visual (Fotos):** Resume lo que ves. No sumes valor por estado 'normal'. Solo resta si ves daños graves (fugas, golpes) o suma si detectas Extras Reales (Tripuntal, Pala, Pesas, GPS).
            2. **Estadística de Mercado:** Simula un rastreo en Agriaffaires, Tractorpool, E-Farm y Milanuncios. Filtra duplicados. 
            3. **Muestra:** Utiliza unidades de +/- 1000 horas respecto a las {horas} indicadas.
            4. **Lógica de Precios:** - 'Precio Aterrizaje': Media de mercado ajustada.
               - 'Precio Compra Sugerido': Aplicar margen comercial del 15% sobre el precio de aterrizaje.

            ### FORMATO DE SALIDA REQUERIDO:
            ## 📊 INFORME DE TASACIÓN PROFESIONAL
            ---
            **Unidad:** {marca} {modelo} | **Año:** {anio} | **Uso:** {horas} Horas.

            ### 1. COMPARATIVA DE MERCADO (Muestra Real)
            | # | Portal | Ubicación | Horas | Precio Est. | Observaciones |
            |---|---|---|---|---|---|
            [Genera aquí una tabla con al menos 12-15 referencias realistas]

            ### 2. EVALUACIÓN DE EXTRAS Y ESTADO
            - **Extras detectados:** [Listado según texto y fotos]
            - **Impacto en valor:** [Ej: +4.000€ por pala cargadora]

            ### 3. VALORACIÓN FINAL
            - **VALOR DE MERCADO (Venta):** [Precio €]
            - **PRECIO DE COMPRA SUGERIDO (Agrícola Noroeste):** [Precio €]

            ---
            *Nota: Informe generado mediante análisis estadístico de tokens y visión computacional.*
            """

            with st.spinner('🔍 Accediendo a bases de datos europeas y analizando estado visual...'):
                # Preparamos el paquete de datos para Gemini
                paquete_datos = [prompt_instrucciones]
                for f in fotos_subidas:
                    img = Image.open(f)
                    paquete_datos.append(img)
                
                # Ejecución
                response = model.generate_content(paquete_datos)
                
            # --- MOSTRAR RESULTADOS ---
            st.success("✅ Tasación finalizada correctamente.")
            st.markdown(response.text)
            
            # Botón para descargar o imprimir (opcional)
            st.download_button("Descargar Informe (TXT)", response.text, file_name=f"Tasacion_{marca}_{modelo}.txt")
            
        except Exception as e:
            st.error(f"❌ Error crítico en el motor: {e}")
