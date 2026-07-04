import streamlit as st


def show_success(message):
    st.success(message)


def show_error(message):
    st.error(message)


def character_count(text):
    return len(text)    