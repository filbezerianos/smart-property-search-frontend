import os
import streamlit as st
import pandas as pd
from datetime import datetime


# Start with the page config
st.set_page_config(
    page_title="Home Match AI",
    layout="wide",
    page_icon = ":material/house:",
    menu_items={
        'About': "Created by Orbiont Ltd."
    },
     initial_sidebar_state = 'collapsed'   
)



# Configure the sidebar
with st.sidebar:
    st.page_link('main.py', label='Home', icon=':material/house:', disabled=True)
    st.page_link('pages/faq.py', label='FAQs', icon=':material/help:')
    st.page_link('https://tally.so/r/3NJ5gO', label='Get in Touch', icon=':material/alternate_email:')

    st.divider()
    st.write(f"© {datetime.now().year} Orbiont")


def main_button_click():
    st.session_state.first_search_done = True
    if "searches_count" not in st.session_state:
        st.session_state.searches_count = 1
    else:
        st.session_state.searches_count += 1


def show_no_results_error():
    st.error(":material/sentiment_dissatisfied: Sorry, no results were found. Please try again with different preferences.")



def apply_face(value):
    if value <= 0:
        #return '⚪⚪⚪⚪⚪'
        return '○○○○○'
    elif 0 < value < 0.2:
        #return '🟠⚪⚪⚪⚪'
        return '●○○○○'
    elif 0.2 <= value < 0.4:
        #return '🟠🟠⚪⚪⚪'
        return '●●○○○'
    elif 0.4 <= value < 0.6:
        #return '🟠🟠🟠⚪⚪'
        return '●●●○○'
    elif 0.6 <= value < 0.8:
        #return '🟠🟠🟠🟠⚪'
        return '●●●●○'
    elif 0.8 <= value <= 1:
        #return '🟠🟠🟠🟠🟠'
        return '●●●●●'
    else:
        return 'None'  # In case the value is outside the expected range


# Load the csv with the data
df = pd.read_csv('data/properties.csv',  dtype={'property_id': 'str'}).sort_values(by='monthly_int', ascending=True)


# Add new columns with the score dots
df['natural_light_smiley_face'] = df['natural_light_score'].apply(apply_face)
df['large_windows_smiley_face'] = df['large_windows_score'].apply(apply_face)
df['high_ceiling_smiley_face'] = df['high_ceiling_score'].apply(apply_face)
df['fireplace_smiley_face'] = df['fireplace_score'].apply(apply_face)
df['no_carpet_smiley_face'] = df['no_carpet_score'].apply(apply_face)
df['wide_lenses_smiley_face'] = df['wide_lenses_score'].apply(apply_face)
df['overprocessed_smiley_face'] = df['overprocessed_score'].apply(apply_face)

# Get the creation date of the data file
#data_file_creation_date = os.path.getctime('data/properties.csv')
#creation_date_formatted = datetime.fromtimestamp(data_file_creation_date).strftime('%d %B %Y')


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
st.markdown("## :blue[Home Match AI.] Discover a :blue[Home with Character.] Not Just the Basics.")

if "searches_count" not in st.session_state:
    pass
else:
    if st.session_state.searches_count > 4 and "asked_for_feedback" not in st.session_state:
        st.info(f"If you have any questions, feedback or suggestions, we would love to hear from you! :material/alternate_email: [Get in touch!](https://tally.so/r/3NJ5gO)")
        st.session_state.asked_for_feedback = True
    else:
        pass

if "first_search_done" not in st.session_state:
    #st.image("images/large_banner.png", use_column_width="always")
    pass
else:
    #st.markdown("### :blue[Smart Property Search.] Where AI Meets the Photos of Your Next Home.")
    pass

