from bs4 import BeautifulSoup, ResultSet
from tldextract import tldextract
import os
import requests

from RequestCache import RequestCache
from cssextraction.CssMetadata import CssMetadata


class CssExtractor:
    METHOD = "GET"
    PARSER = "lxml"
    
    def __init__(self, url: str) -> None:
        self.domain_name = self._extract_domain(url)
        self.response: requests.Request = RequestCache.request(self.METHOD, url)
        self.soup = BeautifulSoup(self.response.text, self.PARSER)
    
    def get_metadata(self) -> CssMetadata:
        external_css, local_css = self._parse_link()
        block_css = self._get_block_css()
        return CssMetadata(local_css, external_css, block_css)
    
    def _parse_link(self) -> int:
        links = self._get_link()
        external_css = 0
        local_css = 0
        for link in links:
            if link.has_attr("href") or link.has_attr("data-href"):
                src = link["href"] if link.has_attr("href") else link["data-href"]
                if self._is_external_css(src):
                    external_css += 1
                    continue
            local_css += 1
        return external_css, local_css

    def _is_external_css(self, src: str) -> bool:
        if src.startswith("//"):
            src = src.lstrip("//")
        if "cdn" in src or "unpkg" in src or \
                not os.path.isabs(src) and self.domain_name not in src:
            return True
        return False
    
    def _get_block_css(self) -> int:
        return len(self.soup.find_all("style"))
    
    def _get_link(self) -> ResultSet:
        return self.soup.find_all("link")
    
    def _extract_domain(self, url: str) -> str:
        ext = tldextract.extract(url)
        return f"{ext.domain}.{ext.suffix}"