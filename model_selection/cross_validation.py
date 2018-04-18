from collections import Counter
import numpy as np
from sklearn.neighbors import KDTree
from sklearn import datasets
import matplotlib.pyplot as plt


def SCV(X, y, k, seed=0):
    """
    Standard stratified cross-validation (SCV):
    It places an equal number of samples of each
    class on each partition to maintain class
    distributions equal in all partitions.

    pseudocode:
    for each class cj ∈ C do
        n ← count(cj)/k
        for each fold Fi (i = 0, . . . , k − 1) do
            E ← randomly select n examples of class cj from D
            Fi ← Fi ∪ E
            D ← D\E
        end for
    end for

    Parameters
    ----------
    X : numpy.ndarray
        data
    y : numpy.ndarray
        labels
    k : int
        number of folds
    seed : int
        random seed for the method

    Returns
    -------
    a list of indexes for each fold
    """
    np.random.seed(seed)
    counts = Counter(y)
    folds = [[] for i in range(k)]  # return indexes for each fold
    # loop through classes
    for cj in counts:
        # calc fold size
        n = int(counts[cj] / k)
        sizes = [n] * k
        # put remains in the folds
        remains = counts[cj] % k
        for i in range(remains):
            sizes[i] += 1

        # split indexes
        class_idx = np.array([ind for ind, val in enumerate(y) if val == cj])
        for i, size in enumerate(sizes):
            fi = np.random.choice(class_idx, size, replace=False).tolist()
            folds[i] += fi
            used = [np.where(class_idx == idx) for idx in fi]
            class_idx = np.delete(class_idx, used)
    return folds


def DB_SCV(X, y, k, dist='euclidean', seed=0):
    """
    Distribution-balanced SCV (DB-SCV):
    keeping data distribution as similar as possible
    between training and test folds by maximizing
    diversity on each fold and trying to keep all
    folds similar to each other.

    pseudocode:
    for each class cj ∈ C do
        e ← randomly select an example of class c j from D
        i=0
        while count(c j ) > 0 do
            Fi ← Fi ∪ {e}
            D ← D \ {e}
            i = (i + 1) mod k
            e ← closest example to e of class cj from D
        end while
    end for

    Parameters
    ----------
    X : numpy.ndarray
        data
    y : numpy.ndarray
        labels
    k : int
        number of folds
    dist : string
        function to calculate distance, check sklearn KDTree
    seed : int
        random seed for the method

    Returns
    -------
    a list of indexes for each fold
    """
    np.random.seed(seed)
    counts = Counter(y)
    folds = [[] for i in range(k)]  # return indexes for each fold
    # loop through classes
    for cj in counts:
        class_idx = np.array([ind for ind, val in enumerate(y) if val == cj])
        e = np.random.choice(class_idx, 1)
        i = 0
        while class_idx.shape[0]:
            x = X[e, :]
            folds[i].append(e[0])
            class_idx = np.delete(class_idx, np.where(class_idx == e))
            i = (i + 1) % k
            X_cj = X[class_idx]
            if not X_cj.shape[0]:
                break
            kdt = KDTree(X_cj, leaf_size=30, metric=dist)
            ind = kdt.query(x, k=1, return_distance=False)
            e = np.array([class_idx[ind[0, 0]]])
    return folds


