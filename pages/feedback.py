import streamlit as st

with st.sidebar:

    st.page_link('main.py', label='Property Search', icon=':material/search:')
    #st.page_link('pages/about.py', label='The Story', icon=':material/library_books:')
    st.page_link('pages/help.py', label='Help Me', icon=':material/help:')
    st.page_link('pages/feedback.py', label='Leave Feedback', icon=':material/feedback:')