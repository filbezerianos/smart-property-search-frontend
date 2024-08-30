import os
import streamlit as st
import pandas as pd
import time
from datetime import datetime


# Start with a wide page

st.set_page_config(
    page_title="Proper-ty Search",
    layout="wide",
    page_icon = ":material/house:",
    menu_items={
        'Get Help': "https://www.google.com",
        'Report a Bug': "https://www.google.com",
        'About': "Created by Orbiont Ltd."
    },
     initial_sidebar_state = 'collapsed'   
)

def main_button_click():
    st.session_state.first_search_done = True
    #st.session_state.expand_state = False
    if "expand_state" in st.session_state:
        del st.session_state["expand_state"]


def show_no_results_error():
    st.error(":material/sentiment_dissatisfied: Sorry, no results were found. Please try again with different preferences.")


# Load the csv with the data
df = pd.read_csv('data/properties.csv',  dtype={'property_id': 'str'})
#print(df.head())

# Get the creation date of the data file
data_file_creation_date = os.path.getctime('data/properties.csv')
creation_date_formatted = datetime.fromtimestamp(data_file_creation_date).strftime('%d %B %Y')
#st.write(f"Creation time: {creation_date_formatted}")

if "first_search_done" not in st.session_state:
        st.write("This is the guide")



with st.expander("MY SEARCH PREFERENCES", expanded = False, icon=":material/search:"):
#with st.popover(":material/search: MY SEARCH PREFERENCES", help=None, disabled=False, use_container_width=True):
    
    # The selection box to order the preferences
    order_feature_options = st.multiselect(
            "Which features are most important to you?",
            ["Prefer natural light", "Dislike carpets", "Avoid wide-lenses photos", "No over-processed photos"],
            placeholder="Select your top preferences in order..."
        )
    
    column_a1, column_a2, column_a3, column_a4 = st.columns(4)
    with column_a1:
        number_of_bedrooms = st.number_input("Bedrooms", min_value=1, max_value=3, value="min", step=1, help="Number of bedrooms (for Room Rental and Studios select 1)")         
    with column_a2:
        postcode = st.text_input("Postcode", value="", max_chars=4, help="Write the first letters of the postcode")      
    with column_a3:
        min_monthly_rent = st.number_input("Min Rent", min_value=100, value=800, step=200, help="Minimum monthly rent in £")
    with column_a4:
        max_monthly_rent = st.number_input("Max Rent", min_value=200, value=1200, step=200, help="Maximum monthly rent in £")

    st.divider()

    # The radio buttons
    exclude_enough_photos_overall = st.toggle("Hide properties with insufficient photos", value=True, help="Choose this option to exclude properties with an insufficient number of photos")         
    exclude_enough_bedroom_photos = st.toggle("Hide properties with limited bedroom photos", value=True, help="Choose this option to exclude properties that lack sufficient photos of the bedrooms")   
    exclude_room_to_rent = st.toggle("Hide rental rooms", value=True, help="Choose this option to exclude rental rooms")

    st.divider()
    update_results = st.button("Find Your Perfect Match", type="primary", on_click=main_button_click, key="button")    


    
    
with st.sidebar:
    st.page_link('main_expander.py', label='Property Search', icon=':material/search:')
    st.page_link('pages/help.py', label='Help Me', icon=':material/help:')
    st.page_link('pages/feedback.py', label='Leave Feedback', icon=':material/feedback:')

    st.divider()
    st.write(f"© {datetime.now().year} Orbiont")







# Configure the dictionary for features ordering
features_dict = {
    "Prefer natural light": ["natural_light_score", False],
    "Dislike carpets": ["no_carpet_score", False],
    "Avoid wide-lenses photos": ["wide_lenses_score", True],
    "No over-processed photos": ["overprocessed_score", True],
}








###
# MAIN PAGE CONFIGURATION
###

st.session_state

st.logo("images/logo_small.svg")

#column_b1, column_b2 = st.columns([1,20])
#with column_b1:
    #st.image("images/logo.svg", width=60) 
