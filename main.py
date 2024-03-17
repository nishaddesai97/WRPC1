from datetime import datetime
import streamlit as st
import os

import WRPC_DSM_UI_Accounts
import WRPC_REGIONAL_ENERGY_ACCOUNTS
data_extracted = False

filename = f"Extracted Data_WRPC_SRPC_{datetime.now().strftime('%d-%m-%Y')}.xlsx"
# def delete_file():
#     if os.path.exists(filename):
#         os.remove(filename)
#         st.success(f"File '{filename}' has been deleted successfully.")
#     else:
#         st.warning(f"File '{filename}' does not exist.")
        
def download_file():
    if data_extracted:
        with open(filename, "rb") as f:
            file_content = f.read()
        st.download_button(label="Download File", data=file_content, file_name=filename)
    else:
        st.warning("No data has been extracted yet.")

if __name__ == '__main__':
    st.markdown('### WRPC SRPC EXTRACT DATA')
    
    years = ['2024','2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
    # Create dropdown widgets for selecting the year and title filter
    selected_year = st.selectbox('Select a Year:', years)
    current_month = datetime.now().strftime('%B')
    months = ["January", "February", "March", "April","May", "June", "July", "August","September", "October", "November", "December"] 
    selected_month = st.selectbox("Select a month", options=months, index=0, format_func=lambda x: x.title())
    
    
    # if st.button("Delete File"):
    #     delete_file()

    checkbox_labels = ["WRPC Regional Accounts", "WRPC DSM UI Accounts", "SRPC SRPC_REA_REA", "SRPC_WA_DSM"]
    # Create multiple checkboxes
    checkbox_values = [st.checkbox(label) for label in checkbox_labels]

    # Define a dictionary mapping each label to its corresponding function
    function_mapping = {
        "WRPC Regional Accounts": WRPC_REGIONAL_ENERGY_ACCOUNTS.extract_data,
        "WRPC DSM UI Accounts": WRPC_DSM_UI_Accounts.fetch_pdfs,
        # "SRPC Option 1": SRPC_REA_REA,
        # "SRPC Option 2": SRPC_WA_DSM
    }

    for label, value in zip(checkbox_labels, checkbox_values):
        if value:
            function_mapping[label](selected_year, selected_month)  # Call the corresponding function based on the selected option
    
    data_extracted = any(checkbox_values)       # Set the flag to True if any data extraction occurs
    download_file()         # Call download_file function after all data extraction functions have completed
