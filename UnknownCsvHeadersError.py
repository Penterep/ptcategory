from msilib.schema import Error


class UnknownCsvHeadersError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)