import numpy as np
import matplotlib.pyplot as plt
import traceback
import sys

from matplotlib_tools.tools import Ruler

def handleException(exc_type, exc_value, exc_traceback):

    traceback.format_exception(exc_type, exc_value, exc_traceback)
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    # root_logger.critical("Uncaught {}".format(exc_type.__name__), exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handleException


xCoord = np.arange(0, 5, 1)
yCoord = [0, 1, -3, 5, -3]
fig = plt.figure()
ax = fig.add_subplot(111)

markerprops = dict(marker='o', markersize=5, markeredgecolor='red')
lineprops = dict(color='red', linewidth=2)

ax.grid(True)
ax.plot(xCoord, yCoord)
ruler = Ruler(ax=ax,
              useblit=True,
              markerprops=markerprops,
              lineprops=lineprops)

plt.show()