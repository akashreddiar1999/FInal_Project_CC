import streamlit as st
from PIL import Image


def app():
    st.title("Welcome to StockPro!!")

    st.subheader("Know all about the stocks that you're interested in, "
                 "get a personalised portfolio and also predict the market price of your favourite stocks!!")

    st.write("   ")
    image = Image.open("ccprojimg1.jpg")
    st.image(image, use_column_width=True)
    st.text("   ")

    st.subheader("And much more! Sign-in to access all the features!")


