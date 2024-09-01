import streamlit as st
from datetime import datetime

# Start with the page config
st.set_page_config(
    page_title="Proper-ty Search",
    layout="wide",
    page_icon = ":material/house:",
    menu_items={
        'About': "Created by Orbiont Ltd."
    },
     initial_sidebar_state = 'collapsed'   
)


with st.sidebar:
    st.page_link('main.py', label='Home', icon=':material/house:')
    st.page_link('pages/faq.py', label='FAQs', icon=':material/help:')
    st.page_link('pages/under_the_hood.py', label='Under the Hood', icon=':material/smart_toy:')

    st.divider()
    st.write(f"© {datetime.now().year} Orbiont")


st.markdown("## Under the Hood")
st.divider()

st.write("Our application gathers information from property websites like Zoopla.co.uk, including the images uploaded for each property.")
st.write("These images are then analysed by our AI model, which is fine tuned to detect specific features such as natural light in rooms, presence of carpets, and more. Each image is rated across different criteria, and these ratings are combined to create an overall score for each property.")
st.write("When you search with specific preferences, the results are filtered and ranked based on these scores to match your preferences as closely as possible.")