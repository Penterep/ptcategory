import requests

class RequestIdentifier:
    def __init__(self, method: str, url: str) -> None:
        self.method = method
        self.url = url
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RequestIdentifier):
            return False
        
        return self.method == other.method and self.url == other.url
    
    def __hash__(self) -> int:
        return hash(self.method) + hash(self.url)
    
    def __str__(self) -> str:
        return f"{self.method}: {self.url}"
    
    def __repr__(self) -> str:
        return self.__str__()

class RequestCache:
    cache : dict[RequestIdentifier, requests.Response] = {}
        
    @classmethod
    def request(cls, method: str, url: str) -> requests.Response:
        identifier = RequestIdentifier(method=method, url=url)
        if identifier in cls.cache.keys():
            return cls.cache[identifier]
        else:
            response = requests.request(method, url)
            cls.cache[identifier] = response
            return response
        
