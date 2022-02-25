#!/bin/bash

module load miniconda38
source /apps/miniconda38/etc/profile.d/conda.sh
conda activate emsuite_web
python manage.py runserver 0.0.0.0:8199
