from datetime import datetime
import streamlit as st
import os

import WRPC_DSM_UI_Accounts
import WRPC_REGIONAL_ENERGY_ACCOUNTS
import SRPC_REA_RTA
import SRPC_WA_DSM

data_extracted = False

filename = f"Extracted Data_WRPC_SRPC_{datetime.now().strftime('%d-%m-%Y')}.xlsx"
# def delete_file():
#     if os.path.exists(filename):
#         os.remove(filename)
#         st.success(f"File '{filename}' has been deleted successfully.")
#     else:
#         st.warning(f"File '{filename}' does not exist.")

# def download_file():
#     if os.path.exists(filename):
#         with open(filename, "rb") as f:
#             file_content = f.read()
#         st.download_button(label="Download File", data=file_content, file_name=filename)
#     else:
#         st.warning("No data has been extracted yet.")

if __name__ == '__main__':
    st.markdown('### Data Extraction from WRPC and SRPC')
    # if st.button("Delete File"):
    #     delete_file()

    years = ['2024','2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
    # Create dropdown widgets for selecting the year and title filter
    selected_year = st.selectbox('Select a Year:', years)
    
    current_month = datetime.now().strftime('%B')
    months = ["January", "February", "March", "April","May", "June", "July", "August","September", "October", "November", "December"] 
    current_month_index = months.index(current_month)
    selected_month = st.selectbox("Select a month", options=months, index=current_month_index, format_func=lambda x: x.title())
    
    # Define a dictionary mapping each label to its corresponding function
    function_mapping = {
        "WRPC Regional Accounts": WRPC_REGIONAL_ENERGY_ACCOUNTS.extract_data,
        "WRPC DSM UI Accounts": WRPC_DSM_UI_Accounts.fetch_pdfs,
        "SRPC REA_RTA": SRPC_REA_RTA.fetch_data,
        "SRPC_WA_DSM": SRPC_WA_DSM.fetch_data
    }
    
    st.error("Opening the Excel file during code execution can result in critical errors. Please refrain from doing so.")
    checkbox_labels = ["WRPC Regional Accounts", "WRPC DSM UI Accounts", "SRPC REA_RTA", "SRPC_WA_DSM"]
    selected_option = st.radio("Select an option", checkbox_labels)
    # if st.button("Start"):
    function_mapping[selected_option](selected_year, selected_month)

    # checkbox_values = [st.checkbox(label) for label in checkbox_labels]         # Create multiple checkboxes

    # if st.button("Start"):
    # for label, value in zip(checkbox_labels, checkbox_values):
    #     if value:
    #         function_mapping[label](selected_year, selected_month)  # Call the corresponding function based on the selected option
    # data_extracted = any(checkbox_values)       # Set the flag to True if any data extraction occurs  
    # download_file()         # Call download_file function after all data extraction functions have completed
