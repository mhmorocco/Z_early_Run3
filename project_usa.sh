#!/bin/sh

 if [ $1 == 'ok' ]
 then
     echo please enter a variable
     read variable
     echo enter lower bound
     read lower_bound
     echo enter upper bound
     read upper_bound
     listy=""

    for ((i=0; i<=39; i++))
    do
        var=$(printf %.4f $(echo "($lower_bound+$i*($upper_bound-$lower_bound)/40)" | bc -l));
        listy+="$var,"
    done
    #edge
    var=$(printf %.4f $(echo "($lower_bound+$i*($upper_bound-$lower_bound)/40)" | bc -l));
    listy+="$var"
    echo $listy
    export variable
    #listy is actually a string
    export x="$listy"
    #############################################################
    #mm channel
    #python shapes/produce_shapes.py --channels mm --output-file output/earlyRun3_crown_2018_mm --directory /storage/gridka-nrg/moh/CROWN_samples/EarlyRun3_V00/CROWNRun --mm-friend-directory /ceph/moh/CROWN_samples/EarlyRun3_V00/friends/crosssection --era 2018 --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --control-plot-set $variable --ntuple_type crown --skip-systematic-variations
    #ee channel
    #python shapes/produce_shapes.py --channels ee --output-file output/earlyRun3_crown_2018_ee --directory /storage/gridka-nrg/moh/CROWN_samples/EarlyRun3_V00/CROWNRun --ee-friend-directory /ceph/moh/CROWN_samples/EarlyRun3_V00/friends/crosssection --era 2018 --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --control-plot-set $variable --ntuple_type crown --skip-systematic-variations
    #mmet channel
    #python shapes/produce_shapes.py --channels mmet --output-file output/earlyRun3_crown_2018_mmet --directory /storage/gridka-nrg/moh/CROWN_samples/EarlyRun3_V00/CROWNRun --mmet-friend-directory /ceph/moh/CROWN_samples/EarlyRun3_V00/friends/crosssection --era 2018 --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --control-plot-set $variable --ntuple_type crown --skip-systematic-variations
    #emet channel
    python shapes/produce_shapes.py --channels emet --output-file output/earlyRun3_crown_2018_emet --directory /storage/gridka-nrg/moh/CROWN_samples/EarlyRun3_V00/CROWNRun --emet-friend-directory /ceph/moh/CROWN_samples/EarlyRun3_V00/friends/crosssection --era 2018 --num-processes 4 --num-threads 4 --optimization-level 1 --control-plots --control-plot-set $variable --ntuple_type crown --skip-systematic-variations
    #############################################################
 else
     echo nope
fi