import numpy as np

from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Text
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class Ruler(object):
    def __init__(self, ax: Axes=None, fig: Figure=None):
        self.fig = fig
        self.ax = ax

        self.ruler_activated = True
        self.background = None
        self.text_background = None
        self.mouse_pressed = False
        self.shift_pressed = False
        self.control_pressed = False
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None

        self.figureText = Figure.text(self=self.fig, x=0, y=0.01, s='Test')
        self.length_text = ax.text(0, 0, 'Test')

        self.arrow = FancyArrowPatch(posA=(0, 0), posB=(0, 0))
        self.arrow.set_mutation_scale(5)
        self.arrow.set_color('r')

        if ax is not None:
            self.set_axes(ax)

    def set_axes(self, ax):
        self.ax = ax
        self.ax.add_patch(self.arrow)
        self.connect()

    def connect(self):
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.ax.figure.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.ax.figure.canvas.mpl_connect('key_release_event', self.on_key_release)

    def on_key_press(self, event):
        print(event.key)
        if event.key == 'shift':
            self.shift_pressed = True

        if event.key == 'control':
            self.control_pressed = True

    def on_key_release(self, event):
        if event.key == 'shift':
            self.shift_pressed = False

        if event.key == 'control':
            self.control_pressed = False

    def on_press(self, event):
        if event.inaxes != self.ax.axes:
            return
        if self.ruler_activated is False:
            return

        self.mouse_pressed = True
        self.x0 = event.xdata
        self.y0 = event.ydata

        self.arrow.set_animated(True)
        self.figureText.set_animated(True)
        self.length_text.set_animated(True)

        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)

        # Redraw everything
        self.fig.draw_artist(self.arrow)
        self.fig.draw_artist(self.figureText)
        self.fig.draw_artist(self.length_text)

        # Blit the whole figure
        self.fig.canvas.blit(self.fig.bbox)

    def on_motion(self, event):
        # On press check if mouse is inside the plot axes.
        if event.inaxes != self.ax.axes:
            return

        if self.mouse_pressed is True:
            self.x1 = event.xdata
            self.y1 = event.ydata

            # If shift is pressed arrow can only move in horizontal axis
            if self.shift_pressed is True:
                pos_a = (self.x0, self.y0)
                pos_b = (self.x1, self.y0)
            # If control is pressed arrow can only move in vertical axis
            elif self.control_pressed is True:
                pos_a = (self.x0, self.y0)
                pos_b = (self.x0, self.y1)
            else:
                pos_a = (self.x0, self.y0)
                pos_b = (self.x1, self.y1)

            # Update position of the length annotation and the arrow
            self.arrow.set_positions(posA=pos_a, posB=pos_b)
            self.length_text.set_position(self.arrow.get_path().vertices[1])

            annote_string = "{:0.2f}".format(self.arrow_length)
            self.length_text.set_text(annote_string)

            fig_string = "Length: {:0.2f}; dx: {:0.2f}; dy: {:0.2f}; angle: {:0.2f}".format(self.arrow_length,
                                                                                            self.arrow_dx,
                                                                                            self.arrow_dy,
                                                                                            self.arrow_angle)
            self.figureText.set_text(fig_string)

            # Draw everything. Tried to
            self.fig.canvas.restore_region(self.background)

            # Redraw the arrow and text
            self.fig.draw_artist(self.arrow)
            self.fig.draw_artist(self.figureText)
            self.fig.draw_artist(self.length_text)

            # Blit the whole figure
            self.fig.canvas.blit(self.fig.bbox)

    def on_release(self, event):
        self.mouse_pressed = False

        if event.inaxes != self.ax.axes:
            return

        self.arrow.set_animated(False)
        self.figureText.set_animated(False)
        self.length_text.set_animated(False)
        self.background = None
        self.fig.canvas.draw()

    @property
    def arrow_length(self):

        return np.sqrt((self.x1 - self.x0) ** 2 + (self.y0 - self.y1) ** 2)

    @property
    def arrow_dx(self):

        return np.abs(self.x1 - self.x0)

    @property
    def arrow_dy(self):

        return np.abs(self.y1 - self.y0)

    @property
    def arrow_angle(self):

        dx = self.x1 - self.x0
        dy = self.y1 - self.y0
        return np.arctan2(dy, dx) * 180 / np.pi


class TextMover(object):
    def __init__(self, ax):
        self.ax = ax
        self.selectedText = None
        self.mousePressed = False
        self.background = None
        self.connect()

    def connect(self):
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.ax.figure.canvas.mpl_connect("pick_event", self.on_pick_event)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_pick_event(self, event):
        print(event.mouseevent)

        if event.mouseevent.button != 1:
            return

        if isinstance(event.artist, Text):
            self.mousePressed = True
            self.selectedText = event.artist

            canvas = self.selectedText.figure.canvas
            axes = self.selectedText.axes
            self.selectedText.set_animated(True)
            canvas.draw()
            self.background = canvas.copy_from_bbox(self.selectedText.axes.bbox)

            axes.draw_artist(self.selectedText)
            canvas.blit(axes.bbox)

    def on_motion(self, event):
        if event.inaxes != self.ax.axes:
            return

        if self.mousePressed is True and self.selectedText:
            self.x1 = event.xdata
            self.y1 = event.ydata

            coords = (self.x1, self.y1)

            self.selectedText.set_position(coords)
            canvas = self.selectedText.figure.canvas
            axes = self.selectedText.axes
            canvas.restore_region(self.background)
            axes.draw_artist(self.selectedText)
            canvas.blit(axes.bbox)

    def on_release(self, event):

        if self.selectedText is None:
            return

        self.mousePressed = False
        self.selectedText.set_animated(False)

        self.background = None
        self.selectedText.figure.canvas.draw()
        self.selectedText = None

    def on_button_press(self, event):
        xCoord = event.xdata
        yCoord = event.ydata

        coords = (xCoord, yCoord)
