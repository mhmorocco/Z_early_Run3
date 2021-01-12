#!/bin/bash
ulimit -s unlimited
ERA=$1

#DIR=$2

source utils/setup_root.sh

# if [[ ! -d $DIR ]]
# then
#     echo "[ERROR] Given directory does not exist. Aborting..."
#     exit 1
# fi

for ch in et mt tt
do
for ERA in 2016 2017 2018
do
for FILE in  /ceph/rschmieder/nmssm/friends/${ERA}/${ch}/FakeFactors_nmssm/{D,EW,Emb,ST,TT,VV,W{[1-4],J,W,Z},ZZ}*/*.root
do
BASE=$(basename $FILE)
FILENAME=${BASE%.root}
echo ${BASE}
python utility/do_pipeline_manipulations.py -i ${FILE} -r /ceph/jbechtel/nmssm/ntuples/${ERA}/${ch}/${FILENAME}/${BASE} -c ${ch} 

done
done
done

