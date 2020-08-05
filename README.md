ttn-solid2d-ipynb
=================

Try
---

[![Jupyter Notebook](https://mybinder.org/badge_logo.svg)][binder]

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
