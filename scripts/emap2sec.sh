#!/bin/bash

TRIM_ID=$(echo "$1" | tr -cd [:alnum:])
sql_update_start="UPDATE emap2sec SET status=2 WHERE id=\"$TRIM_ID\""
sqlite3 db.sqlite3 "$sql_update_start"

USER="rluu"
REMOTE="brown.rcac.purdue.edu"
IDENTITY="~/.ssh/id_rsa"
WD="/home/rluu/emap2sec"

remote_cp_tx() {
    scp -i $IDENTITY $1 $USER@$REMOTE:$WD/$2
}

remote_cp_rx() {
    scp -i $IDENTITY $USER@$REMOTE:$WD/$1 $2
}

remote_sh() {
    ssh -i $IDENTITY $USER@$REMOTE "cd $WD; $1"
}

sql="SELECT mrc_file,contour,sstep,vw,norm FROM emap2sec WHERE id=\"$TRIM_ID\""
params=$(sqlite3 db.sqlite3 "$sql")

mapfile=$(echo $params | awk -F '|' '{print "media/" $1}')
bn=$(basename -- "$mapfile")
ext="${bn##*.}"
filename=$1.$ext

contour=$(echo $params | awk -F '|' '{printf "%g", $2}')
sstep=$(echo $params | awk -F '|' '{print $3}')
vw=$(echo $params | awk -F '|' '{print $4}')
norm=$(echo $params | awk -F '|' '{print $5}')
norm_args=("-gnorm" "-lnorm")

remote_cp_tx $mapfile input/$filename
run_command="./run.sh input/$filename output/$1.pdb -c $contour -sstep $sstep -vw $vw ${norm_args[$norm]}"
echo $run_command
remote_sh "$run_command"
remote_cp_rx output/$1.pdb media/emap2sec/output/$1.pdb

if [ -f "output/$1.pdb" ]; then
    sql_update_end="UPDATE emap2sec SET status=3 WHERE id=\"$TRIM_ID\""
else
    sql_update_end="UPDATE emap2sec SET status=4 WHERE id=\"$TRIM_ID\""
fi

sqlite3 db.sqlite3 "$sql_update_end"

