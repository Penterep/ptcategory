from ast import parse
from urllib.parse import urlparse

from queryextraction.QueryMetadata import QueryMetadata

class QueryExtractor:
    
    def __init__(self, url: str) -> None:
        self.url = url
      
    # Returns query metadata
    def get_metadata(self) -> QueryMetadata:
        query_full = self.get_query()
        query_1, query_2, query_3, query_4, query_5 = self.get_q_parameters()
        return QueryMetadata(query_full, query_1, query_2, query_3, query_4, query_5)
    
    # Returns the query
    def get_query(self) -> str:
        parsed_query = urlparse(self.url).query
        return parsed_query if parsed_query != "" else "0"
    
    # Returns the first 5 query parameters
    def get_q_parameters(self) -> int:
        max_params = 5
        i = 0
        query = self.get_query()
        query_parameters = []
        split_query = query.split("&")
        while i < max_params:
            if len(query_parameters) < len(split_query) and split_query[i] != "0":
                query_parameters.append(hash(split_query[i]))
            else: 
                query_parameters.append(0)  
            i += 1
        return query_parameters[0:5]

    