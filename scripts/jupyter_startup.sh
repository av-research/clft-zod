#!/bin/bash

# Start Jupyter Lab
exec jupyter lab \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --allow-root \
    --ServerApp.token='' \
    --ServerApp.password='' \
    --ServerApp.disable_check_xsrf=True \
    --ServerApp.allow_origin='*' \
    --ServerApp.notebook_dir='/workspace' \
    --ServerApp.base_url='/' \
    --log-level=INFO
