from formextraction.FormsMetadata import FormsMetadata


class FormExtractor:
    def __init__(self, url: str) -> None:
        self.url = url
        
    def get_metadata(self) -> FormsMetadata:  #TODO: implement
        return FormsMetadata(0,0,0,0)