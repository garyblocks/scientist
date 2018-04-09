import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn import datasets
from sklearn import model_selection
import itertools as it
import numpy as np

# import matplotlib.patches as mpatches
# import itertools as it
# import numpy as np
def plot_profile(X, y, names):
    """
    plot the profiles for each data point by classes

    Parameters
    ----------
    X : numpy.array
        features for each subject
    y : numpy.array
        labels for each subject
    names : list
        names of the features

    Returns
    -------
    None

    >>> plot_profile(X, y, names)
    """
    # spilt the data into clusters by class label
    clusters = {i:[] for i in set(y)}
    for i in range(len(y)):
        clusters[y[i]].append(i)
    fig = plt.figure(figsize=(15, 10), dpi= 100, facecolor='w', edgecolor='k')
    # choose subplot
    ax = plt.subplot(1, 1, 1)
    # custom x ticks
    x = [i for i in range(len(names))]
    plt.xticks(x, names, fontsize = 12)
    # rotate xticks
    for label in ax.get_xmajorticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment("right")
        # Plot first center
        # ax.plot(x,centers.tolist()[j],color='red')
        # plot data points in a cluster
        patches = []
        colors = it.cycle(plt.cm.rainbow(np.linspace(0,1,len(clusters))))
        for cls, clr in zip(clusters, colors):
            patches.append(mpatches.Patch(color=clr, label=cls))
            for i in clusters[cls]:
                ax.plot(x, X[i], color=clr ,alpha=0.02, linewidth=2.0)
        # set ylabel and title
        plt.title('profile for each individual')
    plt.legend(handles=patches)
    plt.show()

def test_plot_profile():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    names = list(iris.feature_names)
    plot_profile(X, y, names)
