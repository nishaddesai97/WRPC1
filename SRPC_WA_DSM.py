from openpyxl import Workbook, load_workbook
import xml.etree.ElementTree as ET
from openpyxl.styles import Font
from datetime import datetime
import streamlit as st
from io import BytesIO
import pandas as pd
import pdfplumber
import requests
import urllib3
import re
import os

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
    # with open("test2.txt", "w", encoding="utf-8") as file:
    #     file.write(text)
    return text

def extract_rows_with_keywords(pdf_content, url):
    search_terms =["SPRNG, NPKUNTA", "Sprng, Pugalur" ,"Fortum Solar, PAVAGADA"]
    print("\nFetching rows that contain search terms in ", url)
    rows = re.split(r'\n', pdf_content)  # Split the PDF content into rows
    filtered_rows = []
    WS_Seller = []
    matches= ""

    pattern = rf'(?m)^{re.escape("Sprng, Pugalur (Wind)")} .*?$'
    matches = re.findall(pattern, pdf_content)
    for match in matches:
        WS_Seller.append(match)

    for st in search_terms:
        if st == "SPRNG, NPKUNTA":
            pattern = rf'(?m)^{re.escape(st)} .*?$'
            matches = re.findall(pattern, pdf_content)
            for row in matches:
                if len(row.split()) == 10:
                    filtered_rows.append(row)
                elif len(row.split()) == 7:
                    WS_Seller.append(row)

        if st == "Sprng, Pugalur":
            pattern = r"(Sprng),\s(Pugalur)\n(\d{4}-\d{2}-\d{2} \d+\.\d+ \d+\.\d+ \d+ \-\d+\.\d+ \d+\.\d+ \-\d+\.\d+ \d+\.\d+)\n\((Wind)\)"
            # pattern = rf'(?m)^{re.escape(st)}\n(.*?)$'
            matches = re.findall(pattern, pdf_content)
            for match in matches:
                output = f"{match[0]}, {match[1]} ({match[3]}) {match[2]}"
                filtered_rows.append(output)

        if st == "Fortum Solar, PAVAGADA":
            pattern = r"(Fortum Solar),\n(\d{4}-\d{2}-\d{2} \d+\.\d+ \d+\.\d+ \d+ \d+\.\d+ \d+\.\d+ \-\d+\.\d+ \-\d+\.\d+)\n(PAVAGADA)"
            matches = re.findall(pattern, pdf_content, re.DOTALL)
            for match in matches:
                output = f"{match[0]},{match[2]} {match[1]}"
                # print(output)
                filtered_rows.append(output)

    print("------> Rows fetched")
    return filtered_rows, WS_Seller


def create_file(DSM_Daywise_St_rows , WS_Seller):
    print("Saving data")
    WS_Seller_cols = ["Entity", "Over Injection Charges (Rs)", "Under Injecton Charges (Rs)",
        "Charges for Drawl without schedule (Rs)", "Final Charges (Rs)", "Payable To Pool/Receviable From Pool"]

    DSM_Daywise_St_cols = [ "Station details", "DATE", "Total Schedule (MWHr)",
            "Total Actual (MWHr)", "Total SRAS (MWHr)", "Total Deviation", "Total Overinjection Charges(Rs)", "Total Underinjection Charges (Rs)", "Drawl Charges (Rs)"]

    # print(DSM_Daywise_St_rows)
    DSM_Daywise_formatted_rows = []
    for row in DSM_Daywise_St_rows:
        # Find the index where the first digit occurs
        index = next((i for i, c in enumerate(row) if c.isdigit()), None)
        # Split the row based on the first digit
        if index is not None:
            col1 = row[:index].strip()  # Take the substring before the first digit
            rest_of_row = row[index:].split()  # Split the remaining part by space
            formatted_row = [col1] + rest_of_row
        else:
            formatted_row = [row]  # If no digit is found, consider the entire row as the first column
        DSM_Daywise_formatted_rows.append(formatted_row)
    
    df_DSM = []
    for line in DSM_Daywise_formatted_rows:
        df_DSM.append(line)
    DSM_Daywise_df = pd.DataFrame(df_DSM, columns=DSM_Daywise_St_cols)
    print(df_DSM)
    
    formatted_row = ""
    WS_Seller_df =  []
    WS_Seller_formatted_rows = []
    for row in WS_Seller:
        # Find the index where the first digit occurs
        index = next((i for i, c in enumerate(row) if c.isdigit()), None)
        # Split the row based on the first digit
        if index is not None:
            col1 = row[:index].strip()  # Take the substring before the first digit
            rest_of_row = row[index:].split()  # Split the remaining part by space
            formatted_row = [col1] + rest_of_row
        else:
            formatted_row = [row]  # If no digit is found, consider the entire row as the first column
        WS_Seller_formatted_rows.append(formatted_row)

    for line in WS_Seller_formatted_rows:
        WS_Seller_df.append(line)
    WS_Seller_df = pd.DataFrame(WS_Seller_df, columns=WS_Seller_cols)

    filename = f"Extracted Data_WRPC_SRPC_{datetime.now().strftime('%d-%m-%Y')}.xlsx"
    sheet_name = "SRPC_WA_DSM"

    # Check file existence
    if not os.path.exists(filename):
        wb = Workbook()
        wb.save(filename)
    else:
        wb = load_workbook(filename)

    # Check if sheet exists
    if sheet_name not in wb.sheetnames:
        wb.create_sheet(title=sheet_name)
    ws2 = wb[sheet_name]

    # # Write headers 
    DSM_Daywise_headers = DSM_Daywise_df.columns
    for col_num, header in enumerate(DSM_Daywise_headers, start=1):
        cell = ws2.cell(row=1, column=col_num, value=header)
        cell.font = Font(bold=True)

    # # Write Data
    for row_num, (_, row_data) in enumerate(DSM_Daywise_df.iterrows(), start=2):
      for col_num, value in enumerate(row_data, start=1):
          ws2.cell(row=row_num, column=col_num, value=value)
    
    ws2.append([])
    ws2.append([])

    # # # Write headers 
    fheaders = list(WS_Seller_cols)
    ws2.append(fheaders)

    # # Write Data
    for index, row in WS_Seller_df.iterrows():  # Iterate over DataFrame rows
        frow_list = row.to_list()  # Convert DataFrame row to a list
        ws2.append(frow_list)
    wb.save(filename)

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

    if st.button('Continue'):
        if selected_urls:
            # fetch_text(selected_urls)
            for url in selected_urls:
                with requests.get(url, verify=False) as response:
                    text = extract_text_from_pdf(response.content)
                    # print(text)
                    rows, WS_Seller = extract_rows_with_keywords(text,url)
            create_file(rows, WS_Seller)
            st.success("Extracted SRPC WA DSM✨")
            print("Extracted SRPC WA DSM✨")
        else:
            st.error("Please select at least one URL before continuing.")