#with column_b2:
    #st.subheader("PROPERty SEARCH")
    #st.markdown("## :blue[Proper]:grey[ty] :blue[Search]")
    #st.write("A better way to find your perfect property")

#st.markdown("## :blue[Proper]:grey[ty] :blue[Search]")
#st.divider()







if update_results:

    

    # Set the search preferences to ok
    search_preferences_ok = True

    # Filter based on user selection
    #st.write(features_dict[order_feature_options[0]][1])
    #st.write(len(order_feature_options))  

    #st.success('This is a success message!', icon="✅")
    #st.info('This is a purely informational message', icon="ℹ️")
    #st.warning('This is a warning', icon="⚠️")
    #st.toast('Hip!')

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


        # Order the final results based on the preferences order
        #for ordering in reversed(order_feature_options):
            #st.write(ordering)
            #st.write(features_dict[ordering][0])
            #st.write(features_dict[ordering][1])

            #filtered_df = filtered_df.sort_values(by=[features_dict[ordering][0]], ascending=[bool(features_dict[ordering][1])])

        # If there are any NULL values replace with 0
        # Replace NULL values with 0
        filtered_df = filtered_df.fillna(0)

        # Create a new column based on existing columns
        if order_feature_options:
            #selected_columns = [features_dict[feature][0] for feature in order_feature_options]
            #st.write(selected_columns)

            #filtered_df['preferences_alignment'] = filtered_df[selected_columns].mean(axis=1).round(1)
            #st.write(len(filtered_df['preferences_alignment']))

            #filtered_df = filtered_df.sort_values(by=['preferences_alignment'], ascending=[False])


            weight = len(order_feature_options)

            for ordering in order_feature_options:
                #st.write(features_dict[ordering][0])
                #st.write(len(order_feature_options))

                if 'preferences_alignment' in filtered_df:
                    filtered_df['preferences_alignment'] = filtered_df['preferences_alignment'] + (filtered_df[features_dict[ordering][0]] * weight)
                    #st.write(st.write(weight))
                    weight -= 1
                else:
                    filtered_df['preferences_alignment'] = filtered_df[features_dict[ordering][0]] * weight
                    #st.write(weight)
                    weight -= 1
            
            # Normalise the values to 1
            max_value = filtered_df['preferences_alignment'].max()
            if max_value > 1:
                filtered_df['preferences_alignment'] = filtered_df['preferences_alignment'] / max_value                  

            # Order the list based on the new column for preferences alignment
            filtered_df = filtered_df.sort_values(by='preferences_alignment', ascending=False)
            filtered_df['preferences_alignment'] = (filtered_df['preferences_alignment']*5).round(2)

            filtered_df['asterisk_column'] = (filtered_df['preferences_alignment']).round().astype(int).apply(lambda x: '★' * x)
            #st.write(filtered_df['asterisk_column'])                  

        else:
            pass

        data_df = pd.DataFrame(filtered_df)

        # Check if there are any resutls returned after filtering
        if len(data_df) == 0:
            #st.error(":material/sentiment_dissatisfied: Sorry, no results were found. Please try again with different preferences.")
            show_no_results_error()
        
        else:

            # Set the session state of guide shown so that we do not show it again
            #st.session_state.guide_shown = True

            # Configure the order of the columms based on the selection of preferences
            if order_feature_options:
                column_order_config = ("asterisk_column","title","address","monthly_int","link","agent_name")
                #column_order_config = ("asterisk_column","preferences_alignment","title","address","monthly_int","link","agent_name")
                #column_order_config = ("title","address","monthly_int","link","agent_name")
                for ordering in order_feature_options:
                    column_order_config = column_order_config + (features_dict[ordering][0],)
                
                # Add the column for the number of photos
                #column_order_config = column_order_config + ("number_of_photos_overall_count",)
                
            else:
                st.info("Select your top preferences to narrow down your results even more!", icon=":material/info:")
                column_order_config = ("title","address","monthly_int","link","agent_name")
                pass

            # Check if postcode has been provided
            if not postcode:
                st.info("Choose a postcode to narrow down your results even more!", icon=":material/info:")

            # Configure the height of the table so that we do not have a scrollbar inside the table
            height_config = 35 * len(data_df) + 38
            #st.write(height_config)


            # Load the data in a table
            st.data_editor(
                data_df,
                #column_order=("title","address","monthly_int","link","agent_name","wide_lenses_score","overprocessed_score","natural_light_score","no_carpet_score"),
                column_order=column_order_config,
                column_config={
                    "asterisk_column": st.column_config.TextColumn(
                        "Stars",
                        help="Shows the alignment score across the selected preferences",
                        disabled=True
                    ),
                    "preferences_alignment": st.column_config.ProgressColumn(
                        "Alignment",
                        help="Shows the average alignment score across the selected preferences",
                        width="small",
                        format="%f",
                        min_value=0,
                        max_value=5,
                    ),
                    "property_id": st.column_config.TextColumn(
                        "Property ID",
                        help="The Property ID from Zoopla",
                        disabled=True
                    ),

                    "title": st.column_config.TextColumn(
                        "Description",
                        disabled=True
                    ),
                    
                    "address": st.column_config.TextColumn(
                        "Address",
                        disabled=True
                    ),

                    "monthly_int": st.column_config.NumberColumn(
                        "Monthly Rent",
                        format="£ %d",
                        disabled=True
                    ),

                    "link": st.column_config.LinkColumn(
                        "Link",
                        display_text="Open Link",
                        disabled=True
                    ),

                    "agent_name": st.column_config.TextColumn(
                        "Agency",
                        disabled=True
                    ),

                    "wide_lenses_score": st.column_config.ProgressColumn(
                        "Wide Lenses",
                        width="small",
                        format="%.1f",
                        min_value=0,
                        max_value=1,
                    ),

                    "overprocessed_score": st.column_config.ProgressColumn(
                        "Overprocessed",
                        width="small",
                        format="%.1f",
                        min_value=0,
                        max_value=1,
                    ),

                    "natural_light_score": st.column_config.ProgressColumn(
                        "Natural Light",
                        width="small",
                        format="%.1f",
                        min_value=0,
                        max_value=1,
                    ),

                    "no_carpet_score": st.column_config.ProgressColumn(
                        "No Carpet",
                        width="small",
                        format="%.1f",
                        min_value=0,
                        max_value=1,
                    ),

                    "number_of_photos_overall_score": st.column_config.NumberColumn(
                        "Photos",
                        width="small",
                        disabled=True
                    ),

                    "number_of_bedroom_photos_score": st.column_config.NumberColumn(
                        "Bedroom Photos",
                        width="small",
                        disabled=True
                    ),
                    "number_of_photos_overall_count": st.column_config.NumberColumn(
                        "Number of Photos",
                        width="small",
                        disabled=True
                    ),

                },
                hide_index=True,
                height=height_config,
                key="table",
            )

            # Set update_results to false
            update_results = False

            #st.write("Rate the results:")
            #st.feedback(options="thumbs")

            st.toast(f'{len(data_df)} results found.')
else:
    
    if 'guide_shown' not in st.session_state:
        #st.write("This is the guide")
        #st.write_stream("Easily discover properties with the exact features you desire in 2 simple steps.")
        #st.divider()
        #st.markdown("### Why?")
        #st.markdown("Text here...")

        #st.divider()
        #st.markdown("### How it works")

        #st.session_state.guide_shown  = True
        pass
    else: 
        #st.write("Search to see the results.")
        #st.info("Preferences changed. Click to refresh data!", icon=":material/info:")
        pass
        #st.session_state.guide_shown  = True


if "first_search_done" not in st.session_state:
        #st.write("This is the guide")
        #st.write_stream("Easily discover properties with the exact features you desire in 2 simple steps.")
        st.divider()
        st.markdown("### Why?")
        st.markdown("Text here...")

        st.divider()
        st.markdown("### How it works")


st.divider()
st.write(f"Data updated: {creation_date_formatted}")