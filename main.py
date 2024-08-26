import streamlit as st
import pandas as pd


# Start with a wide page
def wide_space_default():
    st.set_page_config(layout="wide")
   
wide_space_default()


# Configure the dictionary for features ordering
features_dict = {
    "I like natural light": ["natural_light_score", False],
    "I don't like carpets": ["no_carpet_score", False],
    "I don't like wide-lenses photos": ["wide_lenses_score", True],
    "I don't like over-processed photos": ["overprocessed_score", True],
}


# Load the csv with the data
df = pd.read_csv('data/streamlit.csv',  dtype={'property_id': 'str'})
#print(df.head())



"""
PREFERENCES MENU ON THE SIDEBAR
"""

# Load the preferences menu on the sidebar
with st.sidebar:

    column_a1, column_a2 = st.columns(2)
    with column_a1:
        number_of_bedrooms = st.number_input("Bedrooms", min_value=1, max_value=3, value="min", step=1, help="Number of bedrooms (for Room Rental and Studios select 1)")
        min_monthly_rent = st.number_input("Min Rent", min_value=100, value="min", step=200, help="Minimum monthly rent in £")  
    with column_a2:
        postcode = st.text_input("Postcode", value="", max_chars=4, help="Write the first letters of the postcode")
        max_monthly_rent = st.number_input("Max Rent", min_value=1200, value=min_monthly_rent, step=200, help="Maximum monthly rent in £")

    
    # The selection box to order the preferences
    order_feature_options = st.multiselect(
            "Which features are most important to you?",
            ["Prefer natural light", "Dislike carpets", "Avoid wide-lenses photos", "No over-processed photos"],
            placeholder="Select your top preferences..."
        )
    
    # The radio buttons
    exclude_enough_photos_overall = st.toggle("Hide properties with insufficient photos", value=True, help="Choose this option to exclude properties with an insufficient number of photos")  
    exclude_enough_bedroom_photos = st.toggle("Hide properties with limited bedroom photos", value=True, help="Choose this option to exclude properties that lack sufficient photos of the bedrooms")
    exclude_room_to_rent = st.toggle("Hide rental rooms", value=True, help="Choose this option to exclude rental rooms")

    update_results = st.button("Find Your Perfect Match", type="primary")




"""
MAIN PAGE CONFIGURATION
"""

if update_results:
    # Filter based on user selection
    #st.write(features_dict[order_feature_options[0]][1])
    #st.write(len(order_feature_options))  

    #st.success('This is a success message!', icon="✅")
    #st.info('This is a purely informational message', icon="ℹ️")
    #st.warning('This is a warning', icon="⚠️")
    #st.toast('Hip!')  


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
    for ordering in reversed(order_feature_options):
        #st.write(ordering)
        #st.write(features_dict[ordering][0])
        #st.write(features_dict[ordering][1])

        filtered_df = filtered_df.sort_values(by=[features_dict[ordering][0]], ascending=[bool(features_dict[ordering][1])])


    data_df = pd.DataFrame(filtered_df)


    # Configure the order of the columms based on the selection of preferences
    column_order_config = ("title","address","monthly_int","link","agent_name")

    if order_feature_options:
        for ordering in order_feature_options:
            column_order_config = column_order_config + (features_dict[ordering][0],)
    else:
        #column_order_config = ("title","address","monthly_int","link","agent_name")
        pass


    # Configure the height of the table so that we do not have a scrollbar inside the table
    height_config = 35 * len(data_df) + 38
    #st.write(height_config)


    # Load the data in a table
    st.data_editor(
        data_df,
        #column_order=("title","address","monthly_int","link","agent_name","wide_lenses_score","overprocessed_score","natural_light_score","no_carpet_score"),
        column_order=column_order_config,
        column_config={
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
                format="%f",
                min_value=0,
                max_value=1,
            ),

            "overprocessed_score": st.column_config.ProgressColumn(
                "Overprocessed",
                width="small",
                format="%f",
                min_value=0,
                max_value=1,
            ),

            "natural_light_score": st.column_config.ProgressColumn(
                "Natural Light",
                width="small",
                format="%f",
                min_value=0,
                max_value=1,
            ),

            "no_carpet_score": st.column_config.ProgressColumn(
                "No Carpet",
                width="small",
                format="%f",
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

        },
        hide_index=True,
        height=height_config,
    )

    # Set update_results to false
    update_results = False

    st.write("Rate the results:")
    st.feedback(options="thumbs")

    st.toast(f'{len(data_df)} results found.')
else:
    st.write("Search to see the results.")

 
st.divider()
st.write("This is an awesome app")