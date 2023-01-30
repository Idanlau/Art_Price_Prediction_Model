#pip install streamlit
#streamlit run launch_app.py
from scripts.Determine_Fame import biography_artsy

import streamlit as st

st.title("Artist prediction model Itay Tal")
def load_input():
    uploaded_file = st.file_uploader(label='Pick an image to test')
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        st.image(image_data)

    period = st.text_input("Period? ")
    movement = st.text_input("Movement? ")
    description = st.text_input("description? ")
    artist = st.text_input("artist? ")

    # if period and movement and description and artist:
    #     print("got it")

    if artist is not None:
        print("getting artist")
        fame = len(biography_artsy(artist))

def main():
    st.title('Image upload demo')
    load_input()


if __name__ == '__main__':
    main()