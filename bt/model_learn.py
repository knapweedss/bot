# обучаем модель


import pandas as pd
with open('pr_text', encoding = 'UTF-8') as f:
    file = f.read()
    text = file.split('Продолжение →\',')  # уберем лишнее и поделим по новостям
with open('final_text.txt', encoding = 'UTF-8') as f:
    file = f.read()
    text2 = file.split('продолжение →')

# на всякий случай
if len(text) > len(text2) or len(text2) > len(text):
    text = text[0:240]
    text2 = text2[0:240]

df = pd.DataFrame({
    'inp_text' : text2,
    'vvod_text' : text
                  })
# обучение модели
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
vectorizer.fit(df.inp_text)

# большая матрица
matrix_1 = vectorizer.transform(df.inp_text)

# сжимаем матрицу, чтобы не перегружать сервер
from sklearn.decomposition import TruncatedSVD
svd = TruncatedSVD(n_components = 300)
svd.fit(matrix_1)

# оптимальный размнер матрицы
matrix_2 = svd.transform(matrix_1)

import numpy as np
from sklearn.neighbors import BallTree
from sklearn.base import BaseEstimator

# обучение
def softmax(x):
    ver = np.exp(-x)
    return ver/sum(ver)
class OccNeighbor(BaseEstimator):
    def __init__(self, k=3, temperature=1.0):  #три ближайших наиболее вероятных ответа
        self.k = k
        self.temperature = temperature
    def fit(self, X, y):
        self.tree_ = BallTree(X)
        self.y_ = np.array(y)
    def predict(self, X, random_state=None):
        distances, indices = self.tree_.query(X, return_distance=True, k=self.k)
        result = []
        for distance, index in zip(distances, indices):
            result.append(np.random.choice(index, p=softmax(distance * self.temperature)))
        return self.y_[result]
from sklearn.pipeline import make_pipeline
ng = OccNeighbor()
ng.fit(matrix_2, df.vvod_text)
pipe = make_pipeline(vectorizer, svd, ng)
