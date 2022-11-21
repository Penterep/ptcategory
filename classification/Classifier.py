import pandas as pd
from matplotlib import pyplot
from numpy import unique, where
from sklearn.cluster import OPTICS, MeanShift, SpectralClustering, KMeans, MiniBatchKMeans
from numpy import unique, where, sort, arange
from sklearn.cluster import OPTICS, MeanShift, SpectralClustering, DBSCAN, Birch
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator

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

    def spectral_clustering(self) -> None:
        model = SpectralClustering(n_clusters=4, affinity="rbf")
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Spectral clustering")

    def gaussian_mixture(self) -> None:
        model = GaussianMixture(n_components=3)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Gaussian mixture")

    def kmeans(self, init: str  = "k-means++", max_iter: int = 300, init_clusters: int = 10) -> None:
        model = KMeans(init=init, max_iter=max_iter, n_init=init_clusters)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "K-means")
    
    def kmeans_mini_batch(self, init: str = "k-means++", max_iter: int = 300, init_clusters: int = 10, batch_size: int = 2048) -> None:
        model = MiniBatchKMeans(init=init, max_iter=max_iter, n_init=init_clusters, batch_size=batch_size)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "K-means mini batch")
        
    def dbscan(self) -> None:
        dataset_copy = self.dataset.get_copy()
        min_pts = self.dataset.get_colums_len()
        
        neighbors = NearestNeighbors(n_neighbors=min_pts).fit(dataset_copy)
        distances, _ = neighbors.kneighbors(dataset_copy)
        distances = sort(distances, axis=0)[:,min_pts-1]
        i = arange(len(distances))
        
        knee = KneeLocator(i, distances, curve="convex")
        eps = float(f"{distances[knee.knee]:.1f}")

        model = DBSCAN(eps=eps, min_samples=min_pts)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "DBSCAN")

    def birch(self, branching_factor: int=50, n_clusters: int=None, threshold: float=0.1) -> None:
        model = Birch(branching_factor=branching_factor, n_clusters=n_clusters, threshold=threshold)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Birch")

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
