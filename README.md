ttn-solid2d-ipynb
=================

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
