import streamlit as st
import os
import re
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from zipfile import ZipFile

def split_labels(file):
    reader = PdfReader(file)
    num_pages = len(reader.pages)
    
    # Folder name based on the input file name without extension
    folder_name = os.path.splitext(file.name)[0]
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    labels = {}
    for i in range(num_pages):
        page = reader.pages[i]
        text = page.extract_text()
        
        # Extract tracking number from the text
        match = re.search(r'\b\d{4} \d{4} \d{4}\b', text)
        if match:
            tracking_number = match.group(0).replace(" ", "")
            if tracking_number not in labels:
                labels[tracking_number] = []
            labels[tracking_number].append(i)

    for tracking_number, pages in labels.items():
        writer = PdfWriter()
        for page_num in pages:
            writer.add_page(reader.pages[page_num])
        
        label_path = os.path.join(folder_name, f"{tracking_number}.pdf")
        with open(label_path, 'wb') as label_file:
            writer.write(label_file)

    return folder_name

st.title("FedEx Ground Label Splitter")

uploaded_file = st.file_uploader("Upload a consolidated FedEx Ground Label PDF file", type=["pdf"])

if uploaded_file is not None:
    folder_name = split_labels(uploaded_file)
    st.success(f"Labels have been split and saved to the folder: {folder_name}")

    # Create a zip file of the folder
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for root, _, files in os.walk(folder_name):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, folder_name))

    zip_buffer.seek(0)

    st.download_button(
        label="Download All Labels as ZIP",
        data=zip_buffer,
        file_name=f"{folder_name}.zip",
        mime="application/zip"
    )
