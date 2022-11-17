from copy import deepcopy

import pandas as pd
from matplotlib import pyplot
from numpy import unique, where
from sklearn.cluster import OPTICS, MeanShift

from classification.Dataset import Dataset


class Classifier:
    COLORS = ("#00ced1", "#ffa500", "#00ff00", "#0000ff", "#ff1493")
    CLUSTER_COLUMN_NAME = "cluster"
    
    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset
    
    def mean_shift(self) -> None:
        model = MeanShift()
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Mean shift")
        
    def optics(self) -> None:
        model = OPTICS(eps=0.3, min_samples=5)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "OPTICS")
        
    def _get_clustered_dataframe(self, model) -> pd.DataFrame:
        dataset_copy = self.dataset.get_copy()
        yhat = model.fit_predict(dataset_copy)
        clusters = unique(yhat)
        
        i = 1
        for cluster in clusters:
            row_indexes = where(yhat == cluster)[0]
            for r_i in row_indexes:
                dataset_copy[r_i].append("Cluster " + str(i))
            i += 1
        
        categories = self.dataset.get_categories()
        categories.append(self.CLUSTER_COLUMN_NAME)
        return pd.DataFrame(dataset_copy, columns=categories)
        
    def _display_parallel_coordinates(self, data_frame: pd.DataFrame, figure_name: str) -> None:
        f = pyplot.figure(figure_name)
        pd.plotting.parallel_coordinates(data_frame, self.CLUSTER_COLUMN_NAME, color=self.COLORS)
        f.show()
    
    