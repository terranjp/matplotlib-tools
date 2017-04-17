import numpy as np
import matplotlib.pyplot as plt

from matplotlib_tools.tools import Ruler

xCoord = np.arange(0, 4*np.pi, 0.01)
yCoord = np.sin(xCoord)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid(True)
ax.plot(xCoord, yCoord)

ruler = Ruler(ax=ax)



plt.show()