def DOB_SCV(X, y, k, dist='euclidean', seed=0):
    """
    Distribution-balanced SCV (DB-SCV):
    a method designed for testing the maximal influence
    of partition-based covariate shift. It creates folds
    that are as different as possible to each other.

    pseudocode:
    for each class cj ∈ C do
        while count(c j ) > 0 do
            e0 ← randomly select an example of class cj from D
            ei ← ith closest example to e0 of class cj from D (i = 1, . . . , k − 1)
            Fi ← Fi ∪ {ei } (i = 0, . . . , k − 1)
            D ← D \ {ei } (i = 0, . . . , k − 1)
        end while
    end for

    Parameters
    ----------
    X : numpy.ndarray
        data
    y : numpy.ndarray
        labels
    k : int
        number of folds
    dist : string
        function to calculate distance, check sklearn KDTree
    seed : int
        random seed for the method

    Returns
    -------
    a list of indexes for each fold
    """
    np.random.seed(seed)
    counts = Counter(y)
    folds = [[] for i in range(k)]  # return indexes for each fold
    # loop through classes
    for cj in counts:
        class_idx = np.array([ind for ind, val in enumerate(y) if val == cj])
        while class_idx.shape[0]:
            X_cj = X[class_idx]
            # randomly select an example of class cj
            e = np.random.choice(class_idx, 1)
            x = X[e, :]
            # find k closest examples
            n = min(k, len(X_cj))
            kdt = KDTree(X_cj, leaf_size=30, metric=dist)
            ind = kdt.query(x, k=n, return_distance=False).ravel().tolist()
            seen = []
            for i, loc in enumerate(ind):
                folds[i].append(class_idx[loc])
                seen.append(loc)
            class_idx = np.delete(class_idx, seen, axis=0)
    return folds


def MS_SCV(X, y, k, dist='euclidean'):
    """
    Maximally shifted SCV (MS-SCV): keeping data distribution as similar as possible
    between training and test folds by maximizing diversity on each fold and trying to keep
    all folds similar to each other.

    pseudocode:
    for each class cj ∈ C do
        n ← count(cj)/k
        e ← randomly select an example of class cj from D
        for each fold Fi (i = 0, . . . , k − 1) do
            for s = 1 → n do
                Fi ← Fi ∪ {e}
                D ← D \ {e}
                e ← closest example to e of class cj from D
            end for
        end for
    end for

    Parameters
    ----------
    X : numpy.ndarray
        data
    y : numpy.ndarray
        labels
    k : int
        number of folds
    dist : string
        function to calculate distance, check sklearn KDTree
    seed : int
        random seed for the method

    Returns
    -------
    a list of indexes for each fold
    """
    counts = Counter(y)
    folds = [[] for i in range(k)]  # return indexes for each fold
    # loop through classes
    for cj in counts:
        # calc fold size
        n = int(counts[cj] / k)
        sizes = [n] * k

        class_idx = np.array([ind for ind, val in enumerate(y) if val == cj])
        e = np.random.choice(class_idx, 1)
        for i in range(len(folds)):
            for sz in range(sizes[i]):
                x = X[e, :]
                folds[i].append(e[0])
                class_idx = np.delete(class_idx, np.where(class_idx == e))
                X_cj = X[class_idx]
                if not X_cj.shape[0]:
                    # for last example
                    break
                kdt = KDTree(X_cj, leaf_size=30, metric=dist)
                ind = kdt.query(x, k=1, return_distance=False)
                e = np.array([class_idx[ind[0, 0]]])
    return folds


def small_test(cv):
    # unit test
    X = np.array([[1, 2], [1, 3], [24, 22], [12, 17], [100, 97], [99, 101]])
    y = np.array([1, 1, 1, 1, 0, 0])
    fold_index = cv(X, y, 2)
    print(fold_index)
    print(X[fold_index[0]])
    print(y[fold_index[0]])
    print(X[fold_index[1]])
    print(y[fold_index[1]])


def integrate_test(cv):
    # integrate test
    iris = datasets.load_iris()
    X = iris.data[:, :2]  # we only take the first two features.
    y = iris.target
    f = cv(X, y, k=2)
    plot_2d(X[f[0]], y[f[0]], X[f[1]], y[f[1]])


def plot_2d(X1, y1, X2, y2, title1='dataset1', title2='dataset2'):
    # Two subplots, unpack the axes array immediately
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # plot two subplots
    colors, labels = [], []
    C = set(y1) | set(y2)
    for ci in C:
        label = "Class " + str(ci)
        # plot dataset1
        col = ax1.scatter(X1[y1 == ci, 0], X1[y1 == ci, 1], label=label, alpha=0.5)
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
    fig.legend(colors, labels, loc='lower center', ncol=len(C), labelspacing=0.5)
    plt.tight_layout(pad=3)
    plt.show()
