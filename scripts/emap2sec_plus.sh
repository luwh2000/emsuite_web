#!/bin/bash

#SBATCH --time=24:00:00

# $1 is id(with dashes) of the file
TRIM_ID=$(echo "$1" | tr -cd [:alnum:])
sql_update_start="UPDATE emap2sec_plus SET status=2 WHERE id=\"$TRIM_ID\""
sqlite3 db.sqlite3 "$sql_update_start"

USER="dklab"
REMOTE="brown.rcac.purdue.edu"
IDENTITY="~/.ssh/dklab_rcac_id_ecdsa"
WD="/depot/dkihara/data/dklab/emsuite/emap2secplus"
SD="/scratch/brown/dklab/emsuite/emap2secplus"

remote_cp_tx() {
    scp -i $IDENTITY $1 $USER@$REMOTE:$SD/$2
}

remote_cp_rx() {
    scp -i $IDENTITY $USER@$REMOTE:$SD/$1 $2
}

remote_sh() {
    ssh -i $IDENTITY $USER@$REMOTE "cd $WD; $1"
}
sql="SELECT map_file,contour,type,resize FROM emap2sec_plus WHERE id=\"$TRIM_ID\""
params=$(sqlite3 db.sqlite3 "$sql")

mapfile=$(echo $params | awk -F '|' '{print "media/" $1}')
bn=$(basename -- "$mapfile")
ext="${bn##*.}"
filename=$1.$ext
solved_filename=$1.pdb

contour=$(echo $params | awk -F '|' '{printf "%g", $2}')
type=$(echo $params | awk -F '|' '{print $3}')
#type_args=("-gnorm" "-lnorm")
resize=$(echo $params | awk -F '|' '{print $4}')


solved_structure=$(echo $params | awk -F '|' '{print "media/" $6}')

remote_cp_tx $mapfile input/$filename
remote_cp_tx $solved_structure solved/$solved_filename
#run_command="./run.sh input/$filename output/$1.pdb -c $contour -sstep $sstep -vw $vw ${norm_args[$norm]} solved/$1.pdb verification/$solved_filename $TRIM_ID"
run_command="echo 'hello'"
echo $run_command
remote_sh "$run_command"
remote_cp_rx output/$1.pdb media/emap2secplus/output/$1.pdb
echo "copied"
if [ -s "media/emap2secplus/output/$1.pdb" ]; then
    sql_update_end="UPDATE emap2sec_plus SET status=3 WHERE id=\"$TRIM_ID\""
else
    sql_update_end="UPDATE emap2sec_plus SET status=4 WHERE id=\"$TRIM_ID\""
fi

sqlite3 db.sqlite3 "$sql_update_end"