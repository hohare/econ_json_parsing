# Set up path for python

export MYROOT=$(pwd)
export PYTHONPATH=$PYTHONPATH:$MYROOT
alias python="python3" # use python3 by default

alias startdb="mongod --dbpath /usr/local/var/mongodb --logpath /usr/local/var/log/mongodb/mongo.log --fork"
