#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Name of the environment
ENV_NAME="PyWRF"

echo "Creating conda environment: $ENV_NAME"
conda create -y -n $ENV_NAME python=3.10

echo "Activating environment: $ENV_NAME"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate $ENV_NAME

echo "Installing packages into $ENV_NAME..."
conda install -y notebook
conda install -y -c conda-forge wrf-python
conda install -y -c conda-forge netcdf4
conda install -y -c conda-forge cartopy
conda install -y -c conda-forge basemap

echo "Installation complete. To activate the environment, run:"
echo "conda activate $ENV_NAME"
