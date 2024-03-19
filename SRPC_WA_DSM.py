import xml.etree.ElementTree as ET
from datetime import datetime
import streamlit as st
from io import BytesIO
import pandas as pd
import pdfplumber
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # Disable SSL certificate verification warning
def get_pdf(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching PDF: {e}")
        return None

def search_and_extract(pdf_bytes, search_word):
    tables = []
    try:
        with pdfplumber.open(BytesIO(pdf_bytes)) as pdf:
            escaped_word = re.escape(search_word)
            pattern = re.compile(fr"\b{escaped_word}\b", re.IGNORECASE)
            for page_number, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if pattern.search(text):
                    tables_ = page.extract_tables()
                    for table in tables_:
                        tables.append(table)
    except Exception as e:
        print(f"Error extracting tables: {e}")
    return tables

def extract_text_from_pdf(pdf_content):
    text = ""
    with pdfplumber.open(BytesIO(pdf_content)) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    with open("test2.txt", "w", encoding="utf-8") as file:
        file.write(text)
    return text

def extract_rows_with_keywords(pdf_content, search_terms, url):
    print("\nFetching rows that contain search terms in ", url)
    rows = re.split(r'\n', pdf_content)  # Split the PDF content into rows
    filtered_rows = []
    for row in rows:
        if any(term.lower() in row.lower() for term in search_terms):
            filtered_rows.append(row)
    print("------Rows fetched")
    return filtered_rows

def fetch_data(selected_year, selected_month):
    st.warning("Please select the week for which you'd like to fetch data, then click 'Continue' below.")
    # Fetching data from the provided URL
    url = "https://www.srpc.kar.nic.in/html/xml-search/data/commercial.xml?cache="
    response = requests.get(url, verify=False)
    xml_data = response.content
    root = ET.fromstring(xml_data)  # Parsing the XML data
    # Store the selected PDF URLs
    selected_urls = []

    # Extracting relevant information
    for document in root.findall('document'):
        period = document.find('period').text
        urls_found = False     # Flag to track if any URLs are found
        if selected_month.lower()[:3] in period.lower() and selected_year in period:
            for i in range(1, 7):  # Assuming URLs are numbered from 1 to 6
                url_tag = document.find(f'url{i}')
                if url_tag is not None and url_tag.text.endswith('.pdf') and 'dsm' in url_tag.text.lower():
                    urls_found = True  # Set flag to True if URLs are found
                    pdf_url = url_tag.text
                    title = period
                    # Create a checkbox for each PDF URL title
                    checkbox = st.checkbox(title)
                    # If checkbox is checked, add PDF URL to selected_urls list
                    if checkbox:
                        selected_urls.append(pdf_url)
        
            # if not urls_found:
            #     st.error("No data were found for the selected period.")

    search_terms =["SPRNG, NPKUNTA", "SPRNG, PUGULUR","Fortum Solar, PAVAGADA"]
    if st.button('Continue'):
        if selected_urls:
            # fetch_text(selected_urls)
            for url in selected_urls:
                with requests.get(url, verify=False) as response:
                    text = extract_text_from_pdf(response.content)
                    # print(text)
                    rows = extract_rows_with_keywords(text, search_terms,url)
                    for r in rows:
                        print(r)
            st.success("Extracted SRPC WA DSM✨")
            print("Extracted SRPC WA DSM✨")
        else:
            st.error("Please select at least one URL before continuing.")

# Streamlit app
st.title('SRPC WA DSM')
years = ['2024', '2023', '2022', '2021', '2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010']
# Create dropdown widgets for selecting the year and title filter
selected_year = st.selectbox('Select a Year:', years)
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
selected_month = st.selectbox("Select a month", options=months, index=2, format_func=lambda x: x.title())

# Call fetch_data function
fetch_data(selected_year, selected_month)
