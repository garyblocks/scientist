import matplotlib.pyplot as plt
import numpy as np
import math
from collections import Counter
from sklearn.preprocessing import MinMaxScaler
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches


# import matplotlib.pyplot as plt
def plot_2d(X1, y1, X2, y2, title1='dataset1', title2='dataset2'):
    """
    This function is used to compare two datasets by
    make 2d-scatter plot for each of them.

    Parameters
    ----------
    X1: 2d numpy.ndarray
        data for dataset1
    y1: 1d numpy.ndarray
        label for dataset1
    X2: 2d numpy.ndarray
        data for dataset2
    y2: 1d numpy.ndarray
        label for dataset2
    title1: str
        title for plot1
    title2: str
        title for plot2

    >>> plot_2d(X1, y1, X2, y2)
    """
    # Two subplots, unpack the axes array immediately
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # plot two subplots
    colors, labels = [], []
    C = set(y1) | set(y2)
    for ci in C:
        label = "Class " + str(ci)
        # plot dataset1
        col = ax1.scatter(
            X1[y1 == ci, 0],
            X1[y1 == ci, 1],
            label=label,
            alpha=0.5
        )
        # plot dataset2
        ax2.scatter(X2[y2 == ci, 0], X2[y2 == ci, 1], label=label, alpha=0.5)
        colors.append(col)
        labels.append(label)
    ax1.set_title(title1)
    ax2.set_title(title2)

    # make nice plotting
    for ax in (ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.spines['left'].set_position(('outward', 10))
        ax.spines['bottom'].set_position(('outward', 10))
    fig.legend(colors, labels, loc='lower center', ncol=len(C), labelspacing=0)
    plt.tight_layout(pad=3)
    plt.show()


def plot_coincidence(y1, y2):
    """
    plot the coincidence between 2 sets of labes on the same dataset

    Parameters
    ----------
    y1 : list
        first list of labels
    y2 : list
        second list of labels

    Returns
    -------
    None

    >>> plot_coincidence(y1, y2)
    """
    if len(y1) != len(y2):
        print('The two sets of labels are not of same length')
    # count coincidence
    pairs = list(zip(y1, y2))
    freq = Counter(pairs)
    xyz = [tuple(list(key) + [value]) for key, value in freq.items()]
    x, y, z = (np.array(i[0]) for i in zip(zip(*xyz)))
    z = z * z

    # rescale size
    scaler = MinMaxScaler()
    scaler.fit(z.reshape(-1, 1))
    z = scaler.transform(z.reshape(-1, 1)).ravel() + 1

    # use the scatter function
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    ax.scatter(
        x, y, s=z*2000, c=z, cmap="RdYlGn",
        alpha=0.4, edgecolors="black", linewidth=2
    )
    plt.xticks(range(min(x), math.ceil(max(x))+1))
    plt.yticks(range(min(y), math.ceil(max(y))+1))
    plt.show()


# from os import path
# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt
# from wordcloud import WordCloud, STOPWORDS
def word_cloud(text, path_to_pic="default_pic.png", stop_words=["said"]):
    """
    plot a word cloud based on frequency of words

    Parameters
    ----------
    text : str
        text string
    path_to_pic : str
        path to a picture used as the shape of word cloud

    Returns
    -------
    None

    >>> plot_coincidence(y1, y2)
    """
    # set up the word cloud
    mask = np.array(Image.open(path_to_pic))
    stopwords = set(STOPWORDS)
    for wd in stop_words:
        stopwords.add("said")
    wc = WordCloud(
        background_color="white",
        max_words=200,
        mask=mask,
        stopwords=stopwords
    )

    # generate word cloud
    wc.generate(text)

    # show
    plt.figure(figsize=(16, 10))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    # plt.tight_layout(pad=0)
    plt.show()


# from mpl_toolkits.mplot3d import Axes3D
# import matplotlib.patches as mpatches
def plot_3d(X, y, names):
    """
    plot 3 dimesnsion on a 3d scatter plot

    Parameters
    ----------
    X : numpy.array
        Feature data
    y : numpy.array
        Label data
    names : list
        feature names

    Returns
    -------
    None

    >>> plot_3d(X, y, names)
    """
    fig = plt.figure(1, figsize=(15, 6), dpi=100, facecolor='w', edgecolor='k')
    plt.clf()
    ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
    plt.cla()
    # colors
    N = len(set(y)) + 1
    cmap = plt.cm.get_cmap("hsv", N)
    clrs = [cmap(int(i)) for i in y]
    # legend
    recs = [mpatches.Rectangle((0, 0), 1, 1, fc=cmap(i))
            for i in range(0, N - 1)]
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=clrs)
    plt.legend(recs, set(y), loc=4)
    # ax.w_xaxis.set_ticklabels([])
    # ax.w_yaxis.set_ticklabels([])
    # ax.w_zaxis.set_ticklabels([])
    ax.set_xlabel(names[0])
    ax.set_ylabel(names[1])
    ax.set_zlabel(names[2])
    plt.show()
