from django.db import models

# Create your models here.
class Calculations:
    
    @staticmethod
    def mean(data):
        return sum(data) / len(data)
    @staticmethod
    def median(data):
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]
    @staticmethod
    def mode(data):
        from collections import Counter
        data_count = Counter(data)
        mode_data = data_count.most_common()
        max_count = mode_data[0][1]
        modes = [num for num, count in mode_data if count == max_count]
        return modes
    @staticmethod
    def add(x, y):
        return float(x) + float(y)
    @staticmethod
    def subtract(x, y):
        return float(x) - float(y)
    @staticmethod
    def multiply(x, y):
        return float(x) * float(y)
    @staticmethod
    def divide(x, y):
        return float(x) / float(y)
    

class IndexCalculations:
    @staticmethod    
    def ageing_idx(first_ec_gen, second_ec_gen):
        age_idx =first_ec_gen / second_ec_gen
        return age_idx
    @staticmethod
    def sauvy_idx(first_bg_gen, second_bg_gen):
        sau_idx =first_bg_gen / second_bg_gen
        return sau_idx
    @staticmethod
    def ec_weight_idx(first_ec_gen, second_ec_gen, third_ec_gen):
        ecw_idx = ((first_ec_gen + second_ec_gen + third_ec_gen) / second_ec_gen)*100
        return ecw_idx
    @staticmethod
    def dependency_idx(first_ec_gen, second_ec_gen):
        di = (first_ec_gen / second_ec_gen) * 100
        return di
    
    @staticmethod
    def shadow_idx(third_ec_gen, second_ec_gen):
        sh_idx = (third_ec_gen /second_ec_gen) * 100
        return sh_idx

#class ClusterCalculations:
#    def __init__(self, data):
#        self.data = data
#
#    def k_means(self, k):
#        from sklearn.cluster import KMeans
#        kmeans = KMeans(n_clusters=k)
#        kmeans.fit(self.data)
#        return kmeans.labels_, kmeans.cluster_centers_
#    def hierarchical_clustering(self):
#        from scipy.cluster.hierarchy import dendrogram, linkage
#        linked = linkage(self.data, 'ward')
#        return linked
    

