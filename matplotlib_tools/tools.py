import numpy as np

from matplotlib.text import Text
from matplotlib.axes import Axes


class Ruler(object):
    """
    A simple ruler to measure distances on an axes instance. 
    
    There are two modes of operation:
    
    1. Hold left click drag and release to draw the ruler in the axes.
      - Hold shift while dragging to lock the ruler to the horizontal axis.
      - Hold control while drawing to lock the ruler to the vertical axis. 
    
    2. Right click to set the start point and right click again to set the endpoint. 
    
    The keyboard can be used to activate and deactivate the ruler and toggle visibility of the line and text:
    
    'm' : Toggles the ruler on and off. Currently there is no indication on the figure that 
        the ruler is activated. 
         
    'ctl+m' : Toggles the visibility of the ruler and text. 
    
    
    """
    def __init__(self, ax: Axes, ruler_active=True, ruler_unit: str=None):
        """
        Add a ruler to *ax*. If ``ruler_active=True``, the ruler will be activated when the plot is first created.
        If ``ruler_unit`` is set the string will be appended to the length text annotations. 
        
        """

        self.ax = ax
        self.fig = ax.figure
        self.ruler_active = ruler_active
        self.ruler_unit = ruler_unit

        self.ruler_visible = True
        self.mouse_1_pressed = False
        self.mouse_3_pressed = False
        self.shift_pressed = False
        self.control_pressed = False

        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None

        self.line_start_coords = None
        self.line_end_coords = None

        self.line, = self.ax.plot([0, 0], [0, 0])
        self.line_text = self.ax.text(0, 0, '')
        self.detail_text = self.ax.figure.text(0, 0.01, '')
        self.ruler_marker = None

        self.background = None

        self.connect_events()

    def connect_events(self):
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)

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
        if self.ruler_active is True:
            print('Ruler: deactivated')
            self.ruler_active = False

        elif self.ruler_active is False:
            print('Ruler: activated')
            self.ruler_active = True

    def toggle_ruler_visibility(self):
        if self.ruler_visible is True:
            print('Ruler: invisible')
            self.ruler_active = False
            self.ruler_visible = False
            self.line.set_visible(False)
            self.line_text.set_visible(False)
            self.detail_text.set_visible(False)

        elif self.ruler_visible is False:
            print('Ruler: visible')
            self.ruler_visible = True
            self.line.set_visible(True)
            self.line_text.set_visible(True)
            self.detail_text.set_visible(True)

        self.fig.canvas.draw()

    def on_press(self, event):
        """
        On mouse button press check if mouse is within the axes and 
        then check which button has been pressed and handle event
        """

        if event.inaxes != self.ax.axes:
            return
        if self.ruler_active is False:
            return

        if event.button == 1 and self.mouse_3_pressed is False:
            self.handle_button_1_press(event)
        elif event.button == 3:
            self.handle_button_3_press(event)

    def handle_button_1_press(self, event):
        """On button 1 press start drawing the ruler line from the initial press position"""

        self.mouse_1_pressed = True

        self.x0 = event.xdata
        self.y0 = event.ydata

        self.line.set_animated(True)
        self.line_text.set_animated(True)
        self.detail_text.set_animated(True)

        self.fig.canvas.draw()
        self.background = self.fig.canvas.copy_from_bbox(self.fig.bbox)

        # Redraw everything
        self.fig.draw_artist(self.line)
        self.fig.draw_artist(self.line_text)
        self.fig.draw_artist(self.detail_text)

        # Blit the whole figure.
        self.fig.canvas.blit(self.fig.bbox)

    def handle_button_3_press(self, event):
        """
        If button 3 is pressed draw on indicator at first press and then draw the lin to the cursor on second press

        """

        self.mouse_3_pressed = True

        if self.line_start_coords is None:
            self.x0 = event.xdata
            self.y0 = event.ydata
            self.ruler_marker, = self.ax.plot(self.x0, self.y0, 'xr')
            self.fig.canvas.draw()
            self.line_start_coords = self.x0, self.y0

        elif self.line_start_coords is not None:
            self.x1 = event.xdata
            self.y1 = event.ydata
            self.line_end_coords = self.x1, self.y1

            posA = self.line_start_coords[0], self.line_end_coords[0]
            posB = self.line_start_coords[1], self.line_end_coords[1]

            self.line.set_data(posA, posB)

            mid_line_coords = (self.x0 + self.x1) / 2, (self.y0 + self.y1) / 2
            self.line_text.set_position(mid_line_coords)

            self.ruler_marker.remove()
            self.update_text()
            self.fig.canvas.draw()
            self.line_start_coords = None
            self.mouse_3_pressed = False

    def on_motion(self, event):
        """
        On mouse motion draw the ruler and update the text if button 1 is pressed. 
        """
        if event.inaxes != self.ax.axes:
            return

        if self.mouse_1_pressed is True:
            self.x1 = event.xdata
            self.y1 = event.ydata

            # If shift is pressed ruler is constrained to horizontal axis
            if self.shift_pressed is True:
                pos_a = self.x0, self.x1
                pos_b = self.y0, self.y0
            # If control is pressed ruler is constrained to vertical axis
            elif self.control_pressed is True:
                pos_a = self.x0, self.x0
                pos_b = self.y0, self.y1
            # Else the ruler follow the mouse cursor
            else:
                pos_a = self.x0, self.x1
                pos_b = self.y0, self.y1

            # Update position of line, the text length annotation on the middle of the line
            self.line.set_data([pos_a], [pos_b])

            line_coords = self.line.get_path().vertices
            x0 = line_coords[0][0]
            y0 = line_coords[0][1]
            x1 = line_coords[1][0]
            y1 = line_coords[1][1]
            mid_line_coords = (x0 + x1)/2, (y0 + y1)/2

            self.line_text.set_position(mid_line_coords)
            self.update_text()
            self.fig.canvas.restore_region(self.background)

            # Redraw arrow and text
            self.fig.draw_artist(self.line)
            self.fig.draw_artist(self.line_text)
            self.fig.draw_artist(self.detail_text)

            # Blit the whole figure
            self.fig.canvas.blit(self.fig.bbox)

    def update_text(self):
        """Update the length text on the line and detailed text on the figure"""

        if self.ruler_unit is not None:
            self.line_text.set_text("{:0.3f} {}".format(self.ruler_length, self.ruler_unit))
            detail_string = "L: {:0.3f} {}; dx: {:0.3f} {}; dy: {:0.3f} {}; angle: {:0.3f} °".format(self.ruler_length,
                                                                                                     self.ruler_unit,
                                                                                                     self.ruler_dx,
                                                                                                     self.ruler_unit,
                                                                                                     self.ruler_dy,
                                                                                                     self.ruler_unit,
                                                                                                     self.ruler_angle)

        else:
            self.line_text.set_text("{:0.3f}".format(self.ruler_length))
            detail_string = "Length: {:0.3f}; dx: {:0.3f}; dy: {:0.3f}; angle: {:0.3f} °".format(self.ruler_length,
                                                                                                 self.ruler_dx,
                                                                                                 self.ruler_dy,
                                                                                                 self.ruler_angle)

        self.detail_text.set_text(detail_string)

    def on_release(self, event):
        self.mouse_1_pressed = False

        if event.inaxes != self.ax.axes:
            return

        self.line.set_animated(False)
        self.line_text.set_animated(False)
        self.detail_text.set_animated(False)
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
    """
    A simple little tool to move text annotation in an axes by clicking and dragging them. 

    """

    def __init__(self, ax: Axes, active=False):
        self.ax = ax
        self.active = active
        self.selectedText = None
        self.mousePressed = False
        self.background = None
        self.connect_events()

    def connect_events(self):
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_button_press)
        self.ax.figure.canvas.mpl_connect("pick_event", self.on_pick_event)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)

    def on_pick_event(self, event):

        if self.active is False:
            return

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

