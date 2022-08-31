set -ex

HASH=`ipfs add -r ./docs -Q`
echo ${HASH}

ipfs name publish ${HASH}

