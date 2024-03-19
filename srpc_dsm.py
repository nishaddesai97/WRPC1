import streamlit as st
import requests
import urllib3
import xml.etree.ElementTree as ET
import re

# Disable SSL certificate verification warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Fetching data from the provided URL
url = "https://www.srpc.kar.nic.in/html/xml-search/data/commercial.xml?cache="
response = requests.get(url, verify=False)
xml_data = response.content

# Parsing the XML data
root = ET.fromstring(xml_data)

# Extracting relevant information
documents = {}
for document in root.findall('document'):
    doc_type = document.find('type').text
    period = document.find('period').text
    url1_element = document.find('url1')
    url1 = url1_element.text if url1_element is not None else None
    if url1 is not None:
        # Extract year from the period using regex
        match_year = re.search(r'(\d{4})-(\d{2})', doc_type)  # Match year in the format YYYY-YY
        match_month = re.search(r'(\w{4})', period) # Match month in the format YYYY-MMM
        if match_year and match_month:
            year = match_year.group(1)  # Taking the first year mentioned
            month = match_month.group(1) # Taking the first month mentioned
            documents.setdefault(year, {}).setdefault(month, []).append((period, url1))

# Streamlit app
st.title('SRPC DSM Documents')

# Get unique years from the documents
years = sorted(documents.keys(), reverse=True)
selected_year = st.selectbox('Select Year', years)

if selected_year:
    months = sorted(documents[selected_year].keys())
    selected_month = st.selectbox('Select Month', months)

    if selected_month:
        st.subheader(f'Documents for {selected_month} {selected_year}')
        for period, url1 in documents[selected_year][selected_month]:
            checkbox_value = st.checkbox(label=f"[{period}]({url1})", value=False)
