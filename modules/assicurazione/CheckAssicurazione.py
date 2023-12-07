from modules.assicurazione.DriverManager import DriverManager
from modules.assicurazione.PdfChecker import PdfChecker


class CheckAssicurazione:

    @staticmethod
    def is_da_scaricare():
        return not PdfChecker.exists() or not PdfChecker.is_assicurazione_valid()

    @staticmethod
    def download():
        if PdfChecker.exists():
            PdfChecker.delete_old_file()
        mgr = DriverManager()
        return mgr.get_assicurazione()
