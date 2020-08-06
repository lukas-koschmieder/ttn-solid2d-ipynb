# -*- coding: utf-8
"""@author: Lukas Koschmieder"""

from ipywidgets import interactive
import json
import requests
import time
from IPython.display import clear_output
from ipywidgets import Box, FloatSlider, FloatText, Output, Text, VBox
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable

class Widget(Box):
  def __init__(self, server, t=0.0, verbose=False):
    self.server = server
    self.request = FloatText(description="Request [s]", disabled=True)
    self.predict = FloatText(description="Prediction [s]", disabled=True)
    self.render = FloatText(description="Rendering  [s]", disabled=True)
    self.time = FloatSlider(description="Time [s]", min=0.0, max=1.0, 
                            step=0.01, value=t, continuous_update=False)
    self.status = Text(description="Status", disabled=True)
    self.output = Output()
    
    ui = (self.time,)
    if verbose:
      ui = ui + (self.request, self.predict, self.render)
    ui = ui + (self.status, self.output)

    super(Widget, self).__init__((VBox(ui),))

    self.time.observe(self.update, names=['value'])
    self.update({'new':t})

  def imshow(self, u_grid, v_grid):
    u = self.ax1.imshow(u_grid.T, interpolation='nearest', cmap=plt.cm.jet, 
                        origin='lower', aspect='equal', vmin=-1, vmax=0)
    v = self.ax2.imshow(v_grid.T, interpolation='nearest', cmap=plt.cm.jet, 
                        origin='lower', aspect='equal', vmin=0, vmax=1)
    return (u, v)
 
  def plot(self, x, y, u, v):
    x, y, u, v = np.array(x), np.array(y), np.array(u), np.array(v)

    x_coords, y_coords = np.meshgrid(y, x)
    xy_coords = np.hstack((x_coords.flatten()[:,None], 
                            y_coords.flatten()[:,None]))
    u_grid = griddata(xy_coords, u.flatten(), (x_coords, y_coords), 
                      method='linear')
    v_grid = griddata(xy_coords, v.flatten(), (x_coords, y_coords), 
                      method='linear')

    if not hasattr(self, 'fig'): # figure lazy init
      plt.ioff()
      fig, (ax1, ax2) = plt.subplots(2)
      self.fig, self.ax1, self.ax2 = fig, ax1, ax2
      ax1.set_title('Temperature')
      ax2.set_title('Solid fraction')
      (i1, i2) = self.imshow(u_grid, v_grid)
      cax1 = make_axes_locatable(ax1).append_axes("right", size="5%", pad=0.1)
      cax2 = make_axes_locatable(ax2).append_axes("right", size="5%", pad=0.1)
      fig.colorbar(i1, cax=cax1)
      fig.colorbar(i2, cax=cax2)
      plt.tight_layout()
    else: # figure update
      self.imshow(u_grid, v_grid)
    
    clear_output(wait=True)
    display(self.fig)

  def update(self, t):
    with self.output:
      request_start = time.time()
      self.status.value = "Requesting data..."
      try:
        respond = requests.get("{}?t={}".format(self.server, t['new']))
      except:
        print('ERROR: Failed to request ttn-solid2d-server: {}'
              .format(self.server))
        raise
      self.request.value = str(time.time() - request_start)
      render_start = time.time()
      self.status.value = "Rendering data..."
      try:
        out = json.loads(respond.content)
      except:
        print('ERROR: Failed to parse ttn-solid2d-server resonse: {}'
              .format(respond.content))
        raise
      self.predict.value = str(out['predict_time'])
      self.plot(out['x'], out['y'], out['u'], out['v'])
      self.render.value = str(time.time() - render_start)
      self.status.value = 'Completed in {:.2f}s'.format(time.time() -
                                                        request_start)