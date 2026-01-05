import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="Test Visión Correcto", layout="centered")
st.title("👁️ Probando Visión con Gemini 1.5")

# Barra lateral para la llave
api_key = st.sidebar.text_input("Introduce tu Gemini API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Usamos el modelo correcto y actualizado
        model = genai.GenerativeModel('gemini-1.5-flash')

        uploaded_file = st.file_uploader("Sube una foto para probar", type=["jpg", "jpeg", "png"])

        if uploaded_file:
            image = Image.open(uploaded_file)
            # Mostramos la foto pequeña (regla de usuario)
            st.image(image, caption="Foto cargada", width=300)

            if st.button("¿Qué ves en la foto?"):
                with st.spinner("La IA está mirando..."):
                    # Enviamos la imagen y el texto juntos
                    response = model.generate_content(["Describe brevemente lo que ves.", image])
                    st.success("Respuesta de la IA:")
                    st.write(response.text)
                    
    except Exception as e:
        st.error(f"Error: {e}")
        st.info("Si sale error 404, recuerda darle a 'HABILITAR' en Google Cloud.")
else:
    st.warning("Introduce la API Key a la izquierda.")
