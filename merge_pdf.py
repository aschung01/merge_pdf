import os
import argparse
import pypdf
from typing import List
from pathlib import Path
import streamlit as st


def merge_pdfs(files: List[Path], output: Path) -> None:
    try:
        merger = pypdf.PdfWriter()
        for path in files:
            merger.append(path)
        merger.write(output)
        print("Successfully merged PDFs")
        print(f"Output: {output}")
    except Exception as error:
        print(error)


uploaded_files = st.file_uploader(
    "Upload PDF files", type="pdf", accept_multiple_files=True
)


if uploaded_files:
    file_names = [file.name for file in uploaded_files]

    # Let the user reorder the list of files
    reordered_file_names = st.multiselect(
        "Reorder the files as needed (select in the desired merge order):",
        file_names,
        default=None,
    )

    if len(reordered_file_names) != len(file_names):
        st.warning(
            f"Please select {len(file_names)} files to reorder.\
                Currently, you have selected {len(reordered_file_names)}."
        )
    else:
        # Update the order of uploaded_files based on reordered_file_names
        ordered_files = sorted(
            uploaded_files, key=lambda x: reordered_file_names.index(x.name)
        )

    output_path = st.text_input(
        "Enter output file path and name:", value=f"{os.getcwd()}/merged.pdf"
    )

    if st.button("Merge PDFs"):
        merge_pdfs(ordered_files, output_path)
        st.success(
            f"PDFs merged successfully!\
                You can find the merged file at: {output_path}"
        )
