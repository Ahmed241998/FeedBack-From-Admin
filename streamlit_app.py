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
machine_name = [
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
    timezone_offset = 3  # Pacific Standard Time (UTC−08:00)
    tzinfo = timezone(timedelta(hours=timezone_offset))
    date = datetime.now(tzinfo)
    datem = date.date()
    name = st.text_input(label="Name")
    machine_name = st.selectbox("Machine", machine_name,index = None,placeholder = "Select Machine")
    problem = st.text_area(label="Problem Details")
    action = st.text_area(label="Action Details")
    type_cate = st.selectbox("Type", type_cat ,index =None,placeholder = "Select Type")
    tech = st.selectbox("Assigned To", maintenance_names,index =None ,placeholder = "Select Maintenenace Member")
    d = st.date_input("Date Of Completion", datem ,format="DD/MM/YYYY" )
    f = st.selectbox("Shift Of Completion",shift ,index =None ,placeholder = "Select Shift Of Completion")

    submit_button = st.form_submit_button(label="Submit")

    # If the submit button is pressed
    if submit_button:
        # Check if all mandatory fields are filled
        if not name or not machine_name or not action:
            st.warning("Ensure all mandatory fields are filled.")
            st.stop()
        else:
            # Create a new row of vendor data
            action_data = pd.DataFrame(
                [
                    {
                        "Date": date,
                        "Name": name,
                        "Machine": machine_name,
                        "Problem": problem,
                        "Action": action,
                        "Type":type_cate,
                        "Assigned To":tech,
                        "Date Of Completion": d,
                        "Shift Of Completion" : f
                    }
                ]
            )
            # Add the new vendor data to the existing data
            updated_df = pd.concat([existing_data, action_data], ignore_index=True)
            conn.update(worksheet='Action Details',data=updated_df)
            st.success("Action is submitted With Full Data")

