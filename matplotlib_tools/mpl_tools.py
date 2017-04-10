import numpy as np

from matplotlib.patches import FancyArrowPatch
from matplotlib.text import Text
from matplotlib.axes import Axes
from matplotlib.figure import Figure


class Ruler(object):
    """
    Simple measurement tool for matplotlib. 
    
    """
    def __init__(self, ax: Axes, ruler_unit: str=None):
        self.ax = ax
        self.fig = ax.figure
        self.ruler_unit = ruler_unit

        self.ruler_activated = True
        self.ruler_visible = True
        self.mouse_1_pressed = False
        self.mouse_3_pressed = False
        self.shift_pressed = False
        self.control_pressed = False

        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None

        self.arrow_init_coords = None

        self.arrow = None
        self.ruler_marker = None
        self.fig_measure_text = None
        self.ruler_text = None
        self.create_arrow()
        self.background = None

        self.connect()

    def connect(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)

    def create_arrow(self):
        # Create an arrow from a Fancy Arrow Patch
        # TODO: Allow configuration of arrow with kwargs
        self.arrow = FancyArrowPatch(posA=(0, 0), posB=(0, 0))
        self.arrow.set_mutation_scale(5)
        self.arrow.set_color('r')
        self.ax.add_patch(self.arrow)

        # Add empty text artists to the figure and the axes.
        # TODO: Allow config of text with kwargs
        self.fig_measure_text = Figure.text(self=self.ax.figure, x=0, y=0.01, s='')
        self.ruler_text = self.ax.text(0, 0, '')

    def on_key_press(self, event):
        if event.key == 'shift':
            self.shift_pressed = True

        if event.key == 'control':
            self.control_pressed = True

        if event.key == 'm':
            self.toggle_ruler()

        if event.key == 'ctrl+m':
            self.toggle_ruler_visibility()

    def on_key_release(self, event):
        if event.key == 'shift':
            self.shift_pressed = False

        if event.key == 'control':
            self.control_pressed = False

    def toggle_ruler(self):
        if self.ruler_activated is True:
            print('Ruler: deactivated')
            self.ruler_activated = False

        elif self.ruler_activated is False:
            print('Ruler: activated')
            self.ruler_activated = True

    def toggle_ruler_visibility(self):
        if self.ruler_visible is True:
            print('Ruler: invisible')
            self.ruler_activated = False
            self.ruler_visible = False
            self.arrow.set_visible(False)
            self.ruler_text.set_visible(False)
            self.fig_measure_text.set_visible(False)

        elif self.ruler_visible is False:
            print('Ruler: visible')
            self.ruler_visible = True
            self.arrow.set_visible(True)
            self.ruler_text.set_visible(True)
            self.fig_measure_text.set_visible(True)

        self.fig.canvas.draw()

    def on_press(self, event):
        print(event.button)

        if event.inaxes != self.ax.axes:
            return
        if self.ruler_activated is False:
            return

        if event.button == 1 and self.mouse_3_pressed is False:
            self.handle_button_1_press(event)
        elif event.button == 3:
            self.handle_button_3_press(event)

    def handle_button_1_press(self, event):
        if self.arrow is None:
            self.create_arrow()

        self.mouse_1_pressed = True

        self.x0 = event.xdata
        self.y0 = event.ydata

        self.arrow.set_animated(True)
        self.fig_measure_text.set_animated(True)
        self.ruler_text.set_animated(True)

        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)

        # Redraw everything
        self.fig.draw_artist(self.arrow)
        self.fig.draw_artist(self.fig_measure_text)
        self.fig.draw_artist(self.ruler_text)

        # Blit the whole figure. Tried just drawing the arrow and the text but ran into clipping issues.
        self.fig.canvas.blit(self.fig.bbox)

    def handle_button_3_press(self, event):
        if self.arrow is None:
            self.create_arrow()

        self.mouse_3_pressed = True

        if self.arrow_init_coords is None:
            self.x0 = event.xdata
            self.y0 = event.ydata
            self.ruler_marker, = self.ax.plot(self.x0, self.y0, 'xr')
            self.fig.canvas.draw()
            self.arrow_init_coords = self.x0, self.y0

        elif self.arrow_init_coords is not None:
            self.x1 = event.xdata
            self.y1 = event.ydata
            self.arrow_end_coords = self.x1, self.y1

            self.arrow.set_positions(posA=self.arrow_init_coords, posB=self.arrow_end_coords)
            self.ruler_text.set_position(self.arrow.get_path().vertices[1])
            self.ruler_marker.remove()
            self.update_text()
            self.fig.canvas.draw()
            self.arrow_init_coords = None
            self.mouse_3_pressed = False

    def on_motion(self, event):
        # On press check if mouse is inside the plot axes.
        if event.inaxes != self.ax.axes:
            return

        if self.mouse_1_pressed is True:
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
            self.ruler_text.set_position(self.arrow.get_path().vertices[1])

            self.update_text()

            # Draw everything. Tried to draw the arrow and text separately but ran into clipping issues
            self.fig.canvas.restore_region(self.background)

            # Redraw the arrow and text
            self.fig.draw_artist(self.arrow)
            self.fig.draw_artist(self.fig_measure_text)
            self.fig.draw_artist(self.ruler_text)

            # Blit the whole figure
            self.fig.canvas.blit(self.fig.bbox)

    def update_text(self):
        if self.ruler_unit is not None:
            self.ruler_text.set_text("{:0.2f} {}".format(self.ruler_length, self.ruler_unit))
            measure_string = "L: {:0.2f} {}; dx: {:0.2f} {}; dy: {:0.2f} {}; angle: {:0.2f} °".format(self.ruler_length,
                                                                                                      self.ruler_unit,
                                                                                                      self.ruler_dx,
                                                                                                      self.ruler_unit,
                                                                                                      self.ruler_dy,
                                                                                                      self.ruler_unit,
                                                                                                      self.ruler_angle)

        else:
            self.ruler_text.set_text("{:0.2f}".format(self.ruler_length))
            measure_string = "Length: {:0.2f}; dx: {:0.2f}; dy: {:0.2f}; angle: {:0.2f} °".format(self.ruler_length,
                                                                                                  self.ruler_dx,
                                                                                                  self.ruler_dy,
                                                                                                  self.ruler_angle)

        self.fig_measure_text.set_text(measure_string)

    def on_release(self, event):
        self.mouse_1_pressed = False

        if event.inaxes != self.ax.axes:
            return

        self.arrow.set_animated(False)
        self.fig_measure_text.set_animated(False)
        self.ruler_text.set_animated(False)
        self.background = None
        self.ax.figure.canvas.draw()

    @property
    def ruler_length(self):
        return np.sqrt((self.x1 - self.x0) ** 2 + (self.y0 - self.y1) ** 2)

    @property
    def ruler_dx(self):
        return np.abs(self.x1 - self.x0)

    @property
    def ruler_dy(self):
        return np.abs(self.y1 - self.y0)

    @property
    def ruler_angle(self):
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
