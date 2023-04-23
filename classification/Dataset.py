from copy import deepcopy


class Dataset:
    def __init__(self, data: list[dict[str, any]], start_from_col: int) -> None:
        self._data = data
        self._dataset: list[list[int]] = None
        self._categories: list[str] = None
        self._start_from_col = start_from_col

    # Returns a copy of the dataset
    def get_copy(self) -> list[list[int]]:
        if not self._dataset:
            self._dataset = list(list(map(int, list(x.values())[self._start_from_col:])) for x in self._data)
        return deepcopy(self._dataset)

    # Returns a list of the categories
    def get_categories(self) -> list[str]:
        if not self._categories:
            self._categories = list(list(self._data[0].keys())[self._start_from_col:])
        return self._categories.copy()

    # Returns the number of columns
    def get_colums_len(self) -> int:
        return (len(self._data[0]) - self._start_from_col) + 1