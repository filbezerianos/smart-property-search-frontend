import os
import streamlit as st
import pandas as pd
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


# Configure the sidebar
with st.sidebar:
    st.page_link('main.py', label='Home', icon=':material/house:')
    st.page_link('pages/faq.py', label='FAQs', icon=':material/help:')
    st.page_link('pages/under_the_hood.py', label='Under the Hood', icon=':material/smart_toy:')

    st.divider()
    st.write(f"© {datetime.now().year} Orbiont")


def main_button_click():
    st.session_state.first_search_done = True
    if "expand_state" in st.session_state:
        del st.session_state["expand_state"]


def show_no_results_error():
    st.error(":material/sentiment_dissatisfied: Sorry, no results were found. Please try again with different preferences.")


def apply_face(value):
    if value <= 0:
        return '⚪⚪⚪⚪⚪'
    elif 0 < value < 0.2:
        return '🟠⚪⚪⚪⚪'
    elif 0.2 <= value < 0.4:
        return '🟠🟠⚪⚪⚪'
    elif 0.4 <= value < 0.6:
        return '🟠🟠🟠⚪⚪'
    elif 0.6 <= value < 0.8:
        return '🟠🟠🟠🟠⚪'
    elif 0.8 < value <= 1:
        return '🟠🟠🟠🟠🟠'
    else:
        return 'None'  # In case the value is outside the expected range


# Load the csv with the data
df = pd.read_csv('data/properties.csv',  dtype={'property_id': 'str'})


# Get the creation date of the data file
data_file_creation_date = os.path.getctime('data/properties.csv')
creation_date_formatted = datetime.fromtimestamp(data_file_creation_date).strftime('%d %B %Y')


# Configure the dictionary for features ordering
features_dict = {
    "Natural Light": ["natural_light_score", False, "natural_light_smiley_face"],
    "Large Windows": ["large_windows_score", False, "large_windows_smiley_face"],
    "High Ceiling": ["high_ceiling_score", False, "high_ceiling_smiley_face"],
    "Fireplace": ["fireplace_score", False, "fireplace_smiley_face"],
    "No Carpets": ["no_carpet_score", False, "no_carpet_smiley_face"],
    "No Wide Lenses": ["wide_lenses_score", True, "wide_lenses_smiley_face"],
    "No Edited Photos": ["overprocessed_score", True, "overprocessed_smiley_face"],
}


# Show the large banner or top title depending on journey
if "first_search_done" not in st.session_state:
    #st.image("images/large_banner.png", use_column_width="always")
    pass
else:
    st.markdown("### Smart Search. Where AI meets property photos.")


# The search preferences container
with st.container(border=True):
    # The selection box to order the preferences
    order_feature_options = st.multiselect(
            "What do you care about most in a home?",
            ["Natural Light", "Large Windows", "High Ceiling", "No Carpets", "No Wide Lenses", "No Edited Photos"],
            placeholder="Pick what you care about most in a home, in the order that matters to you..."
        )
    
    column_a1, column_a2, column_a3, column_a4, column_a5, column_a6 = st.columns([0.2,0.2,0.2,0.2,0.1,0.1], vertical_alignment="bottom")
    with column_a1:
        number_of_bedrooms = st.number_input("Bedrooms", min_value=1, max_value=3, value="min", step=1, help="Number of bedrooms (for Room Rental and Studios select 1)")    
    with column_a2:
        postcode = st.text_input("Postcode", value="", max_chars=4, help="Write the first letters of the postcode")      
    with column_a3:
        min_monthly_rent = st.number_input("Min Rent", min_value=100, value=800, step=200, help="Minimum monthly rent in £")
    with column_a4:
        max_monthly_rent = st.number_input("Max Rent", min_value=200, value=1200, step=200, help="Maximum monthly rent in £")
    with column_a5:
        with st.popover("More...", help="More options", disabled=False, use_container_width=True):        
            # The radio buttons
            exclude_enough_photos_overall = st.toggle("Hide properties with insufficient photos", value=True, help="Choose this option to exclude properties with an insufficient number of photos")         
            exclude_enough_bedroom_photos = st.toggle("Hide properties with limited bedroom photos", value=True, help="Choose this option to exclude properties that lack sufficient photos of the bedrooms")   
            exclude_room_to_rent = st.toggle("Hide rental rooms", value=True, help="Choose this option to exclude rental rooms")
    with column_a6:
        update_results = st.button(":material/search: Search", type="primary", on_click=main_button_click, use_container_width=True)
        

