#pip install streamlit
#streamlit run launch_app.py
# from src.Determine_Fame import biography_artsy
import joblib

import streamlit as st
import numpy as np
forest = joblib.load("ArtNum.joblib")
# image_regressor = joblib.load("image_regressor.joblib")

st.title("Artist prediction model Itay Tal")

def load_input():
    uploaded_file = st.file_uploader(label='Pick an image to test')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)

    artist = st.text_input("artist? ") #1
    year = st.text_input("year? ") #2
    art_nouveau = st.text_input("Art Nouveau? ") #7
    abstract_express = st.text_input("Abstract Expressionism? ") #4
    expressionisim = st.text_input("Expressionism? ") #12
    feminist_art = st.text_input("Feminist Art? ") #13
    Abstract = st.text_input("Abstract? ") #3
    conceptual = st.text_input("Conceptual? ") #9
    impressionism = st.text_input("Impressionism? ") #15
    baroque = st.text_input("baroque? ") #8
    geometric_abstraction = st.text_input("Geometric Abstraction? ") #14
    cubism = st.text_input("cubism? ") #10
    art_brut = st.text_input("Art Brut? ") #5
    environmental_art = st.text_input("Environmental Art? ") #11
    art_deco = st.text_input("Art Deco? ") #6

    # if artist is not None:
    #     print("getting artist")
    #     fame = len(biography_artsy(artist).split())
    submit = st.button('Submit')

    st.write(submit)

    if submit:
        input_data = [artist,year,Abstract,
                      abstract_express,art_brut,art_deco,
                      art_nouveau,baroque,conceptual,cubism,
                      environmental_art,expressionisim,
                      feminist_art,geometric_abstraction,impressionism]
        print(forest.predict([input_data]))



def main():
    st.title('Image upload demo')
    load_input()


if __name__ == '__main__':
    main()