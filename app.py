import streamlit as st
import pandas as pd
import numpy as np
import joblib
import math
import base64
from src.pipeline.prediction_pipeline import predict, preprocess_data

# Function to read and display an image as background
def add_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
    encoded_image = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpeg;base64,{encoded_image});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Add background image
add_background('images/image.jpg')

# Streamlit user interface
st.title('Application de Prédiction')

page = st.sidebar.selectbox('Sélectionnez une page', ['Prédiction', 'About Us', 'Informations'])

if page == 'Prédiction':
    with st.sidebar.form(key='prediction_form'):
        col1, col2 = st.columns(2)
        
        with col1:
            distance = st.number_input('DISTANCE')
            region = st.text_input('REGION')
            carrier = st.text_input('CARRIER', '')
            origin = st.text_input('ORIGIN', '')
            origin_wac = st.number_input('ORIGIN_WAC')
        
        with col2:
            dest = st.text_input('DEST', '')
            dest_wac = st.number_input('DEST_WAC')
            year = st.number_input('YEAR', min_value=2010, max_value=2030, value=2024)
            month = st.number_input('MONTH', min_value=1, max_value=12, value=1)
            class_ = st.text_input('CLASS')
        
        submit_button = st.form_submit_button(label='Faire une Prédiction')

    # Display message before submission
    if not submit_button:
        st.write('### Veuillez introduire vos données')
        st.write('### pour faire votre prédiction')

    if submit_button:
        data = {
            'DISTANCE': [distance],
            'REGION': [region],
            'CARRIER': [carrier],
            'ORIGIN': [origin],
            'ORIGIN_WAC': [origin_wac],
            'DEST': [dest],
            'DEST_WAC': [dest_wac],
            'YEAR': [year],
            'MONTH': [month],
            'CLASS': [class_]
        }

        model_path = "models/best_model.pkl"
        label_encoder_path = "models/label_encoder.pkl"
        log_transformer_path = "models/log_transformer.pkl"

        model = joblib.load(model_path)
        
        df_new = pd.DataFrame(data)

        # Faire des prédictions
        predictions = predict(df_new, model, label_encoder_path, log_transformer_path)
        prediction_original = np.exp(predictions)

        passengers = prediction_original[0][0]
        freight = prediction_original[0][1]
        mail = prediction_original[0][2]

        st.markdown(f"<h3 style='text-align: center;'>Le nombre de passagers prévu est : {math.floor(passengers)}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>La quantité de fret prévue : {math.floor(freight)}</h3>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>La quantité de courrier prévue est : {math.floor(mail)}</h3>", unsafe_allow_html=True)

elif page == 'About Us':
    st.header('À Propos de Nous')
    st.write("Cette Application est conçue par : ")
    st.write("M. Mourad HAMZAOUI et M. Mehdi Belamine")  
    st.write('''Nous sommes une équipe dédiée à la création d'applications de machine learning avancées. Notre objectif est d'apporter des solutions innovantes aux problèmes du monde réel en utilisant des techniques de pointe en science des données.''')

elif page == 'Informations':
    st.header('Informations')
    st.write('''Cette application utilise un modèle de machine learning pour prédire le nombre de passagers, et les quantités de fret et de courrier basées sur des données d'entrée. Les prédictions sont générées en utilisant un modèle enregistré en pickle. Nous utilisons également Streamlit pour créer une interface utilisateur interactive.''')
