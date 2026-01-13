import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

# Configuración de la API (Usa tu clave de siempre)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])



# --- ESTILO CSS PARA LIMPIAR INTERFAZ ---
st.markdown("""import streamlit as st
import google.generativeai as genai
from PIL import Image
import time

def main():
    # Configuración de la API
    if "GOOGLE_API_KEY" not in st.secrets:
        st.error("Falta la clave GOOGLE_API_KEY en los Secrets de Streamlit")
        return

    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

    st.title("🚜 Peritaje Profesional V2.0")

    # --- DATOS OBLIGATORIOS ---
    with st.expander("📝 Datos de la Máquina", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            marca = st.text_input("Marca*")
        with col2:
            modelo = st.text_input("Modelo*")
        with col3:
            anio = st.text_input("Año*")
        
        observaciones = st.text_area("Incidencias y Extras (Pala, averías, pintura...)")

    # --- FOTOS ---
    st.subheader("📸 Fotos (5 a 10)")
    fotos_subidas = st.file_uploader("Subir imágenes", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

    comentarios = []
    if fotos_subidas:
        for i, foto in enumerate(fotos_subidas[:10]):
            c1, c2 = st.columns([1, 3])
            c1.image(foto, width=100)
            txt = c2.text_area(f"Nota foto {i+1} (máx 4 líneas)", key=f"n_{i}", height=70)
            comentarios.append(txt)

    # --- BOTÓN Y LÓGICA ---
    if st.button("🚀 REALIZAR TASACIÓN"):
        if not (marca and modelo and anio):
            st.warning("Marca, Modelo y Año son obligatorios.")
        elif len(fotos_subidas) < 5:
            st.warning("Sube al menos 5 fotos.")
        else:
            bar = st.progress(0)
            msg = st.empty()
            for p in range(100):
                time.sleep(0.02)
                bar.progress(p + 1)
                if p == 20: msg.text("Analizando fotos...")
                if p == 50: msg.text("Buscando en mercado europeo...")
                if p == 80: msg.text("Calculando precio de compra...")

            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                texto_fotos = "\n".join([f"Foto {i+1}: {c}" for i, c in enumerate(comentarios)])
                
                prompt = f"""Tasador profesional. Máquina: {marca} {modelo} ({anio}). 
                Observaciones: {observaciones}. Notas fotos: {texto_fotos}.
                TAREA: 1. Extrae número serie. 2. Da PRECIO DE COMPRA (valor de captación para concesionario, tirando a la baja pero realista).
                Se directo y breve."""

                lista = [prompt]
                for f in fotos_subidas:
                    lista.append(Image.open(f))

                res = model.generate_content(lista)
                st.success("Peritaje Finalizado")
                st.write(res.text)
            except Exception as e:
                st.error(f"Error: {e}")

# Esto es lo que evita el parpadeo infinito
if __name__ == "__main__":
    main()
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {max-width: 800px; margin: 0 auto;}
    </style>
    """, unsafe_allow_index=True)

st.title("🚜 Peritaje Profesional V2.0")
st.info("Complete los campos obligatorios y suba las fotos con sus notas.")

# --- FORMULARIO DE DATOS ---
with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        marca = st.text_input("Marca*", placeholder="Ej: John Deere")
    with col2:
        modelo = st.text_input("Modelo*", placeholder="Ej: 6155R")
    with col3:
        anio = st.text_input("Año*", placeholder="Ej: 2018")

    observaciones = st.text_area(
        "Incidencias y Extras", 
        placeholder="Pala cargadora, cambio roto, pintura saltada en capó, etc.",
        height=100
    )

st.divider()

# --- SUBIDA DE FOTOS Y COMENTARIOS ---
st.subheader("Fotografías (Mínimo 5, Máximo 10)")
fotos_subidas = st.file_uploader("Arrastre o seleccione las fotos", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)

comentarios = {}

if fotos_subidas:
    if len(fotos_subidas) > 10:
        st.error("Máximo 10 fotos permitidas.")
    else:
        for i, foto in enumerate(fotos_subidas):
            col_img, col_txt = st.columns([1, 2])
            with col_img:
                st.image(foto, use_column_width=True)
            with col_txt:
                comentarios[i] = st.text_area(
                    f"Nota para foto {i+1}", 
                    placeholder="Máximo 4 líneas explicativas...",
                    key=f"coment_{i}",
                    height=80
                )

st.divider()

# --- LÓGICA DE TASACIÓN ---
if st.button("🚀 REALIZAR TASACIÓN PROFESIONAL"):
    # Validación de campos mandatorios
    if not marca or not modelo or not anio:
        st.warning("⚠️ Marca, Modelo y Año son campos obligatorios.")
    elif len(fotos_subidas) < 5:
        st.warning("⚠️ Se requieren al menos 5 fotografías para un peritaje preciso.")
    else:
        # Barra de progreso dinámica
        progreso = st.progress(0)
        status_text = st.empty()
        
        for p in range(100):
            time.sleep(0.03) # Simulación de carga para que no sea aburrido
            progreso.progress(p + 1)
            if p < 30: status_text.text("🔍 Analizando imágenes y placas...")
            elif p < 60: status_text.text("📊 Comparando mercado europeo (Mascus/Agriaffaires)...")
            else: status_text.text("⚖️ Calculando valor de compra profesional...")

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # Construcción del Prompt con el ajuste "Precio de Compra"
            prompt_vendedor = f"""
            Eres un tasador experto de maquinaria agrícola para un concesionario.
            
            DATOS TÉCNICOS:
            - Marca: {marca}
            - Modelo: {modelo}
            - Año: {anio}
            - Observaciones del perito: {observaciones}
            
            NOTAS DE LAS FOTOS:
            {list(comentarios.values())}
            
            TAREA:
            1. Analiza las fotos buscando desgastes reales (ruedas, fugas, cabina).
            2. Extrae el Número de Serie si ves la placa.
            3. Proporciona un PRECIO DE COMPRA PROFESIONAL (lo que el concesionario debe pagar para captar la máquina). 
               El precio debe ser competitivo pero tirando a la BAJA para asegurar margen de reventa, sin ser ridículo.
            4. Conclusión breve de por qué ese precio (basado en mercado europeo).
            
            ESTILO: Muy directo, profesional, sin rellenos.
            """
            
            lista_contenido = [prompt_vendedor]
            for f in fotos_subidas:
                img = Image.open(f)
                lista_contenido.append(img)
            
            response = model.generate_content(lista_contenido)
            
            st.success("✅ Tasación Completada")
            st.subheader("Resultado del Peritaje")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"Error en la IA: {e}")
