class CssMetadata:
    def __init__(self, local_css: int, external_css: int, block_css: int) -> None:
        self.external_css = external_css
        self.local_css = local_css
        self.block_css = block_css