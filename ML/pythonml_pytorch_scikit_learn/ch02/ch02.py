import numpy as np


class Perceptron:
    """Perception classifier.
    Parameters
    ----------
    eta : float
        Learning rate (between 0.0 and 1.0)
    n_iter : int
        Passes over the training dataset.
    random_state : int
        Random number generator seed for random weight initialization.
    Attributes
    ----------
    w_ : 1d-array
        Weights after fitting.
    b_ : float
        Bias after fitting.
    errors_ : list
        Number of misclassifications in every epoch.
    """

    def __init__(self, eta=0.01, n_iter=50, random_state=1):
        self.eta = eta
        self.n_iter = n_iter
        self.random_state = random_state

    def fit(self, X, y):
        """Fit training data.
        Parameters
        ----------
        X:{array-like},shape=[n_examples,n_features]
            Training vectors,where n_examples is the number of examples and n_features is the number of features.
        y:array-like,shape=[n_examples]
            Target values.
        Returns
        -------
        self:object
        """
        rgen = np.random.RandomState(
            self.random_state
        )  # 创建随机数生成器实例，self.random_state是seed
        # numpy.random.RandomState 对象的 normal 方法。
        # 该方法用于生成服从正态（高斯）分布的随机数。
        # loc：均值；scale：标准差；size：生成随机数的数量
        self.w_ = rgen.normal(
            loc=0.0, scale=0.01, size=X.shape[1]
        )  # shape[1]是列数，shape[0]是行数,生成权重w和x匹配
        self.b_ = np.float_(0.0)  # 创建一个浮点型数值
        self.errors_ = []

        for _ in range(self.n_iter):  # 迭代n.iter次
            errors = 0
            for xi, target in zip(
                X, y
            ):  # zip()函数用于将可迭代的对象作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表
                update = self.eta * (target - self.predict(xi))
                self.w_ += update * xi
                self.b_ += update
                errors += int(update != 0.0)
                print(xi)
                print(self.predict(xi))
                print(target)
                print(self.w_)
                print(update)

            self.errors_.append(errors)
        return self

    def net_input(self, X):
        """Calculate net input"""
        return np.dot(X, self.w_) + self.b_

    def predict(self, X):
        """Return class label after unit step"""
        return np.where(self.net_input(X) >= 0.0, 1, 0)


import os
import pandas as pd

try:
    s = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"
    # print('From URL:', s)
    df = pd.read_csv(s, header=None, encoding="utf-8")

except HTTPError:
    s = "iris.data"
    print("From local Iris path:", s)
    df = pd.read_csv(s, header=None, encoding="utf-8")


import matplotlib.pyplot as plt
import numpy as np

# select setosa and versicolor
y = df.iloc[0:100, 4].values
y = np.where(y == "Iris-setosa", 0, 1)  # 提取标签并进行转化

# extract sepal length and petal length
X = df.iloc[0:100, [0, 2]].values  # 提取第一个特征列和第三个特征列

ppn = Perceptron(eta=0.01, n_iter=10)
ppn.fit(X, y)
