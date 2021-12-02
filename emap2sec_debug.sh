#!/bin/bash
# $1 is id(with dashes) of the file
TRIM_ID=$(echo "$1" | tr -cd [:alnum:])
sql_update_start="UPDATE emap2sec SET status=2 WHERE id=\"$TRIM_ID\""
sqlite3 db.sqlite3 "$sql_update_start"

USER="lu677"
REMOTE="brown.rcac.purdue.edu"
IDENTITY="~/.ssh/id_rsa.pub"
WD="/home/lu677/emsuite/emap2sec"

remote_cp_tx() {
    scp $1 $USER@$REMOTE:$WD/$2
}

remote_cp_rx() {
    scp $USER@$REMOTE:$WD/$1 $2
}

remote_sh() {
    ssh $USER@$REMOTE "cd $WD; $1"
}
sql="SELECT map_file,contour,sstep,vw,norm,solved_structure FROM emap2sec WHERE id=\"$TRIM_ID\""
params=$(sqlite3 db.sqlite3 "$sql")

mapfile=$(echo $params | awk -F '|' '{print "media/" $1}')
bn=$(basename -- "$mapfile")
ext="${bn##*.}"
filename=$1.$ext
solved_filename=$1.pdb

contour=$(echo $params | awk -F '|' '{printf "%g", $2}')
sstep=$(echo $params | awk -F '|' '{print $3}')
vw=$(echo $params | awk -F '|' '{print $4}')
norm=$(echo $params | awk -F '|' '{print $5}')
norm_args=("-gnorm" "-lnorm")
solved_structure=$(echo $params | awk -F '|' '{print "media/" $6}')

echo $mapfile
echo $filename
remote_cp_tx $mapfile input/$filename
remote_cp_tx $solved_structure solved/$solved_filename
run_command="./run.sh input/$filename output/$1.pdb -c $contour -sstep $sstep -vw $vw ${norm_args[$norm]} solved/$1.pdb verification/$solved_filename $TRIM_ID"
echo $run_command
remote_sh "$run_command"
remote_cp_rx output/$1.pdb media/emap2sec/output/$1.pdb

if [ -s "media/emap2sec/output/$1.pdb" ]; then
    sql_update_end="UPDATE emap2sec SET status=3 WHERE id=\"$TRIM_ID\""
else
    sql_update_end="UPDATE emap2sec SET status=4 WHERE id=\"$TRIM_ID\""
fi

sqlite3 db.sqlite3 "$sql_update_end"
