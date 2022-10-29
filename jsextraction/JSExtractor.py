from bs4 import BeautifulSoup, ResultSet
import requests
import os
import re

from RequestCache import RequestCache
from jsextraction.JSMetadata import JSMetadata
from jsextraction.JSEvents import JSEvents


class JSExtractor:
    METHOD = "GET"
    PARSER = "lxml"
    
    def __init__(self, url: str) -> None:
        self.domain_name = find_domain_name(url)
        self.response: requests.Request = RequestCache.request(self.METHOD, url)
        self.soup = BeautifulSoup(self.response.text, self.PARSER)
        self.events = JSEvents()
        
    def get_metadata(self) -> JSMetadata:
        external_js, local_js = self._parse_scripts()
        inline_js = self._get_inline_js()
        return JSMetadata(external_js, local_js, inline_js)
    
    def _parse_scripts(self) -> int:
        scripts = self._get_scripts()
        external_js = 0
        local_js = 0
        for script in scripts:
            if script.has_attr("src"):
                src = script.attrs["src"]
                if not os.path.isabs(src) and \
                        self.domain_name not in src:
                    external_js += 1
                    continue
            local_js += 1
        return external_js, local_js

    def _get_inline_js(self) -> int:
        return len(self.soup.select(self.events.get_select_format()))

    def _get_scripts(self) -> ResultSet:
        return self.soup.find_all("script")


def find_domain_name(url: str) -> str:
    pattern = re.compile('(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,10}[a-z0-9]')
    return pattern.search(url).group()