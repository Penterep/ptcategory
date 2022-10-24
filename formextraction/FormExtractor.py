from RequestCache import RequestCache
from formextraction.FormsMetadata import FormsMetadata
import requests
from bs4 import BeautifulSoup,ResultSet

from formextraction.HrefAttribute import HrefAttribute

class FormExtractor:
    METHOD = "GET"
    PARSER = "html.parser"
    
    def __init__(self, url: str) -> None:
        self.url = url
        self.response: requests.Response = RequestCache.request(self.METHOD, url) #TODO: test if fails
        self.soup = BeautifulSoup(self.response.text, self.PARSER)
        
    def get_metadata(self) -> FormsMetadata:
        html_form = self.get_html_form()
        login_form = self.get_login_form()
        upload_input = self.get_upload_input()
        download_button = self.get_download_button()
        return FormsMetadata(html_form, login_form, upload_input, download_button)
    
    def get_html_form(self) -> int:
        forms = self.get_forms()
        return len(forms)
    
    def get_login_form(self) -> int:
        forms = self.get_forms()
        login_forms = 0
        for form in forms:
            password_inputs = form.select("input[type=password]")
            if len(password_inputs) > 0:
                login_forms += 1
        return login_forms
        
    def get_forms(self) -> ResultSet:
        return self.soup.find_all("form")
    
    def get_upload_input(self) -> int:
        return len(self.soup.select("input[type=upload]"))
    
    def get_download_button(self) -> int:
        download_buttons = 0
        anchor_tags = self.soup.select("a[href],a[download]")
        for anchor_tag in anchor_tags:
            if anchor_tag.has_attr("download"):
                download_buttons += 1
            elif anchor_tag.has_attr("href"):
                if HrefAttribute(anchor_tag.attrs["href"]).is_file_href():
                    download_buttons += 1
        return download_buttons
    