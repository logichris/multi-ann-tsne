from openTSNE.nearest_neighbors import KNNIndex

import nmslib
import os
import numpy as np

class BruteForce(KNNIndex):
    #VALID_METRICS = neighbors.Nmslib.valid_metrics

    def build(self, data):
        n_items, vector_length = data.shape
        self._method_name = "brute_force"
        self._metric = {
        'angular': 'cosinesimil', 'euclidean': 'l2'}[self.metric]

        self.index = nmslib.init(
            space=self._metric, method=self._method_name, data_type=nmslib.DataType.DENSE_VECTOR, dtype=nmslib.DistType.FLOAT)

        self.index.addDataPointBatch(data)
        self.index.createIndex()

    def query_train(self, data, k):
        result = np.asarray(self.index.knnQueryBatch(data, k))
        neighbors = np.empty((data.shape[0],k), dtype=int)
        distances = np.empty((data.shape[0],k))
        for i in range(len(data)):
            neighbors[i] = result[i][0]
            distances[i] = result[i][1]
        return neighbors, distances

    def query(self, query, k):
        result = np.asarray(self.index.knnQueryBatch(query, k))
        neighbors = np.empty((query.shape[0],k), dtype=int)
        distances = np.empty((query.shape[0],k))
        for i in range(len(query)):
            neighbors[i] = result[i][0]
            distances[i] = result[i][1]
        return neighbors, distances
