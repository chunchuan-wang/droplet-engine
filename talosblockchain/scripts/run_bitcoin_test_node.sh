bitcoind -daemon -regtest -dnsseed=0 -addnode=$1 -datadir=$2 -server -rpcuser="talos" -rpcpassword="talos" -debug -txindex
