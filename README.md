# matplotlib-tools
Various tools for matplotlib.

<h2>Ruler</h2>

An an interactive ruler to measure distances. Heavily inspired by the tool in ImageJ.
    
    
Usage:
----------

1. Hold left click drag and release to draw the ruler in the axes.
  - Hold shift while dragging to lock the ruler to the horizontal axis.
  - Hold control while drawing to lock the ruler to the vertical axis. 

2. Right click one of the markers to move the ruler. 

The keyboard can be used to activate and deactivate the ruler and toggle 
visibility of the line and text:

'm' : Toggles the ruler on and off. 

'ctl+m' : Toggles the visibility of the ruler and text. 

Example
----------
    
    >>> xCoord = np.arange(0, 5, 1)
    >>> yCoord = [0, 1, -3, 5, -3]
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot(111)
    
    >>> markerprops = dict(marker='o', markersize=5, markeredgecolor='red')
    >>> lineprops = dict(color='red', linewidth=2)
    
    >>> ax.grid(True)
    >>> ax.plot(xCoord, yCoord)
    
    >>> ruler = Ruler(ax=ax,
                  useblit=True,
                  markerprops=markerprops,
                  lineprops=lineprops)
    
    >>> plt.show()
    


![Ruler Gif](/animated_gif/mpl_ruler.gif?raw=True)



