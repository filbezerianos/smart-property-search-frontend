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
    st.page_link('https://tally.so/r/3NJ5gO', label='Get in Touch', icon=':material/alternate_email:')

    st.divider()
    st.write(f"© {datetime.now().year} Orbiont")

st.markdown("# FAQs")
st.write("")

st.markdown("##### What is the Home Match AI application?")
st.write("Home Match AI is an advanced application that uses a fine-tuned AI model to detect specific property features, like natural light in rooms, the presence of carpets etc. This allows users to search and rank properties based on detailed characteristics, going beyond the usual basic search criteria.")
st.write("")

st.markdown("##### How does the application work?")
st.write("Our application analyses each property image based on various criteria, assigning ratings to specific features. These ratings are combined to generate an overall score for each property. When you search with specific preferences, properties are filtered and ranked according to these scores ensuring the results align with what you are looking for.")
st.write("")

st.markdown("##### How is this different from other property platforms?")
st.write("Unlike existing platforms, our application stands out by using property photos to identify specific features, such as natural light, high ceilings etc. This approach allows you to search beyond the basic parameters like rent and location, providing a more detailed and personalised property search experience.")
st.write("")

st.markdown("##### Which markets can I search?")
st.write("Currently, our database includes rental properties in UK, London only. We are working on expanding coverage to include more areas and regions in the future.")
st.write("")

st.markdown("##### Why can't I search for properties with more than 3 bedrooms?")
st.write("Our data is limited to properties with up to 3 bedrooms. We are continually expanding our dataset, and properties with more bedrooms will be available in the future.")
st.write("")

st.markdown("##### Can I search for properties for sale?")
st.write("At the moment, our data is limited to rental properties. We are continually expanding our dataset, and properties for sale will be available in the future.")
st.write("")

st.markdown("##### What personal preferences can I search for?")
st.write("Currently, our model processes preferences related to Natural Light, Windows, Ceiling, Carpets, Wide Lenses, and Photo Editing. We're working on expanding our AI capabilities to include a broader range of characteristics in the future.")
st.write("")

st.markdown("##### What data sources do you use?")
st.write("Right now, we source our data from Zoopla.co.uk and Rightmove.co.uk. We plan to integrate additional data sources in the near future to provide more results.")
st.write("")

st.markdown("##### How current are the search results?")
st.write("You can find the date of the last data update at the bottom of the search page. While the data isn't in real-time, we strive to keep it as up-to-date as possible.")
st.write("")

st.markdown("##### How can I find more information about a property I'm interested in?")
st.write("After viewing the search results, you can click the link in the Details column to be directed to the relevant property website for more information.")
st.write("")

st.markdown("##### Why am I not being redirected to the relevant property page when clicking the link in the Details column?")
st.write("This issue likely occurs because the property is no longer listed on the property website (e.g. Zoopla). Since the data isn't updated in real time, the property may have been removed or become unavailable after the last update.")
st.write("")

st.markdown("##### What kind of updates will I receive if I subscribe?")
st.markdown("By subscribing, you will be notified about the official launch of the application. Additionally, you may receive an invitation to access pre-release versions if you are interested in trying out the application early. You can subscribe by dropping us a message [here](https://tally.so/r/3NJ5gO)")
st.write("")
