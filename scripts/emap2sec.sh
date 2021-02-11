USER="rluu"
REMOTE="brown.rcac.purdue.edu"
IDENTITY="~/.ssh/id_rsa"
WD="/home/rluu/emap2sec"

remote_cp() {
    scp -i $IDENTITY $1 $USER@$REMOTE:$WD/$2
}

remote_sh() {
    ssh -i $IDENTITY $USER@$REMOTE "cd $WD; $1"
}

params=cat $1

get_param() {
    $params
}

echo $(get_param id)

