import streamlit as st
import requests

st.title('Subir Documento PDF')

# Ingresar el nombre de la colección
name_collection = st.text_input("Nombre de la colección")

# Mostrar un área de drag and drop para subir archivos
uploaded_file = st.file_uploader("Arrastra y suelta un archivo PDF aquí", type="pdf")

# Botón para subir el archivo
if st.button('Subir Documento'):
    if uploaded_file is not None and name_collection:
        files = {'file': (uploaded_file.name, uploaded_file, 'application/pdf')}
        data = {'name_collection': name_collection}  # Corregir aquí
        
        response = requests.post('http://localhost:8000/add_document', files=files, data=data)

        if response.status_code == 200:
            st.success('Documento subido con éxito.')
        else:
            st.error(f'Error al subir el documento: {response.text}')
    else:
        st.error('Por favor, asegúrate de haber proporcionado un nombre de colección y haber subido un archivo PDF.')
