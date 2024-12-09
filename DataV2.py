import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import joblib

df = pd.read_csv('SDGs_Zero_Hunger.csv')

with st.sidebar:
    selected = option_menu(
        'Data Zero Hunger',
        ['SDG Zero Hunger Score', 'Kategori Zero Hunger Negara', 'Prediksi Score'],
        default_index=0
    )

if selected == 'SDG Zero Hunger Score':
    st.title("Zero Hunger Score")
    st.write("Masukkan nama negara untuk melihat skor:")
    NamaNegara = st.text_input("Nama negara", key="score_input") 

    if NamaNegara:
        data = df[df['NamaNegara'].str.contains(NamaNegara, case=False, na=False)]
        if not data.empty:
            st.dataframe(data)
        else:
            st.warning(f"Data untuk negara **{NamaNegara}** tidak ditemukan.")

if selected == 'Kategori Zero Hunger Negara':
    st.title("Kategori Zero Hunger")
    st.write("Masukkan nama negara untuk mengetahui kategorinya:")
    Kategori = st.text_input("Nama negara", key="kategori_input") 

    if Kategori:
        data1 = df[df['NamaNegara'].str.contains(Kategori, case=False, na=False)]
        if not data1.empty:
            kategori1 = data1.iloc[0]['Kategori']
            st.success(f"Negara **{Kategori}** ini dalam kategori: **{kategori1}**")
        else:
            st.warning(f"Data untuk negara **{Kategori}** tidak ditemukan.")

model = joblib.load('random_forest_model.pkl')
label_encoder = joblib.load('coder.pkl')

if selected == 'Prediksi Score':
    st.title("Prediksi Score Manual")
    st.write("Masukan Value Score Random:")
    score_2021 = st.number_input("Skor Tahun 2021", min_value=0.0, max_value=100.0, step=0.1)
    score_2022 = st.number_input("Skor Tahun 2022", min_value=0.0, max_value=100.0, step=0.1)
    score_2023 = st.number_input("Skor Tahun 2023", min_value=0.0, max_value=100.0, step=0.1)
    goals_score = st.number_input("Zero Hunger Goals Score", min_value=0.0, max_value=100.0, step=0.1)
    if st.button("Prediksi Kategori"):
        input_data = pd.DataFrame({
            '2021': [score_2021],
            '2022': [score_2022],
            '2023': [score_2023],
            'ZeroHungerGoalsScore': [goals_score]
        })
        prediction = model.predict(input_data)
        predicted_category = label_encoder.inverse_transform(prediction)[0]
        st.success(f"Prediksi Kategori: {predicted_category}")