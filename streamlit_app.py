import pandas as pd
import streamlit as st
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timezone, timedelta


# Display Title and Description
st.title("L'Oréal Action Plan")

# Establishing a Google Sheet Connection
conn = st.experimental_connection('gsheets',type=GSheetsConnection)

# Ftech Exisiting Vendors data
existing_data = conn.read(worksheet= 'Action Details',usecols = list(range(8)) , ttl = 5)
existing_data = existing_data.dropna(how="all")

# List of Machine Names
machine_name_lst = [
    "LSH01",
    "LSH02",
    "LSH06",
    "LSH04",
    "LSH05",
    "All Machines"
]
maintenance_names = [
    "Abanoub M",
    "Trez M",
    "Tarek Mohamed Abdel Hakem",
    "Mohamed Said Abdel Azeem",
    "Mohamed Ezzat",
    "Amr Naguib El Sayed Hefny",
    "Micael Mina",
    "Hedar Ahmed Mohamed",
    "Nasser Tohamy Abdel Wahab",
    "Gomaa Ahmed Mahmoud",
    "Hassan Abdallah Mohamed",
    "Ahmed Soliman EL Kotb EL Afify",
    "Mohamed Saad Saleh Mahmoud",
    "Gehad Refaat Mohamed",
    "Others"
]
type_cat = ['Short Term','Mid Term','Long Term']
shift = ["|","||","|||"]
# Onboarding New Vendor Form
with st.form(key="action_plan_form"):
    machine_name = st.selectbox("Machine", machine_name_lst,index= 5 )
    action = st.selectbox("Action",existing_data[existing_data['Machine'] == machine_name]['Action'].tolist(),index=None,placeholder = "Select Action")
    type_cate = st.selectbox("Type", type_cat ,index =None,placeholder = "Select Type")
    tech = st.selectbox("Assigned To", maintenance_names,index =None ,placeholder = "Select Maintenenace Member")
    d = st.date_input("Date Of Completion", value = None ,format="DD/MM/YYYY" )
    f = st.selectbox("Shift Of Completion",shift ,index =None ,placeholder = "Select Shift Of Completion")
    maintenance_feedback = st.text_area(label="Maintenance Feedback")
    submit_button = st.form_submit_button(label="Submit")
    # If the submit button is pressed
    if submit_button:
        if not machine_name or not action:
            st.warning("Ensure To Select Machine Name")
            st.stop()
        else:
                existing_data.at[existing_data[existing_data['Action'] == action].index.to_list()[0],"Type"] = type_cate
                conn.update(worksheet='Operators Data',data=existing_data)
                st.success("Action is submitted With Full Data")
