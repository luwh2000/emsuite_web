USER="rluu"
REMOTE="brown.rcac.purdue.edu"
IDENTITY="~/.ssh/id_rsa"

remote_command() {
    ssh -i $IDENTITY $USER@$REMOTE "$1"
}

remote_command "touch $1"
