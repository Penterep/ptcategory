import csv
from UnknownCsvHeadersError import UnknownCsvHeadersError

from formextraction.FormExtractor import FormExtractor
from jsextraction.JSExtractor import JSExtractor

class CsvProvider:
    DELIMITER = ","
    ENCODING = "utf-8"

    def __init__(self, csv_file_path: str) -> None:
        self.csv_file_path = csv_file_path
        with open(csv_file_path, encoding=self.ENCODING) as csv_file:
            self.rows_dict = list(csv.DictReader(csv_file, delimiter=self.DELIMITER))

    def save_file(self) -> None:
        with open(self.csv_file_path, "w", encoding=self.ENCODING, newline="") as csv_file:
            if len(self.rows_dict) > 0:
                writer = csv.DictWriter(csv_file, fieldnames=self.rows_dict[0].keys(), delimiter=self.DELIMITER)
                writer.writeheader()
                writer.writerows(self.rows_dict)
            else:
                raise UnknownCsvHeadersError("Cannot figure out headers of the csv file, because csv file does not have any rows.")

    def extract_forms(self) -> None:
        for row in self.rows_dict:
            form_extractor = FormExtractor(url=row["URL"])
            metadata = form_extractor.get_metadata()
            row["HTML form"] = metadata.html_form
            row["Login form"] = metadata.login_form
            row["Upload input"] = metadata.upload_input
            row["Download button"] = metadata.download_button
            row["User input"] = metadata.user_input
            row["Registration form"] = metadata.registration_form

    def extract_javascript(self) -> None:
        for row in self.rows_dict:
            js_extractor = JSExtractor(url=row["URL"])
            metadata = js_extractor.get_metadata()
            row["Local JavaScript"] = metadata.local_js
            row["External JavaScript"] = metadata.external_js
            row["Inline JavaScript"] = metadata.inline_js