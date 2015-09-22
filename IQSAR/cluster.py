X=r3

print __doc__

from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs



# Compute Affinity Propagation
def afprop(X):
    af = AffinityPropagation(affinity='euclidean').fit(X)
    cluster_centers_indices = af.cluster_centers_indices_
    labels = af.labels_



    n_clusters_ = len(cluster_centers_indices)

    print 'Estimated number of clusters: %d' % n_clusters_
    print ("Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels, metric='sqeuclidean'))


from sGreedy import sG


def read_data(input_fname):
    fp = open(input_fname, 'r')
    labels = map(str.strip, fp.readline().split(',')[1:])
    nx = len(labels)
    print "nx=", nx
    lst_data = []
    idx = 0
    while 1:
        line = fp.readline()
        if not line:
            break
        ll = line.split(',')
        if labels[idx] != ll[0]:
            print "#JMS>Err, label mismatch!!, idx=%d, label=%s, ll[0]=%s" % (idx, labels[idx], ll[0])
            break
        lst_data.append(ll[1:])

        idx +=1
        
    fp.close()

    return labels, lst_data


def chk_data_symmetry(data):
    nr, nc = data.shape
    for i in range(nr):
        for j in range(i, nc):
            if data[i, j] != data[j, i]:
                print "#JMS>Err, data symmetry err!! (i,j)=(%d,%d)", (i,j)
    return



def doit():
    labels, lst_data = read_data()
    data = np.array(lst_data, dtype=np.float)
    print "data.shape=", data.shape

    tc = sG(labels, data)
    tc.run()
    return tc.Info2()


if __name__ == '__main__':
    doit()
'''
##############################################################################
# Plot result
import pylab as pl
from itertools import cycle

pl.close('all')
pl.figure(1)
pl.clf()

cluster1=list()


colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    pl.plot(X[class_members, 0], X[class_members, 1], col + '.')
    pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
            markeredgecolor='k', markersize=14)
    for x in X[class_members]:
        pl.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)
        
pl.title('Estimated number of clusters: %d' % n_clusters_)
pl.show()

print cluster_centers_indices
print cluster_centers_indices[labels].shape

print cluster_centers_indices
print labels
print labels.shape

print r3[cluster_centers_indices[labels]]'''
