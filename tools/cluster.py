#coding=utf8


# KMeansCluster:
# train(vectors, k) -> (means, groups)


import numpy as np
import random


class KMeansCluster (object):
    """
    k-means 聚类
    """

    def __init__(self):
        """
        `distance`: 训练时所用的距离公式
        """
        self.weights = None

    def _dist(self, p1, p2):
        """
         计算两点距离平方和
        `p1`: 第一个点
        `p2`: 第二个点
        """
        p1 = np.array(p1)
        p2 = np.array(p2)
        return np.sum((p1 - p2) ** 2)

    def _getRandomPoint(self, dim):
        p = []
        for i in xrange(dim):
            p.append(8 * random.random())
        return p

    def _getRandomMeans(self, vectors, k):
        s = set()
        l = len(vectors)
        idx = 0
        means = []
        print 'generating random means...'
        while len(s) < k:
            idx = int(np.floor(l * random.random()))
            if idx in s: continue
            s.add(idx)
            means.append(vectors[idx])
        return means

    def _getMean(self, ps):
        """
        计算一批点的中心点
        `ps`: 点的集合
        """
        l = len(ps)
        fl = float(l)
        dim = len(ps[0])
        mean = []
        for j in xrange(dim):
            mean.append(0)
            for i in xrange(l):
                mean[j] += ps[i][j]
        for j in xrange(dim):
            mean[j] /= fl
        return mean

    def train(self, vectors, k=2, nInit=10, maxIter=1000, weights=None):
        """
        `vectors`: 点集
        `k`: 要分类的数目
        `nInit`: 以不同的初始化中心训练的次数
        `maxIter`: 最大迭代次数
        """
        self.weights = weights
        minMeans = []
        minGroups = []
        minError = float('inf')
        for n in range(nInit):
            means, groups, error = self._train(vectors, k, maxIter)
            print 'error with train', n, error
            if error < minError:
                minError = error
                minMeans = means
                minGroups = groups
        print 'minimum error:', minError
        return minMeans, minGroups

    def _train(self, vectors, k=2, maxIter=1000):
        """
        `vectors`: 点集
        `k`: 要分类的数目
        `maxIter`: 最大迭代次数
        """
        cp = len(vectors) # 点的总数
        dim = len(vectors[0]) # 点的维度
        means = self._getRandomMeans(vectors, k) # 随机生成means
        deltas = [] # 保存与上次means的差，若差值小的一定范围，则停止迭代

        for m in xrange(k):
            deltas.append(0)

        dists = [] # 临时保存距离
        groups = [] # 临时保存分类的点

        for i in xrange(maxIter):
            # assign step
            groups = [] # 清空
            dists = []

            for m in xrange(k):
                groups.append([])
                dists.append(0)

            for p in xrange(cp):
                for m in xrange(k):
                    dists[m] = self._dist(vectors[p], means[m])
                    if self.weights != None: dists[m] *= self.weights[p]
                idx = dists.index(min(dists))
                groups[idx].append(vectors[p])
            # update means
            for m in xrange(k):
                deltas[m] = means[m]
                means[m] = self._getMean(groups[m])
                deltas[m] = sum(np.abs(np.array(deltas[m]) - np.array(means[m])))
            if sum(deltas) < 1e-100: break
        error = self._computeError(means, groups)
        return means, groups, error

    def _computeError(self, means, groups):
        error = 0
        npmean = []
        for k in xrange(len(means)):
            npmean = np.array(means[k])
            for p in groups[k]:
                error += np.sqrt(sum((np.array(p) - npmean) ** 2))
        return error
