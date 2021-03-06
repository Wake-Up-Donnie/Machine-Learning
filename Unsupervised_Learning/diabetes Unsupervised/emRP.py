from sklearn import  datasets, metrics, decomposition, mixture
import matplotlib.pyplot as plt
from sklearn.random_projection import SparseRandomProjection
from sklearn import mixture
import numpy as np
import pandas as pd

data = pd.read_csv(
    'https://archive.ics.uci.edu/ml/machine-learning-databases/pima-indians-diabetes/pima-indians-diabetes.data',
    sep=",", header=None)
colnames =  ['preg', 'plas', 'pres', 'skin', 'insu', 'mass', 'pedi', 'age', 'class']
data.columns = colnames
X, y = data.iloc[:, :-1], data.iloc[:, -1]
X.columns = colnames[:len(colnames)-1]

rp = SparseRandomProjection(n_components=6)
projected_data = rp.fit_transform(X)

gm = mixture.GMM(n_components=2, covariance_type='diag')
gm.fit(projected_data)
X_expect = y
y_pred = gm.predict(projected_data)


both = pd.concat([pd.DataFrame(y_pred), pd.DataFrame(y)],1)
both.columns = ['pred', 'class']


from sklearn.metrics import accuracy_score
print "Accuracy"
print accuracy_score(both['class'], both['pred'])


for k in range(1,8):
    model = mixture.GMM(n_components=k, covariance_type='diag')
    labels = model.fit_predict(projected_data)
    if k == 2:
        all = np.concatenate((projected_data, np.expand_dims(labels, axis=1), np.expand_dims(y, axis=1)), axis=1)
        all= pd.DataFrame(all)

        for l in range(0, 2):
            print "Clus {}".format(l)
            clus = all.loc[all.iloc[:, -2] == l].iloc[:, -2:]
            print clus.shape[0]
            print float(clus.loc[clus.iloc[:, -1] == 0].shape[0]) / clus.shape[0]
            print float(clus.loc[clus.iloc[:, -1] == 1].shape[0]) / clus.shape[0]


homo = []
comp = []
v_mea = []
sil = []
man = []
numPoints = 8
for i in range(2, numPoints):
    rp = SparseRandomProjection(n_components=6)
    projected_data = rp.fit_transform(X)
    gm = mixture.GMM(n_components=i, covariance_type='diag')
    gm.fit(projected_data)
    y_pred = gm.predict(projected_data)
    homo.append(metrics.homogeneity_score(y, y_pred))
    comp.append(metrics.completeness_score(y, y_pred))
    v_mea.append(metrics.v_measure_score(y, y_pred))
    sil.append(metrics.silhouette_score(projected_data, gm.predict(projected_data), metric='euclidean'))
    man.append(metrics.silhouette_score(projected_data, gm.predict(projected_data), metric='manhattan'))

x = xrange(2, numPoints)
fig = plt.figure()
plt.plot(x, homo, label='homogeneity score')
plt.plot(x, comp, label='completeness score')
plt.plot(x, v_mea, label='v measure score')
plt.plot(x, sil, label='Silhouette Score euclidean')
plt.plot(x, man, label='Silhouette Score manhattan')
plt.legend(loc='upper right', shadow=True)
plt.show()