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
from constants import thesisIDspath

thesisids = pd.read_excel(thesisIDspath)

print(thesisids.head())