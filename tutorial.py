# https://github.com/streamlit/streamlit/issues/4195#issuecomment-998909519
# Simpler, effective method to clear value of text_input #4195
import streamlit as st

input = st.text_input("text", key="text")


def clear_text():
    st.session_state["text"] = ""


st.button("clear text input", on_click=clear_text)
st.write(input)