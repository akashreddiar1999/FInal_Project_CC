import streamlit as st
import hashlib
from pymongo import MongoClient
import pymongo

import glossary
import home
import myPortfolio
import portfolio
import prediction


def app():
    client = MongoClient(
        'mongodb+srv://dbShreya:vuh42u4cNDnSlmFm@cluster0.gttk9.mongodb.net/Cluster0?retryWrites=true&w=majority')

    db = client.userData

    people = db.people

    def make_hashes(password):
        return hashlib.sha256(str.encode(password)).hexdigest()

    def check_hashes(password, hashed_text):
        if make_hashes(password) == hashed_text:
            return hashed_text
        return False

    def add_userdata(username, password, email):
        people.create_index([('Email', pymongo.DESCENDING)], unique=True)
        people.insert_one({'Username': username, 'Password': password, 'Email': email})

    def login_user(username, password, email):
        myquery = {"Username": username, "Password": password, 'Email': email}
        data = people.find_one(myquery)
        return data


    menu = ["Login", "SignUp"]
    #a, b = st.beta_columns(2)

    choice = st.radio("Login or Create a New Account", menu)

    if choice == "Home":
        st.subheader("Home")
    elif choice == "Login":
        st.subheader("Login Section")

        placeholder1 = st.empty()
        placeholder2 = st.empty()
        placeholder3 = st.empty()

        #email = st.text_input("Email")
        email = placeholder1.text_input("Email")
        username = placeholder2.text_input("Username")
        password = placeholder3.text_input("Password", type='password')

        click_clear = st.button('Clear', key=1)
        if click_clear:
            email = placeholder1.text_input("Email", value='', key=1)
            username = placeholder2.text_input("Username",  value='', key=1)
            password = placeholder3.text_input("Password", value='', key=1)

        if st.checkbox("Login"):
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd), email)
            if result:
                st.success("Logged in as {}".format(username))
                st.subheader("Great! Now you can access the entire site.")

                SecuredPages = {"Home": home, "My Portfolio": myPortfolio, "Analysis": portfolio,
                                "Prediction": prediction, "Glossary": glossary}

                selection = st.sidebar.radio("Menu", list(SecuredPages.keys()))
                sec_page = SecuredPages[selection]
                sec_page.app()
            else:
                st.warning("Incorrect Username/Password")

    elif choice == "SignUp":
        st.subheader("Create New Account")

        placeholder1 = st.empty()
        placeholder2 = st.empty()
        placeholder3 = st.empty()

        # email = st.text_input("Email")
        email = placeholder1.text_input("Email")
        new_user = placeholder2.text_input("Username")
        new_password = placeholder3.text_input("Password", type='password')

        click_clear = st.button('Clear', key=1)
        if click_clear:
            email = placeholder1.text_input("Email", value='', key=1)
            new_user = placeholder2.text_input("Username", value='', key=1)
            new_password = placeholder3.text_input("Password", value='', key=1)

        #email = st.text_input("Email")
        #new_user = st.text_input("Username")
        #new_password = st.text_input("Password", type='password')

        try:
            if st.checkbox("Signup"):
                add_userdata(new_user, make_hashes(new_password), email)
                st.success("You have successfully created a valid Account")
                st.info("Go to Login menu to login")

        except pymongo.errors.DuplicateKeyError:
            st.warning("This email-id is already in use. Create another one.")



