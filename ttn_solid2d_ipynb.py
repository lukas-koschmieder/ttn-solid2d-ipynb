# -*- coding: utf-8
"""@author: Lukas Koschmieder"""

from ipywidgets import interactive
import json
import requests
import time
from IPython.display import clear_output
from ipywidgets import FloatText, FloatSlider
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from mpl_toolkits.axes_grid1 import make_axes_locatable

class Widget():
  def __init__(self, server):
    self.server = server
    self.ui_rtt = FloatText(description="RTT [s]", disabled=True)
    self.ui_predict = FloatText(description="Prediction [s]", disabled=True)
    self.ui_render = FloatText(description="Rendering  [s]", disabled=True)
    self.ui_time = FloatSlider(description="Time [s]", min=0.0, max=1.0, 
                               step=0.01, continuous_update=False)

  def plot(self, x, y, u, v):
    with self.ui_output:
      x, y, u, v = np.array(x), np.array(y), np.array(u), np.array(v)

      x_coords, y_coords = np.meshgrid(y, x)
      xy_coords = np.hstack((x_coords.flatten()[:,None], 
                            y_coords.flatten()[:,None]))
      
      u_grid = griddata(xy_coords, u.flatten(), 
                        (x_coords, y_coords), method='linear')
      v_grid = griddata(xy_coords, v.flatten(), 
                        (x_coords, y_coords), method='linear')

      fig, (ax1, ax2) = plt.subplots(2)

      ax1.set_title('Temperature')
      h1 = ax1.imshow(u_grid.T, interpolation='nearest', cmap=plt.cm.jet, 
                      origin='lower', aspect='equal', vmin=-1, vmax=0)
      cax1 = make_axes_locatable(ax1).append_axes("right", size="5%", pad=0.1)
      fig.colorbar(h1, cax=cax1)

      ax2.set_title('Solid fraction')
      h2 = ax2.imshow(v_grid.T, interpolation='nearest', cmap=plt.cm.jet, 
                      origin='lower', aspect='equal', vmin=0, vmax=1)
      cax2 = make_axes_locatable(ax2).append_axes("right", size="5%", pad=0.1)
      fig.colorbar(h2, cax=cax2)

      plt.tight_layout()
      plt.show()

  def update(self, t):
      with self.ui_output:
          rtt_start = time.time()
          try:
            #respond = requests.get(self.server, data={ 't': t })
            respond = requests.get("{}?t={}".format(self.server, t))
          except:
            print('ERROR: Failed to request ttn-solid2d-server: {}'
                  .format(self.server))
            raise
          self.ui_rtt.value = str(time.time() - rtt_start)
          render_start = time.time()
          try:
            out = json.loads(respond.content)
          except:
            print('ERROR: Failed to parse ttn-solid2d-server resonse: {}'
                  .format(respond.content))
            raise
          self.ui_predict.value = str(out['predict_time'])
          self.plot(out['x'], out['y'], out['u'], out['v'])
          self.ui_render.value = str(time.time() - render_start)
        
  def display(self, verbose=False):
    if verbose:
      display(self.ui_rtt, self.ui_predict, self.ui_render)
    if not hasattr(self, 'ui'):
      self.ui = interactive(self.update, t=self.ui_time)
      self.ui_output = self.ui.children[-1]
    return self.ui