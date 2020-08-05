ttn-solid2d-ipynb
=================

Try
---

[![Jupyter Notebook](https://mybinder.org/badge_logo.svg)][binder]

> Notice that it will take a few moments for Binder to install the Python 
> environment. Also the application itself will be far less responsive then it
> would be if ran on a local computer. The delays are mainly caused by the 
> network communications between the TTN prediction server (Google Cloud Run), 
> the Python kernel (Binder), and the user's PC. Feel free to enable the verbose
> mode setting `verbose=True` to see how much time the application spends in the 
> different stages. The prediction itself usually takes only a few milliseconds
> while request and rendering both take significantly longer (around two orders 
> of magnitude).

Build
-----

```bash
conda create -n ttn-solid2d-ipynb python=3.6
conda activate ttn-solid2d-ipynb
conda install -c conda-forge jupyterlab
conda install -c conda-forge nodejs
conda install -c conda-forge matplotlib
conda install -c conda-forge ipywidgets
jupyter labextension install @jupyter-widgets/jupyterlab-manager
```

Run
---

```bash
conda activate ttn-solid2d-ipynb
jupyter lab
```

[binder]: https://beta.mybinder.org/v2/gh/lukas-koschmieder/ttn-solid2d-ipynb/master?filepath=ttn-solid2d.ipynb
