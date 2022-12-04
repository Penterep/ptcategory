import csv
from UnknownCsvHeadersError import UnknownCsvHeadersError

from formextraction.FormExtractor import FormExtractor
from jsextraction.JSExtractor import JSExtractor
from cssextraction.CssExtractor import CssExtractor
from queryextraction.QueryExtractor import QueryExtractor
from progbar.PgBar import PgBar

class CsvProvider:
    DELIMITER = ","
    ENCODING = "utf-8"
    
    def __init__(self, csv_file_path: str) -> None:
        self.csv_file_path = csv_file_path
        with open(csv_file_path, encoding=self.ENCODING) as csv_file:
            self.rows_dict = list(csv.DictReader(csv_file, delimiter=self.DELIMITER))
        self.p = PgBar(max_value=len(self.rows_dict)*4)
        
            
    def save_file(self) -> None:
        with open(self.csv_file_path, "w", encoding=self.ENCODING, newline="") as csv_file:
            if len(self.rows_dict) > 0:
                writer = csv.DictWriter(csv_file, fieldnames=self.rows_dict[0].keys(), delimiter=self.DELIMITER)
                writer.writeheader()
                writer.writerows(self.rows_dict)
            else:
                raise UnknownCsvHeadersError("Cannot figure out headers of the csv file, because csv file does not have any rows.")
    
    def extract_forms(self) -> None:
        self.p.set_desc("Extracting forms")
        for row in self.rows_dict:
            self.p.update(1)
            form_extractor = FormExtractor(url=row["URL"])
            metadata = form_extractor.get_metadata()
            row["HTML form"] = metadata.html_form
            row["Login form"] = metadata.login_form
            row["Upload input"] = metadata.upload_input
            row["Download button"] = metadata.download_button
            row["User input"] = metadata.user_input
            row["Registration form"] = metadata.registration_form
                              
    def extract_javascript(self) -> None:
        self.p.set_desc("Extracting JS")
        for row in self.rows_dict:
            self.p.update(1)
            js_extractor = JSExtractor(url=row["URL"])
            metadata = js_extractor.get_metadata()
            row["Local JavaScript"] = metadata.local_js
            row["External JavaScript"] = metadata.external_js
            row["Inline JavaScript"] = metadata.inline_js
            
    def extract_css(self) -> None:
        self.p.set_desc("Extracting CSS")
        for row in self.rows_dict:
            self.p.update(1)
            css_extractor = CssExtractor(url=row["URL"])
            metadata = css_extractor.get_metadata()
            row["Local CSS"] = metadata.local_css
            row["External CSS"] = metadata.external_css
            row["Block CSS"] = metadata.block_css

    def extract_query(self) -> None:
        self.p.set_desc("Extracting query")
        for row in self.rows_dict:
            self.p.update(1)
            query_extractor = QueryExtractor(url=row["URL"])
            metadata = query_extractor.get_metadata()
            row["Query params"] = metadata.query_full
            row["Query param 1"] = metadata.query_1
            row["Query param 2"] = metadata.query_2
            row["Query param 3"] = metadata.query_3
            row["Query param 4"] = metadata.query_4
            row["Query param 5"] = metadata.query_5
        self.p.set_desc("Extraction done")
        self.p.close()