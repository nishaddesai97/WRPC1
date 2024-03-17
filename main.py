from datetime import datetime
import streamlit as st


if __name__ == '__main__':
    st.markdown('### REGIONAL ENERGY ACCOUNTS')
    years = ['2024','2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
    
    # Create dropdown widgets for selecting the year and title filter
    selected_year = st.selectbox('Select a Year:', years)
    current_month = datetime.now().strftime('%B')
    selected_month = st.text_input('Enter a Month:', current_month)
    
    checkbox_labels = ["WRPC Regional Accounts", "WRPC DSM UI Accounts", "SRPC Option 1", "SRPC Option 2"]
    
    # Create multiple checkboxes
    checkbox_values = [st.checkbox(label) for label in checkbox_labels]

    if st.button('Extract Data'):
        for label, value in zip(checkbox_labels, checkbox_values):
            st.write(f"{label}: {value}")
