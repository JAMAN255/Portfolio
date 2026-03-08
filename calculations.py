class Calculations:
    def __init__(self, data):
        self.data = data

    def mean(self):
        return sum(self.data) / len(self.data)

    def median(self):
        sorted_data = sorted(self.data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        else:
            return sorted_data[mid]

    def mode(self):
        from collections import Counter
        data_count = Counter(self.data)
        mode_data = data_count.most_common()
        max_count = mode_data[0][1]
        modes = [num for num, count in mode_data if count == max_count]
        return modes

class IndexCalculations:
    def __init__(self, first_ec_gen, second_ec_gen, third_ec_gen, first_bg_gen, second_bg_gen, third_bg_gen):
        self.first_ec_gen = first_ec_gen
        self.second_ec_gen = second_ec_gen
        self.third_ec_gen = third_ec_gen
        self.first_bg_gen = first_bg_gen
        self.second_bg_gen = second_bg_gen
        self.third_bg_gen = third_bg_gen
        
    def ageing_idx(self):
        age_idx =self.first_ec_gen / self.second_ec_gen
        return age_idx
    
    def sauvy_idx(self):
        sau_idx =self.first_bg_gen / self.second_bg_gen
        return sau_idx
    def ec_weight_idx(self):
        ecw_idx = ((self.first_ec_gen + self.second_ec_gen + self.self.third_ec_gen) / self.second_ec_gen)*100
        return ecw_idx
    
    def dependency_idx(self):
        di = (self.first_ec_gen / self.second_ec_gen) * 100
        return di
    
    def shadow_idx(self):
        sh_idx = (self.third_ec_gen /self.second_ec_gen) * 100
        return sh_idx

class ClusterCalculations:
    def __init__(self, data):
        self.data = data

    def k_means(self, k):
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(self.data)
        return kmeans.labels_, kmeans.cluster_centers_
    