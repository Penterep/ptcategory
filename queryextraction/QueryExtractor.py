from email.mime import base
from urllib.parse import urlparse

from QueryMetadata import QueryMetadata

class QueryExtractor:
    
    def __init__(self, url: str) -> None:
        self.url = url
      
    def get_metadata(self) -> QueryMetadata:
        query_full = self.get_query()
        #print(query_full)
        query_1, query_2, query_3, query_4, query_5 = self.get_q_parameters()
        return QueryMetadata(query_full, query_1, query_2, query_3, query_4, query_5)
    
    def get_query(self) -> str:
        return urlparse(self.url).query
    
    def get_q_parameters(self) -> int:
        query = self.get_query()
        query_parameters = []
        
        split_query = query.split("&")
        
        for i in split_query:
            for j in range(1, len(split_query)):
                query_parameters[j] = int(str(hash(i)), 16)
    
        return query_parameters[0:4]

""""
query = QueryExtractor("https://www.midgard.cz/?lang=en&page=shop")
x = query.get_metadata()
print(x.query_1)
"""    