# The search preferences container
with st.container(border=True):
    # The selection box to order the preferences
    order_feature_options = st.multiselect(
            "What do you care about the most in a home?",
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
            show_only_top_rated_properties = st.toggle("Show only top-rated properties", value=False, help="Choose this option to filter out properties that may not meet your preferences.")
            exclude_zoopla = st.toggle("Hide Zoopla properties", value=False, help="Choose this option to exclude properties from Zoopla")
            exclude_rightmove = st.toggle("Hide Rightmove properties", value=False, help="Choose this option to exclude properties from Rightmove")
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
    
    if exclude_zoopla and exclude_rightmove:
        st.error(f":material/error: Zoopla and Rightmove properties cannot be excluded at the same time. Please select at least one to proceed.")
        search_preferences_ok = False



    ###
    # IF THE PREFERENCES ARE OK, LOAD THE RESULTS
    ###

    if search_preferences_ok:

        # Filter the properties based on the preferences
        filtered_df = df[(df['monthly_int'] >= min_monthly_rent) & (df['monthly_int'] <= max_monthly_rent)]
        filtered_df = filtered_df[filtered_df['address'].str.contains(str(postcode).upper())]
        filtered_df = filtered_df[filtered_df['bed_number'] == number_of_bedrooms]

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

        if exclude_zoopla:
            filtered_df = filtered_df[filtered_df['property_platform'] != "Zoopla"]
        else:
            pass

        if exclude_rightmove:
            filtered_df = filtered_df[filtered_df['property_platform'] != "Rightmove"]
        else:
            pass

        # If there are any NULL values replace with 0
        filtered_df = filtered_df.fillna(0)

        # Check how may results have left after th estandard filtering
        if len(filtered_df) == 0:
            show_no_results_error()
        elif len(filtered_df) >1500:
            st.error(f":material/error: Your search returned {len(filtered_df)} results. Please refine your query to narrow down the results.")
        else:

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
                #filtered_df['natural_light_smiley_face'] = df['natural_light_score'].apply(apply_face)
                #filtered_df['large_windows_smiley_face'] = df['large_windows_score'].apply(apply_face)
                #filtered_df['high_ceiling_smiley_face'] = df['high_ceiling_score'].apply(apply_face)
                #filtered_df['fireplace_smiley_face'] = df['fireplace_score'].apply(apply_face)
                #filtered_df['no_carpet_smiley_face'] = df['no_carpet_score'].apply(apply_face)
                #filtered_df['wide_lenses_smiley_face'] = df['wide_lenses_score'].apply(apply_face)
                #filtered_df['overprocessed_smiley_face'] = df['overprocessed_score'].apply(apply_face)

                # Increase the counter for the searches with feature preferences
                if "number_of_feature_searches" not in st.session_state:
                    st.session_state.number_of_feature_searches = 1
                    with st.container(border=True):
                        st.markdown("Here's a quick guide to help you understand **how well each property matches your preferences**:")
                        #st.write("🟠⚪⚪⚪⚪: Minimal | 🟠🟠⚪⚪⚪: Slight | 🟠🟠🟠⚪⚪: Moderate | 🟠🟠🟠🟠⚪: Strong | 🟠🟠🟠🟠🟠: Excellent")
                        st.write("●○○○○: Minimal | ●●○○○: Slight | ●●●○○: Moderate | ●●●●○: Strong | ●●●●●: Excellent")
                else:
                    st.session_state.number_of_feature_searches += 1

                # If the option to filter to top-rated properties is selected
                if show_only_top_rated_properties:
                    filtered_df = filtered_df[filtered_df['preferences_alignment'] >= 0.7]

            else:
                # If no photo preferences selected
                if "number_of_feature_searches" not in st.session_state:
                    st.info(f":material/info: Try selecting what you care the most in a home from the top menu and see how well each property matches your preferences.")
                else:
                    pass

            # Use the filtered results to load the table
            data_df = pd.DataFrame(filtered_df)
  
            # Configure the order of the columms based on the selection of preferences
            column_order_config = ("title","address","monthly_int","property_platform","link","agent_name")
            if order_feature_options:         
                for ordering in order_feature_options:
                    column_order_config = column_order_config + (features_dict[ordering][2],)           
            else:
                pass

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
                    "property_platform": st.column_config.TextColumn(
                        "Platform",
                        width="small",
                        disabled=True
                    ),
                    "link": st.column_config.LinkColumn(
                        "Details",
                        display_text="More ↗",
                        width="small",
                        disabled=True
                    ),
                    "agent_name": st.column_config.TextColumn(
                        "Agency",
                        disabled=True,
                    ),
                    "preferences_alignment": st.column_config.ProgressColumn(
                        "Align Score",
                        min_value = 0,
                        max_value = 1,
                        format="%.2f",
                        width="small"
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
        
    #st.divider()
    st.write("")

    column_c1, column_c2, column_c3, column_c4 = st.columns(4, gap="large")
    with column_c1:
        column_c11, column_c12, column_c13 = st.columns([1,2,1])
        with column_c11:
            st.empty()
        with column_c12:
            st.image("images/small_banners/house.png", width=200)     
        with column_c13:
            st.empty()
        
        st.markdown("##### :blue[Image your dream home]")
        st.write("Let photos bring your future home to life. Our AI analyses images to find properties that match your desires.")

    with column_c2: 
        column_c21, column_c22, column_c23 = st.columns([1,2,1])
        with column_c21:
            st.empty()
        with column_c22:
            st.image("images/small_banners/search.png", width=200)     
        with column_c23:
            st.empty()

        st.markdown("##### :blue[Filter the noise]")
        st.write("No more endless scrolling through irrelevant listings. Search only properties that meet your exact preferences.")
    
    with column_c3:
        column_c31, column_c32, column_c33 = st.columns([1,2,1])
        with column_c31:
            st.empty()
        with column_c32:
            st.image("images/small_banners/ai.png", width=200)     
        with column_c33:
            st.empty()

        st.markdown("##### :blue[Smart, AI-powered search]")
        st.write("Our AI model analyses property images to identify characteristics that match your specific needs.")
          
    with column_c4:
        column_c41, column_c42, column_c43 = st.columns([1,2,1])
        with column_c41:
            st.empty()
        with column_c42:
            st.image("images/small_banners/happy.png", width=200)     
        with column_c43:
            st.empty()
        
        st.markdown("##### :blue[See only what fits]")
        st.write("Spend time viewing homes that meet your criteria. Save time and go straight to the right property.")


    st.divider()
    st.markdown("## What We Are Excited About")
    st.write("Our AI model integrated with smart search is designed to benefit everyone in the property market. Whether you are a home seeker finding your dream home, an estate agent looking to match clients with their ideal properties or a client assistant catering to specific needs, we can streamline the process and deliver results tailored to you.")
    st.write("")

    column_d1, column_d2, column_d3, column_d4, column_d5, column_d6 = st.columns(6, gap="large")
    with column_d1:         
        st.image("images/large_banners/home_seeker.png", width=275)
    with column_d2:
        st.write('>"I love being able to search for specific features like :blue[large windows]. It saves us so much time by showing only the properties that match exactly what my partner and I are looking for."')
        st.markdown("Home Seeker")
    with column_d3:
        st.image("images/large_banners/real_estate_agent.png", width=275)     
    with column_d4:
        st.write('>"My clients often have specific preferences, like :blue[high ceilings] and :blue[hardwood floors]. Being able to filter properties based on these details is a game-changer. It allows me to focus on showings that truly meet their needs."')
        st.markdown("Real Estate Agent")
    with column_d5:
        st.image("images/large_banners/private_client_assistant.png", width=275)     
    with column_d6:
        st.write('>"My clients have specific demands. Finding the perfect property for them has been a challenge. Being able to rank properties based on features like :blue[natural light] has significantly improved our service and cut down the time it takes to find the ideal match for our clients."')
        st.markdown("Private Client Assistant")

    st.divider()
    
    column_d1, column_d2 = st.columns(2,gap="large")
    with column_d1:
        st.markdown("## Quick :blue[Tour]")
        st.write("")
        st.video("https://youtu.be/jrlK6PtMNcY")
    with column_d2:
        st.markdown("## Join the :blue[Insider List]")
        st.write("")
        st.write("Stay in the loop and be the first to know about application updates. You may also receive exclusive invitations to try pre-release versions and experience new features early. To subscribe, simply drop us a message [here](https://tally.so/r/3NJ5gO).")

# Bottom of the page
st.divider()
st.image("images/logo/orbiont_logo.png", width=150) 
#st.write(f"Data updated: {creation_date_formatted}")

#st.session_state