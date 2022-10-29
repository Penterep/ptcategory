class JSMetadata:
    def __init__(self, external_js: int, local_js: int, inline_js: int) -> None:
        self.external_js = external_js
        self.local_js = local_js
        self.inline_js = inline_js