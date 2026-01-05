import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Tasador Pro 2026", layout="centered")
st.title("🚜 Tasador Alta Potencia (Gemini Pro)")

# Barra lateral para tu API Key
api_key = st.sidebar.text_input("Introduce tu API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Al tener cuenta Pro, usamos gemini-1.5-pro que es más inteligente
        # Eliminamos el sufijo -latest para evitar el error 404
        model = genai.GenerativeModel('gemini-1.5-pro')

        with st.form("formulario_tasacion"):
            st.subheader("Datos Obligatorios *")
            modelo = st.text_input("Marca y Modelo *")
            horas = st.number_input("Horas *", min_value=0)
            estado = st.text_area("Estado y Averías *")
            
            # Una sola foto para máxima estabilidad
            foto = st.file_uploader("Sube la foto principal *", type=['jpg', 'jpeg', 'png'])
            
            if foto:
                st.image(Image.open(foto), width=300)

            submit = st.form_submit_button("🚀 TASAR CON GEMINI PRO")

        if submit:
            if not (modelo and estado and foto):
                st.error("⚠️ Faltan datos o la foto.")
            else:
                with st.spinner("Gemini Pro está analizando..."):
                    img = Image.open(foto)
                    # Tu regla de los 10.000€ y 100h
                    prompt = f"Tasador experto. Analiza: {modelo}, {horas}h, {estado}. REGLA: Si hay averías, resta 10.000€ y 100h de taller. Precio mercado 2026."
                    response = model.generate_content([prompt, img])
                    st.success("✅ Tasación Completada")
                    st.write(response.text)

    except Exception as e:
        st.error(f"Error de conexión: {e}")
else:
    st.warning("Escribe tu clave en la barra lateral.")
