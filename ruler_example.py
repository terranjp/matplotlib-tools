
import numpy as np
import matplotlib.pyplot as plt

from matplotlib_tools.mpl_tools import Ruler

yCoord = np.arange(0, 100, 1)
xCoord = np.arange(0, 100, 1)

fig = plt.figure()


ax = fig.add_subplot(111)

ax(True)
ruler = Ruler(ax=ax, ruler_unit='ft')

ax.plot(xCoord, yCoord, picker=5)

plt.show()