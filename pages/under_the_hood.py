import streamlit as st
from datetime import datetime

with st.sidebar:
    st.page_link('main.py', label='Home', icon=':material/house:')
    st.page_link('pages/faq.py', label='FAQs', icon=':material/help:')
    st.page_link('pages/under_the_hood.py', label='Under the Hood', icon=':material/smart_toy:')

    st.divider()
    st.write(f"© {datetime.now().year} Orbiont")