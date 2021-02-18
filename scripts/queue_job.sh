#!/bin/bash

# $1 : Job type (e.g. emap2sec)
# $2 : Job ID (e.g. 6bdd5322-e45f-4c1a-b9a3-fa089748c1df)

TRIM_ID=$(echo "$2" | tr -cd [:alnum:])

module load slurm
sbatch -o logs/$2 scripts/$1.sh $2

sql_update="UPDATE $1 SET status=1 WHERE id=\"$TRIM_ID\""
sqlite3 db.sqlite3 "$sql_update"

