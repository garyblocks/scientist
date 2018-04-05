import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import model_selection

# import matplotlib.pyplot as plt
def plot_2d(X1, y1, X2, y2, title1='dataset1', title2='dataset2'):
    """
    This function is used to compare two datasets by make 2d-scatter plot for each of them.

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
    """
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
    fig.legend(colors, labels, loc='lower center', ncol=len(C), labelspacing=0.)
    plt.tight_layout(pad=3)
    plt.show()

def test_plot_2d():
    iris = datasets.load_iris()
    X = iris.data[:, :2]  # we only take the first two features.
    y = iris.target
    X1, X2, y1, y2 = model_selection.train_test_split(X, y, test_size=0.5, random_state=42)
    plot_2d(X1, y1, X2, y2)
