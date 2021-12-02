#!/bin/bash

TRIM_ID=$(echo "$1" | tr -cd [:alnum:])
sql_update_start="UPDATE mainmast SET status=2 WHERE id=\"$TRIM_ID\""
sqlite3 db.sqlite3 "$sql_update_start"

USER="lu677"
REMOTE="brown.rcac.purdue.edu"
IDENTITY="~/.ssh/id_rsa"
WD="/home/lu677/emap2sec"

remote_cp_tx() {
    scp -i $IDENTITY $1 $USER@$REMOTE:$WD/$2
}

remote_cp_rx() {
    scp -i $IDENTITY $USER@$REMOTE:$WD/$1 $2
}

remote_sh() {
    ssh -i $IDENTITY $USER@$REMOTE "cd $WD; $1"
}

sql="SELECT map_file,gw,t,allow,filter,merge,Rlocal,Nround,Nnb,Ntb,Dkeep,Const FROM mainmast WHERE id=\"$TRIM_ID\""
params=$(sqlite3 db.sqlite3 "$sql")

mapfile=$(echo $params | awk -F '|' '{print "media/" $1}')
bn=$(basename -- "$mapfile")
ext="${bn##*.}"
filename=$1.$ext

gw=$(echo $params | awk -F '|' '{printf "%g", $2}')
t=$(echo $params | awk -F '|' '{print $3}')
allow=$(echo $params | awk -F '|' '{print $4}')
filter=$(echo $params | awk -F '|' '{print $5}')
merge=$(echo $params | awk -F '|' '{print $6}')
Rlocal=$(echo $params | awk -F '|' '{print $7}')
Nround=$(echo $params | awk -F '|' '{print $8}')
Nnb=$(echo $params | awk -F '|' '{print $9}')
Ntb=$(echo $params | awk -F '|' '{print $10}')
Dkeep=$(echo $params | awk -F '|' '{print $11}')
Const=$(echo $params | awk -F '|' '{print $12}')

remote_cp_tx $mapfile input/$filename
run_command="./run.sh input/$filename output/$1.pdb -gw $gw -t $t -allow $allow -filter $filter -merge $merge -Rlocal $Rlocal -Nround $Nround -Nnb $Nnb -Ntb $Ntb -Dkeep $Dkeep -Const $Const"
echo $run_command
remote_sh "$run_command"
remote_cp_rx output/$1.pdb media/mainmast/output/$1.pdb

if [ -f "media/mainmast/output/$1.pdb" ]; then
    sql_update_end="UPDATE mainmast SET status=3 WHERE id=\"$TRIM_ID\""
else
    sql_update_end="UPDATE mainmast SET status=4 WHERE id=\"$TRIM_ID\""
fi

sqlite3 db.sqlite3 "$sql_update_end"

