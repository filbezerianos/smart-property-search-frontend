import streamlit as st
from datetime import datetime


# Start with the page config
st.set_page_config(
    page_title="Smart Property Search",
    layout="wide",
    page_icon = ":material/house:",
    menu_items={
        'About': "Created by Orbiont Ltd."
    },
     initial_sidebar_state = 'expanded'   
)


with st.sidebar:
    st.page_link('main.py', label='Home', icon=':material/house:')
    st.page_link('pages/faq.py', label='FAQs', icon=':material/help:', disabled=True)
    st.page_link('pages/under_the_hood.py', label='Under the Hood', icon=':material/smart_toy:')
    st.page_link('https://tally.so/r/mDDDEZ', label='Get in Touch', icon=':material/alternate_email:')

    st.divider()
    st.write(f"© {datetime.now().year} Orbiont")


st.markdown("## FAQs")
st.divider()


st.markdown("##### Which UK regions can I search?")
st.write("Currently, our database includes properties in London only. We are working on expanding coverage to include more areas and regions soon.")
st.write("")

st.markdown("##### Why can't I search for properties with more than 3 bedrooms?")
st.write("Our data is limited to properties with up to 3 bedrooms. We are continually expanding our dataset, and properties with more bedrooms will be available in the future.")
st.write("")

st.markdown("##### What personal preferences can I search for?")
st.write("Currently, our model processes preferences related to Natural Light, Windows, Ceiling, Carpets, Wide Lenses, and Photo Editing. We're working on expanding our AI capabilities to include a broader range of characteristics in the future.")
st.write("")

st.markdown("##### What data sources do you use?")
st.write("Right now, we source our data from Zoopla.co.uk. We plan to integrate additional data sources in the near future to provide more results.")
st.write("")

st.markdown("##### How current are the search results?")
st.write("You can find the date of the last data update at the bottom of the search page. While the data isn't in real-time, we strive to keep it as up-to-date as possible.")
st.write("")

st.markdown("##### How can I find more information about a property I'm interested in?")
st.write("After viewing the search results, you can click the link in the Details column to be directed to the relevant property website for more information.")
st.write("")



