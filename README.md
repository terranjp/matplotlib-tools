# matplotlib-tools
Various tools for matplotlib.

<h2>Ruler</h2>

An an interactive ruler to measure distances. 
    
There are two modes of operation:

1. Hold left click drag and release to draw the ruler in the axes.
  - Hold shift while dragging to lock the ruler to the horizontal axis.
  - Hold control while drawing to lock the ruler to the vertical axis. 

2. Right click to set the start point and right click again to set the endpoint. 

The keyboard can be used to activate and deactivate the ruler and toggle visibility of the line and text:

 - 'm' : Toggles the ruler on and off. Currently there is no indication on the figure that 
    the ruler is activated. 
     
 - 'ctl+m' : Toggles the visibility of the ruler and text. 


To use the ruler pass an Axes instance as the first arg to the constructor. A example usage is shown below:


    import numpy as np
    import matplotlib.pyplot as plt
    
    from matplotlib_tools.mpl_tools import Ruler
    
    xCoord = np.arange(0, 4*np.pi, 0.01)
    yCoord = np.sin(xCoord)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.grid(True)
    ax.plot(xCoord, yCoord)
    
    ruler = Ruler(ax=ax)
    
    plt.show()


![Ruler Gif]
(/animated_gif/mpl_ruler.gif)



