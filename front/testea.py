import streamlit as st
import requests

# Configuración de la página
st.set_page_config(
    page_title="Chat Interface",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Contenedor para los mensajes de chat
chat_history = st.container()

# Lista para almacenar el historial de mensajes
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Mostrar el historial de mensajes
with chat_history:
    for i, message in enumerate(st.session_state['messages']):
        if i % 2 == 0:  # Mensaje del usuario
            st.markdown(f"<div style='text-align: left; background-color: #f1f1f1; padding: 10px; border-radius: 10px; margin: 10px 0;'>{message}</div>", unsafe_allow_html=True)
        else:  # Respuesta del servidor
            st.markdown(f"<div style='text-align: right; background-color: #d1ffd6; padding: 10px; border-radius: 10px; margin: 10px 0;'>{message}</div>", unsafe_allow_html=True)

# Contenedor para el input de texto y el botón
input_container = st.container()

# Asegúrate de limpiar el campo de entrada antes de inicializar el widget
if st.session_state.get('clear_text_input', False):
    st.session_state['user_input'] = ""
    st.session_state['clear_text_input'] = False

# Input text y botón en la parte inferior centrada
with input_container:
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        user_input = st.text_input("", placeholder="Escribe tu mensaje aquí...", key="user_input", label_visibility="collapsed")
    
    with col3:
        if st.button("Enviar"):
            # Agrega el mensaje del usuario al historial
            st.session_state['messages'].append(user_input)
            
            # Muestra un spinner mientras se espera la respuesta del servidor
            with st.spinner('Enviando tu mensaje y esperando respuesta...'):
                try:
                    # Envía la solicitud al servidor
                    response = requests.get("http://localhost:8000/llm-response", params={"input": user_input})
                    
                    # if response.status_code == 200:
                    #     # Asegúrate de que la respuesta es JSON y contiene el campo 'reply'
                    #     json_response = response.json()
                    #     #server_reply = json_response.get('reply', 'Error: No se recibió una respuesta válida.')
                    # else:
                    #     server_reply = f"Error: Respuesta inesperada del servidor ({response.status_code}): {response.text}"
                    
                except requests.exceptions.RequestException as e:
                    raise f"Error al conectar con el servidor: {e}"
            
            # Limpia el campo de entrada
            st.session_state['clear_text_input'] = True
            print("Front Respuesta:  ",response)
            # Agrega la respuesta del servidor al historial
            #st.session_state['messages'].append(server_reply)