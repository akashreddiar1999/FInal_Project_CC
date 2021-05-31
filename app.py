import streamlit as st
import glossary
import portfolio
import Login
import home
from PIL import Image
from streamlit import caching

caching.clear_cache()


@st.cache(allow_output_mutation=True)
def get_state():
    return []


state = get_state()
state.append(len(state))

try:
    # Pages = {"Login": Login, "My Portfolio": myPortfolio, "Stock": stock, "Portfolio": portfolio, "Prediction": prediction}
    image5 = Image.open("ccprojimg7.jpg")
    st.sidebar.image(image5, use_column_width=True)

    Pages = {"Home": home, "Login": Login, "Glossary": glossary}
    # st.sidebar.title('Navigation')
    selection = st.selectbox("Menu", list(Pages.keys()))
    page = Pages[selection]
    page.app()

except:
    pass


