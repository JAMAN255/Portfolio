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
    