###
# SHOW SEARCH RESULTS
###

# If the search button is clicked
if update_results:

    # Set the search preferences to ok
    search_preferences_ok = True


    ###
    # CHECKS BEFORE LOADING THE RESULTS
    ###

    if min_monthly_rent > max_monthly_rent:
        st.error(f":material/error: The minimum monthly rent (£ {min_monthly_rent}) cannot be higher that the maximum monthly rent (£ {max_monthly_rent})")
        search_preferences_ok = False


    ###
    # IF THE PREFERENCES ARE OK, LOAD THE RESULTS
    ###

    if search_preferences_ok:

        # Filter the properties based on the preferences
        filtered_df = df[(df['monthly_int'] >= min_monthly_rent) & (df['monthly_int'] <= max_monthly_rent)]
        filtered_df = filtered_df[filtered_df['address'].str.contains(str(postcode))]
        filtered_df = filtered_df[filtered_df['bed_number_smap'] == number_of_bedrooms]

        if exclude_enough_photos_overall:
            filtered_df = filtered_df[filtered_df['number_of_photos_overall_score'] == 1]
        else:
            pass

        if exclude_enough_bedroom_photos:
            filtered_df = filtered_df[filtered_df['number_of_bedroom_photos_score'] == 1]
        else:
            pass

        if exclude_room_to_rent:
            filtered_df = filtered_df[~filtered_df['title'].str.contains("Room to rent")]
        else:
            pass

        # If there are any NULL values replace with 0
        filtered_df = filtered_df.fillna(0)

        # Create a new column based on existing columns
        if order_feature_options:

            # The weight for the new columns is the number of preferences selection
            weight = len(order_feature_options)

            for ordering in order_feature_options:
                if 'preferences_alignment' in filtered_df:
                    filtered_df['preferences_alignment'] = filtered_df['preferences_alignment'] + (filtered_df[features_dict[ordering][0]] * weight)
                    weight -= 1
                else:
                    filtered_df['preferences_alignment'] = filtered_df[features_dict[ordering][0]] * weight
                    weight -= 1
            
            # Normalise the values to 1
            max_value = filtered_df['preferences_alignment'].max()
            if max_value > 1:
                filtered_df['preferences_alignment'] = filtered_df['preferences_alignment'] / max_value                  

            # Order the list based on the new column for preferences alignment
            filtered_df = filtered_df.sort_values(by='preferences_alignment', ascending=False)
            
            # Create new columns with smiley faces based on the scores
            filtered_df['natural_light_smiley_face'] = df['natural_light_score'].apply(apply_face)
            filtered_df['large_windows_smiley_face'] = df['large_windows_score'].apply(apply_face)
            filtered_df['high_ceiling_smiley_face'] = df['high_ceiling_score'].apply(apply_face)
            filtered_df['fireplace_smiley_face'] = df['fireplace_score'].apply(apply_face)
            filtered_df['no_carpet_smiley_face'] = df['no_carpet_score'].apply(apply_face)
            filtered_df['wide_lenses_smiley_face'] = df['wide_lenses_score'].apply(apply_face)
            filtered_df['overprocessed_smiley_face'] = df['overprocessed_score'].apply(apply_face)

            # Increase the counter for the searches with feature preferences
            if "number_of_feature_searches" not in st.session_state:
                st.session_state.number_of_feature_searches = 1
                with st.container(border=True):
                    st.markdown("Here's a quick guide to help you understand **how well each property matches your preferences**:")
                    st.write("🟠⚪⚪⚪⚪: Minimal | 🟠🟠⚪⚪⚪: Slight | 🟠🟠🟠⚪⚪: Moderate | 🟠🟠🟠🟠⚪: Strong | 🟠🟠🟠🟠🟠: Excellent")
            else:
                st.session_state.number_of_feature_searches += 1

        else:
            # If no photo preferences selected do nothing
            pass

        # Use the filtered results to load the table
        data_df = pd.DataFrame(filtered_df)

        # Check if there are any resutls returned after filtering
        if len(data_df) == 0:
            show_no_results_error()

        else:

            # Configure the order of the columms based on the selection of preferences
            if order_feature_options:
                column_order_config = ("title","address","monthly_int","link","agent_name")
                for ordering in order_feature_options:
                    column_order_config = column_order_config + (features_dict[ordering][2],)           
            else:
                column_order_config = ("title","address","monthly_int","link","agent_name")

            # Configure the height of the table so that we do not have a scrollbar inside the table
            height_config = 35 * len(data_df) + 38

            # Load the data in a table
            st.data_editor(
                data_df,
                column_order=column_order_config,
                column_config={
                    "title": st.column_config.TextColumn(
                        "Description",
                        disabled=True
                    ),
                    "address": st.column_config.TextColumn(
                        "Address",
                        disabled=True
                    ),
                    "monthly_int": st.column_config.NumberColumn(
                        "Rent",
                        format="£ %d",
                        disabled=True
                    ),
                    "link": st.column_config.LinkColumn(
                        "Details",
                        display_text="Zoopla",
                        disabled=True
                    ),
                    "agent_name": st.column_config.TextColumn(
                        "Agency",
                        disabled=True
                    ),
                    "natural_light_smiley_face": st.column_config.TextColumn(
                        "Natural Light",
                        disabled=True,
                        width="small"
                    ),
                    "large_windows_smiley_face": st.column_config.TextColumn(
                        "Large Windows",
                        disabled=True,
                        width="small"
                    ),
                    "high_ceiling_smiley_face": st.column_config.TextColumn(
                        "High Ceiling",
                        disabled=True,
                        width="small"
                    ),
                    "fireplace_smiley_face": st.column_config.TextColumn(
                        "Fireplace",
                        disabled=True,
                        width="small"
                    ),
                    "no_carpet_smiley_face": st.column_config.TextColumn(
                        "No Carpet",
                        disabled=True,
                        width="small"
                    ),
                    "wide_lenses_smiley_face": st.column_config.TextColumn(
                        "No Wide Lenses",
                        disabled=True,
                        width="small"
                    ),
                    "overprocessed_smiley_face": st.column_config.TextColumn(
                        "No Edited Photos",
                        disabled=True,
                        width="small"
                    ),
                },
                hide_index=True,
                height=height_config,
                use_container_width=True,
            )

            # Show a message with the number of resutls returned
            st.toast(f'{len(data_df)} results found.')
