import google.generativeai as genai
import typing_extensions as typing

# Configuración de la API
genai.configure(api_key="TU_API_KEY")

# Definimos la estructura obligatoria de la tasación
class TasacionMaquinaria(typing.TypedDict):
    marca_modelo: str
    estado_general: str  # (Excelente, Bueno, Regular, Desgastado)
    valor_estimado_euros: int
    justificacion_precio: str
    reparaciones_detectadas: list[str]
    campos_completos: bool # Para verificar obligatoriedad

# Inicializamos el modelo con la configuración de salida
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # O gemini-2.0-flash si ya está disponible en tu región
    generation_config={
        "response_mime_type": "application/json",
        "response_schema": TasacionMaquinaria
    }
)

# Definimos la lógica de tasación
def tasar_maquinaria(ruta_imagen, horas_reparacion, coste_reparacion):
    # Cargamos la imagen (previamente guardada para la vista previa)
    foto_tractor = genai.upload_file(path=ruta_imagen)
    
    prompt = f"""
    Analiza la imagen de este tractor y tásalo profesionalmente. 
    Datos conocidos: 
    - Se le han invertido {horas_reparacion} horas de trabajo técnico.
    - El coste de las piezas y reparaciones recientes asciende a {coste_reparacion} euros.
    
    INSTRUCCIONES:
    1. Identifica marca y modelo si es visible.
    2. Evalúa el estado exterior a partir de la foto.
    3. Suma el valor de la inversión de {coste_reparacion}€ al valor base de mercado.
    4. Todos los campos del JSON son OBLIGATORIOS.
    """
    
    response = model.generate_content([prompt, foto_tractor])
    return response.text

# Ejemplo de uso
# resultado = tasar_maquinaria("tractor_front.jpg", 100, 10000)
# print(resultado)
