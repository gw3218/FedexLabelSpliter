#!/usr/bin/env python
# coding: utf-8

# In[3]:


import os
import re
import PyPDF2
import streamlit as st

def extract_tracking_number(text):
    """
    Extracts the tracking number from the given text.
    Assumes that the tracking number is in the format "1234 5678 9012".
    """
    match = re.search(r'\b\d{4} \d{4} \d{4}\b', text)
    if match:
        return match.group(0).replace(' ', '')  # Remove spaces for the filename
    return None

def split_pdf(file, output_dir):
    pdf_reader = PyPDF2.PdfReader(file)
    total_pages = len(pdf_reader.pages)

    for page_num in range(total_pages):
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        tracking_number = extract_tracking_number(text)

        if tracking_number:
            pdf_writer = PyPDF2.PdfWriter()
            pdf_writer.add_page(page)
            output_filename = os.path.join(output_dir, f"{tracking_number}.pdf")
            with open(output_filename, 'wb') as output_pdf:
                pdf_writer.write(output_pdf)
            st.write(f"Saved: {output_filename}")
        else:
            st.warning(f"No tracking number found on page {page_num + 1}")

st.title("FedEx Ground Label Splitter")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Splitting PDF..."):
        base_name = os.path.basename(uploaded_file.name)
        output_dir = os.path.splitext(base_name)[0]
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        split_pdf(uploaded_file, output_dir)
        st.success("PDF splitting completed!")

        # Provide a download link for the folder
        st.write(f"Download split labels from the folder: {output_dir}")

st.caption("Upload a consolidated FedEx Ground Label PDF file. The tool will split the file into individual labels using the tracking number as the name for each file and save them in a folder with the same name as the input file.")


# In[ ]:




