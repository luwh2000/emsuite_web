#!/bin/bash

module load miniconda38
source /apps/miniconda38/etc/profile.d/conda.sh
conda activate emsuite_web
python manage.py runserver 0.0.0.0:8199

#completed file:c09e8682-d047-432d-b93a-ee79a5cb6ee1
#http://kiharalab.org:8200/
