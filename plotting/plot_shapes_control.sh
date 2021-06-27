source utils/setup_cvmfs_sft.sh
source utils/setup_python.sh

ERA=$1
INPUT=$2
#variable to plot
v="pt_1"
for ch in "mt" "et" "tt"
do
    plotting/plot_shapes_control.py -l --era Run${ERA} --input $INPUT --variables ${v} --channels ${ch} --embedding --fake-factor --blinded
done