else:
    if "first_search_done" not in st.session_state:
        pass
    else:
        st.info("Preferences changed. Search again to refresh data!", icon=":material/change_circle:")


# As landing page show the large banner and the smaller banners. After the first search they disappear
if "first_search_done" not in st.session_state:
        
    st.markdown("### Find Out How it Works")

    column_c1, column_c2, column_c3, column_c4 = st.columns(4, gap="large")
    with column_c1:
        column_c11, column_c12, column_c13 = st.columns([1,2,1])
        with column_c11:
            st.empty()
        with column_c12:
            st.image("images/small_banners/house.png", width=200)     
        with column_c13:
            st.empty()
        
        st.markdown("##### :red[Picture your ideal home]")
        st.write("Imagine your future home by letting photos tell the story. AI can analyse images to match properties to your desires.")

    with column_c2:
        
        column_c21, column_c22, column_c23 = st.columns([1,2,1])
        with column_c21:
            st.empty()
        with column_c22:
            st.image("images/small_banners/search.png", width=200)     
        with column_c23:
            st.empty()

        st.markdown("##### :red[Filter the noise]")
        st.write("No more endless scrolling through irrelevant listings. Search only properties that meet your preferences.")
    
    with column_c3:

        column_c31, column_c32, column_c33 = st.columns([1,2,1])
        with column_c31:
            st.empty()
        with column_c32:
            st.image("images/small_banners/ai.png", width=200)     
        with column_c33:
            st.empty()

        st.markdown("##### :red[AI-powered search]")
        st.write("Our AI model analyses property images to identify characteristics that match your specific needs.")
        st.page_link('pages/under_the_hood.py', label='Learn More')
    
    with column_c4:

        column_c41, column_c42, column_c43 = st.columns([1,2,1])
        with column_c41:
            st.empty()
        with column_c42:
            st.image("images/small_banners/happy.png", width=200)     
        with column_c43:
            st.empty()
        
        st.markdown("##### :red[See only that fits]")
        st.write("Spend time viewing homes that match your criteria. Get to the right property without wasting your time.")


# Bottom of the page
st.divider()
st.write(f"Data updated: {creation_date_formatted}")

#st.session_state