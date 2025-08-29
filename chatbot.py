import streamlit as st
import requests

API_KEY = "sk-53751d5c6f344a5dbc0571de9f51313e"
API_URL = "https://api.deepseek.com/v1/chat/completions"

def enviar_mensaje(mensaje, modelo="deepseek-chat"):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": modelo,
        "messages": [
		{"role": "user", "content": "Habla como Goku de Dragon Ball: usa un tono entusiasta, inocente y amigable, con expresiones como '¡Kamehameha!', '¡Que emocionante!' o '¡Vamos a entrenar mas duro!' responde de forma positiva y con energia, como un guerrero Saiyajin."},
		{"role": "user", "content":mensaje}
		]
	}
    
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🤖 Chatbot con DeepSeek")


# Historial

for message in st.session_state.messages:
	with st.chat_message(message["role"]):
		st.markdown(message["content"])

#Entrada del usuario
if prompt := st.chat_input("Escribe tu mensaje: "):

	st.session_state.messages.append({"role":"user", "content": prompt})

	
	with st.chat_message("user"):
		st.markdown(prompt)
	#Generar respuesta
	if prompt.lower() == "salir":
		respuesta = "¡Hasta luego!"
	else:
		respuesta = enviar_mensaje(prompt)
	# Mostrar y guardar respuesta
	with st.chat_message("assistant"):
		st.markdown(respuesta)
	st.session_state.messages.append({"role": "assistant", "content" : respuesta })

