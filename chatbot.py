import streamlit as st
import requests
from gtts import gTTS
import os
import tempfile
import base64

# 🔑 Configuración API
API_KEY = "sk-53751d5c6f344a5dbc0571de9f51313e"
API_URL = "https://api.deepseek.com/v1/chat/completions"

# 📩 Función para enviar mensajes
def enviar_mensaje(mensaje, modelo="deepseek-chat"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": modelo,
        "messages": [
            
		{"role": "system", "content": "Responde como si fueras Goku de Dragon Ball, usando un tono entusiasta, inocente y energético, con expresiones como '¡Kamehameha!', '¡Qué emocionante!' o '¡Vamos a entrenar más duro!'. Sin embargo, también eres un profesor experto en Sistemas Digitales: explica con claridad y ejemplos sencillos qué son los sistemas digitales, sus componentes (lógica combinacional, secuencial, circuitos), y su importancia en la computación y la electrónica. Siempre mantén el estilo alegre y motivador de Goku mientras enseñas sobre Sistemas Digitales."}


            ,
            {"role": "user", "content": mensaje}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"⚠️ Error en la API: {result}"

# 🎵 Función para reproducir audio sin barra
def reproducir_audio(archivo):
    with open(archivo, "rb") as f:
        audio_bytes = f.read()
    audio_b64 = base64.b64encode(audio_bytes).decode()
    st.markdown(
        f"""
        <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True
    )

# 🧠 Manejo de historial
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Chat estilo Goku con voz")

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    respuesta = enviar_mensaje(prompt)
    st.session_state.messages.append({"role": "assistant", "content": respuesta})

    with st.chat_message("assistant"):
        st.markdown(respuesta)

        # 🔊 Generar audio invisible
        tts = gTTS(respuesta, lang="es")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            reproducir_audio(tmpfile.name)  # 🎵 Sonará automáticamente sin barra
