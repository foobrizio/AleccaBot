import os.path
from datetime import datetime

from PyPDF2 import PdfReader

import Consts


class PdfChecker:

    @staticmethod
    def delete_old_file():
        os.remove(Consts.document)

    @staticmethod
    def exists():
        return os.path.exists(Consts.document)

    @staticmethod
    def is_assicurazione_valid():
        reader = PdfReader(Consts.document)
        page0 = reader.pages[0]
        expiry_date = PdfChecker.extract_expiry_date(page0.extract_text())
        return expiry_date.date() > datetime.now().date()

    @staticmethod
    def extract_expiry_date(text: str):
        subpart = text.split("Day Month Year Day Month Year", 1)[1]
        tokens = subpart.split()
        day = tokens[3]
        month = tokens[4]
        year = tokens[5]
        return datetime(int(year), int(month), int(day))