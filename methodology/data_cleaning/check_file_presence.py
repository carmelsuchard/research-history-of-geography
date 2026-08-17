"""
Purpose: Check the thesisID excel file. Ensure that all text and PDF files are present in the specified directory.
Also check the opposite, that all files are listed in the excel file.
Creator: Carmel
Date: 2026-08-15
"""

import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from constants import *

thesisids = pd.read_csv(thesisIDspath, dtype={"thesisID": str, "text_file": str, "pdf_file": str, "Language":str, "Annotated": bool})
# Check duplicates in any of the columns
duplicates = thesisids[thesisids.duplicated(subset=['thesisID', 'text_file', 'pdf_file'], keep=False)]
if not duplicates.empty:
    print("Duplicates found in thesisID excel file:")
    print(duplicates)
    exit(1)

# Check files presence
for index, row in thesisids.iterrows():
    thesis_id = row['thesisID']
    language = row['Language']
    text_file = row['text_file']
    pdf_file = row['pdf_file']

    if text_file:
        text_file_path = os.path.join(text_files_dir, language, str(text_file))
        if not os.path.exists(text_file_path):
            print(f"Text file missing for thesisID: {thesis_id}, {text_file}")

    if pdf_file:
        pdf_file_path = os.path.join(pdf_files_dir, language, str(pdf_file))
        if not os.path.exists(pdf_file_path):
            print(f"PDF file missing for thesisID: {thesis_id}, {pdf_file}")


# Check if missed any of the files in the archive
english_files = thesisids[thesisids["Language"] == "English"]["text_file"].tolist()
for text_file in os.listdir(os.path.join(text_files_dir, "English")):
    if not text_file in english_files:
        print(f"Text file not found in CSV: {text_file}")

english_files = thesisids[thesisids["Language"] == "English"]["pdf_file"].tolist()
for pdf_file in os.listdir(os.path.join(pdf_files_dir, "English")):
    if not pdf_file in english_files:
        print(f"PDF file not found in CSV: {pdf_file}")

dutch_files = thesisids[thesisids["Language"] == "Dutch"]["text_file"].tolist()
for text_file in os.listdir(os.path.join(text_files_dir, "Dutch")):
    if not text_file in dutch_files:
        print(f"Text file not found in CSV: {text_file}")

dutch_files = thesisids[thesisids["Language"] == "Dutch"]["pdf_file"].tolist()
for pdf_file in os.listdir(os.path.join(pdf_files_dir, "Dutch")):
    if not pdf_file in dutch_files:
        print(f"PDF file not found in CSV: {pdf_file}")


# Order by text_file, and give new thesisIDs
thesisids = thesisids.sort_values(by=['text_file']).reset_index(drop=True)
thesisids["thesisID"] = thesisids.index + 1

thesisids = thesisids[["thesisID", "text_file", "pdf_file", "Language", "Annotated"]]
# Check duplicates in any of the columns

thesisids.to_csv(thesisIDspath, index= False)