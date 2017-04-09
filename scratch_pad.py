import sys
import traceback

import numpy as np
import matplotlib.pyplot as plt

from matplotlib_tools.mpl_tools import Ruler
from matplotlib_tools.mpl_tools import TextMover

def handleException(exc_type, exc_value, exc_traceback):
    traceback.format_exception(exc_type, exc_value, exc_traceback)
    traceback.print_exception(exc_type, exc_value, exc_traceback)

sys.excepthook = handleException



yCoord = np.arange(0, 10, 1)
xCoord = np.arange(0, 10, 1)

fig = plt.figure()

ax = fig.add_subplot(111)

ruler = Ruler(ax=ax, fig=fig)

ax.set_ylim([0, 10])
ax.set_xlim([0, 10])
ax.plot(xCoord, yCoord, picker=5)

plt.show()