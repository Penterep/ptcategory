import pandas as pd
from matplotlib import pyplot
from numpy import arange, sort, unique, where
from sklearn.cluster import OPTICS, MeanShift, SpectralClustering, KMeans, MiniBatchKMeans, DBSCAN, Birch, AffinityPropagation, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors
from kneed import KneeLocator

from classification.Dataset import Dataset


class Clustering:
    COLORS = ("#00ced1", "#ffa500", "#00ff00", "#0000ff", "#ff1493")
    CLUSTER_COLUMN_NAME = "cluster"

    def __init__(self, dataset: Dataset) -> None:
        self.dataset = dataset

    # Mean Shift clustering algorithm
    def mean_shift(self) -> pd.DataFrame:
        model = MeanShift()
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Mean shift")
        return df

    # OPTICS clustering algorithm
    def optics(self) -> None:
        model = OPTICS(eps=0.3, min_samples=5)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "OPTICS")

    # Spectral clustering algorithm
    def spectral_clustering(self) -> None:
        model = SpectralClustering(n_clusters=4, affinity="rbf")
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Spectral clustering")

    # Gaussian mixture clustering algorithm
    def gaussian_mixture(self) -> None:
        print('test')
        model = GaussianMixture(n_components=3)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Gaussian mixture")

    # K-means clustering algorithm
    def kmeans(self, init: str  = "k-means++", max_iter: int = 300, init_clusters: int = 10) -> None:
        model = KMeans(init=init, max_iter=max_iter, n_init=init_clusters)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "K-means")
    
    # Mini batch K-means clustering algorithm
    def kmeans_mini_batch(self, init: str = "k-means++", max_iter: int = 300, init_clusters: int = 10, batch_size: int = 2048) -> None:
        model = MiniBatchKMeans(init=init, max_iter=max_iter, n_init=init_clusters, batch_size=batch_size)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "K-means mini batch")
        
    # DBSCAN clustering algorithm
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
    
    # BIRCH clustering algorithm
    def birch(self, branching_factor: int=50, n_clusters: int=None, threshold: float=0.1) -> None:
        model = Birch(branching_factor=branching_factor, n_clusters=n_clusters, threshold=threshold)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Birch")

    # Affinity Propagation clustering algorithm
    def affinity_propagation(self) -> None:
        model = AffinityPropagation(max_iter=1, damping=0.9)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Affinity propagation")
            
    # Agglomerative Clustering algorithm
    def agglomerative_clustering(self) -> None:
        model = AgglomerativeClustering(n_clusters=None, distance_threshold=0.1, compute_distances=True)
        df = self._get_clustered_dataframe(model)
        self._display_parallel_coordinates(df, "Agglomerative Clustering")

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

        return self._get_dataframe(dataset_copy)
    
    # Machine-processed clustering
    def manual_clustering(self) -> pd.DataFrame:
        dataset_copy = self.dataset.get_copy()
        group_indexes: dict[tuple, str] = {}
        last_group_index = 1
        for row_index, dataset_row in enumerate(dataset_copy):
            group_key = tuple(dataset_row)
            if group_key in group_indexes:
                dataset_copy[row_index].append(group_indexes[group_key])
            else:
                group_index = "Cluster " + str(last_group_index)
                group_indexes[group_key] = group_index
                dataset_copy[row_index].append(group_index)
                last_group_index += 1
        df = self._get_dataframe(dataset_copy)
        self._display_parallel_coordinates(df, "Manual clustering")
        return df
    
    # Returns a dataframe with the clustering column
    def _get_dataframe(self, dataset: list[list[int]]) -> pd.DataFrame:
        categories = self.dataset.get_categories()
        categories.append(self.CLUSTER_COLUMN_NAME)
        return pd.DataFrame(dataset, columns=categories)
    
    # Displays the parallel coordinates of the dataframe
    def _display_parallel_coordinates(self, data_frame: pd.DataFrame, figure_name: str) -> None:
        self._print_cluster_stats(data_frame)
        f = pyplot.figure(figure_name)
        pd.plotting.parallel_coordinates(data_frame, self.CLUSTER_COLUMN_NAME, color=self.COLORS)
        f.show()
        
    def _print_cluster_stats(self, df):
        cluster_counts = df['cluster'].value_counts().sort_index()
        print("Number of items in each cluster:")
        print(cluster_counts)
        
        cluster_means = df.groupby('cluster').mean()
        print("Average values for each cluster:")
        print(cluster_means)