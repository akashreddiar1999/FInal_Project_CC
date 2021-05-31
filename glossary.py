import streamlit as st
import pandas as pd
import numpy as np


def app():
    st.header("Glossary")

    st.subheader("Don't know what that finance term means? Find it here!")

    glos_df = pd.read_csv("glos_df.csv")
    term = st.selectbox("Type in what you're searching for:", glos_df['term'])
    st.subheader(term)
    info = glos_df.loc[(glos_df["term"] == term), 'info'].iloc[0]
    #info = st.text(glos_df['info'])
    st.write(info)
