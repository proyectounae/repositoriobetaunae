import streamlit as st
import requests

# ---------------------------------------------------------
# Asistente de Escritura Académica - IAVQ
# Conecta con la pasarela RAG/LLM de CEDIA (piloto "escritura_academica")
# ---------------------------------------------------------

CEDIA_BASE_URL = "https://ai.hpc.cedia.edu.ec"
COLLECTION = "escritura_academica"

st.set_page_config(page_title="Asistente Escritura Académica - IAVQ", page_icon="📚")

st.title("📚 Asistente de Escritura Académica")
st.caption("Instituto Superior Tecnológico Universitario de Artes Visuales — IAVQ")
st.caption("Powered by CEDIA — HPC AI Gateway (piloto RAG)")

# La API key se lee de los "Secrets" de Streamlit Cloud, nunca queda escrita en el código.
try:
    API_KEY = st.secrets["CEDIA_API_KEY"]
except Exception:
    API_KEY = None

if not API_KEY:
    st.error(
        "No se encontró la API key. Configúrela en Settings → Secrets de Streamlit "
        "Cloud como: CEDIA_API_KEY = \"su_clave_aqui\""
    )
    st.stop()

if "historial" not in st.session_state:
    st.session_state.historial = []

pregunta = st.text_area("Escriba su pregunta o consulta:", height=100)

col1, col2 = st.columns([1, 5])
with col1:
    enviar = st.button("Consultar", type="primary")

if enviar and pregunta.strip():
    with st.spinner("Consultando la base de conocimiento..."):
        try:
            resp = requests.post(
                f"{CEDIA_BASE_URL}/rag",
                headers={"x-api-key": API_KEY, "Content-Type": "application/json"},
                json={
                    "question": pregunta,
                    "collection": COLLECTION,
                    "use_rerank": True,
                },
                timeout=60,
            )
            if resp.status_code == 200:
                data = resp.json()
                respuesta = data.get("answer", "(sin respuesta)")
                st.session_state.historial.insert(0, (pregunta, respuesta))
            else:
                st.error(f"Error {resp.status_code}: {resp.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"No se pudo conectar con el servicio: {e}")

st.divider()

for q, a in st.session_state.historial:
    st.markdown(f"**Pregunta:** {q}")
    st.markdown(f"**Respuesta:** {a}")
    st.divider()
