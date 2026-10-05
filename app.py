import streamlit as st
from google import genai

st.set_page_config(page_title="Corrector Logístico", page_icon="🚛", layout="centered")

st.title("🚛 Asistente de Correos - Logística")
st.write("Ajusta ortografía, gramática y tono corporativo sin alterar patentes, kilos ni horarios.")

# Inicialización segura diseñada para Streamlit
try:
    cliente = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
except KeyError:
    st.error("⚠️ Falla de configuración: Añade GEMINI_API_KEY en los secretos del servidor.")
    st.stop()

texto_original = st.text_area("Borrador rápido:", height=150, placeholder="Ej: nesesito mandar 3 camiones patente AB12-34 a las 15:00 hrs...")

if st.button("Aplicar Formato Profesional"):
    if texto_original.strip():
        instruccion = f"""
        Eres un asistente de redacción para una profesional de logística y transporte. Tu objetivo es corregir la ortografía y gramática de correos electrónicos.
        
        Reglas estrictas:
        1. Tono: Formal pero ágil, directo y empático. Sin introducciones floridas.
        2. Integridad de datos: NO modifiques, redondees ni elimines ninguna cifra, patente, horario, volumen, peso o métrica mencionada.
        3. Formato: Entrega únicamente el texto final corregido, listo para copiar y pegar. No incluyas frases de cortesía en tu respuesta.
        
        Texto a corregir: 
        {texto_original}
        """

        with st.spinner("Estandarizando texto y protegiendo métricas..."):
            try:
                # Se restaura el modelo original solicitado
                respuesta = cliente.models.generate_content(
                    model='gemini-3.5-flash-lite',
                    contents=instruccion,
                )

                st.success("✅ Listo para copiar y enviar:")
                st.text_area("Resultado", value=respuesta.text.strip(), height=200, label_visibility="collapsed")

            except Exception as e:
                st.error(f"Falla de conexión con el modelo: {e}")
    else:
        st.warning("Por favor, ingresa el borrador antes de procesar.")
