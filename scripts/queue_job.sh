#!/bin/bash

# $1 : Job ID (e.g. 6bdd5322-e45f-4c1a-b9a3-fa089748c1df)
# $2 : Job type (e.g. emap2sec)

ID=$(echo "$2" | tr -cd [:alnum:])
sqlite3 db.sqlite3 >> tmp/params/$ID <<EOF
SELECT mrc_file,contour,sstep,vw,norm FROM $1 WHERE id="$ID";
EOF

# module load slurm

# sbatch
# scripts/$2.sh ~/$1
