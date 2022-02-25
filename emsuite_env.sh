#!/bin/bash

module load miniconda38
source /apps/miniconda38/etc/profile.d/conda.sh
conda activate ~jjyang/.conda/envs/emsuite_web
python manage.py runserver 0.0.0.0:8199

