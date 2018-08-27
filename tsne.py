from matplotlib.pyplot import figure, subplot, scatter, show
from sklearn.datasets import load_iris
from sklearn.manifold import TSNE

import json

with open('./datasets/results/two_circles_with_bridge.json') as f:
    data = json.load(f)
print('sialal')

# iris = load_iris()
# X_tsne = TSNE(learning_rate=100).fit_transform(iris.data)
#
# figure(figsize=(10, 5))
# subplot(121)
# scatter(X_tsne[:, 0], X_tsne[:, 1], c=iris.target)
# show()

X_tsne = TSNE(learning_rate=100).fit_transform(list(data.values()))

figure(figsize=(10, 5))
subplot(121)
scatter(X_tsne[:, 0], X_tsne[:, 1])
show()
