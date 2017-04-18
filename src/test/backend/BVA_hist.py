import matplotlib.pylab as plt
import collections, sys
import numpy as np

BVA_FOLDER = '../../api_handlers/lib/'
sys.path.insert(1, BVA_FOLDER)
import BVA
components = ["twitter-timeline", "facebook-wall", "pinterest-timeline", "googleplus-timeline", "traffic-incidents", "finance-search", "open-weather"]
versions = ["stable", "latency", "accuracy", "maintenance", "complexity", "structural"]

bva = BVA.BVA(components,versions)

list_versions=[]
iterations=10000

for _ in range(iterations):
  list_versions += bva.getNewVersions()

data = collections.Counter(list_versions)
def autolabel(rects, ax):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., height,"%d" % int(height),ha="center", va="bottom")
def plot_bar_from_counter(counter, ax=None):
    """"
    This function creates a bar plot from a counter.

    :param counter: This is a counter object, a dictionary with the item as the key
     and the frequency as the value
    :param ax: an axis of matplotlib
    :return: the axis wit the object in it
    """

    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

    frequencies = counter.values()
    names = counter.keys()

    x_coordinates = np.arange(len(counter))
    rects = ax.bar(x_coordinates, frequencies, align='center')
    for i, v in enumerate(frequencies):
      ax.text(v, i, str(v), color='black', fontweight='bold')
    ax.xaxis.set_major_locator(plt.FixedLocator(x_coordinates))
    ax.xaxis.set_major_formatter(plt.FixedFormatter(names))
    autolabel(rects, ax)
    return ax




plot_bar_from_counter(data)
plt.show()

