#!/usr/bin/env bash

conda install -y \
    bokeh \
    cython \
    graphviz \
    holoviews \
    ipywidgets \
    jupyter \
    jupyterlab \
    matplotlib \
    networkx \
    nodejs \
    numpy \
    pandas \
    plotly \
    psutil \
    psycopg2 \
    python=3.6 \
    scipy \
    scikit-learn \
    seaborn \
    sympy \
;

conda install -y -c plotly plotly-orca

pip install credstash

jupyter serverextension enable --py jupyterlab
jupyter nbextension enable --py widgetsnbextension
jupyter labextension install \
        @jupyter-widgets/jupyterlab-manager \
        jupyter-matplotlib \
        jupyterlab_bokeh \
        @pyviz/jupyterlab_pyviz \
        @jupyterlab/plotly-extension \
        @mflevine/jupyterlab_html
