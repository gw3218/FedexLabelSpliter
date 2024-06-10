import streamlit as st
import os
import re
from io import BytesIO
from zipfile import ZipFile

def split_labels(file):
    # Create a folder with the same name as the input file (without extension)
    folder_name = os.path.splitext(file.name)[0]
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    content = file.read().decode('utf-8')
    labels = re.split(r'(?:\n|^)(\d{4} \d{4} \d{4})(?:\n|$)', content)

    for i in range(1, len(labels), 2):
        tracking_number = labels[i].replace(" ", "")
        label_content = labels[i + 1].strip()
        with open(os.path.join(folder_name, f"{tracking_number}.txt"), 'w') as label_file:
            label_file.write(f"{tracking_number}\n{label_content}")

    return folder_name

st.title("FedEx Ground Label Splitter")

uploaded_file = st.file_uploader("Upload a consolidated FedEx Ground Label file", type=["txt"])

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
