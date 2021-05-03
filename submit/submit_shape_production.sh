#!/bin/bash

ERA=$1
CHANNEL=$2
PROCESSES=$3
SUBMIT_MODE=$4
TAG=$5
CONTROL=$6

[[ ! -z $1 && ! -z $2 && ! -z $3 && ! -z $4  && ! -z $5 ]] || ( echo "[ERROR] Number of given parameters is to small."; exit 1 )
[[ ! -z $6 ]] || CONTROL=0
CONTROL_ARG=""
if [[ $CONTROL == 1 ]]
then
    CONTROL_ARG="--control-plots"
fi

source utils/setup_nmssm_samples.sh 
source utils/setup_samples.sh $ERA $CHANNEL
source utils/setup_root.sh
source utils/bashFunctionCollection.sh

IFS="," read -a PROCS_ARR <<< $PROCESSES
PROCESSES=""
for PROC in ${PROCS_ARR[@]};
do
    if [[ "$PROC" =~ "backgrounds1" ]]
    then
        BKG_PROCS1="data,emb"
        PROCESSES="$PROCESSES,$BKG_PROCS1"    
    elif [[ "$PROC" =~ "backgrounds2" ]]
    then
        BKG_PROCS2="ttt,ttl,ttj"
        PROCESSES="$PROCESSES,$BKG_PROCS2"    
    elif [[ "$PROC" =~ "backgrounds3" ]]
    then
        BKG_PROCS3="ztt,zl,zj"
        PROCESSES="$PROCESSES,$BKG_PROCS3"
    elif [[ "$PROC" =~ "backgrounds4" ]]
    then
        BKG_PROCS4="vvt,vvl,vvj,w"
        PROCESSES="$PROCESSES,$BKG_PROCS4" 
    elif [[ "$PROC" =~ "sm_signals" ]]
    then
        SIG_PROCS="ggh,qqh,tth,vh"
        PROCESSES="$PROCESSES,$SIG_PROCS"
    elif [[ "$PROC" =~ "nmssm_split1" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT1"
    elif [[ "$PROC" =~ "nmssm_split2" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT2"
    elif [[ "$PROC" =~ "nmssm_split3" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT3"
    elif [[ "$PROC" =~ "nmssm_split4" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT4"
    elif [[ "$PROC" =~ "nmssm_split5" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT5"
    elif [[ "$PROC" =~ "nmssm_split6" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT6"
    elif [[ "$PROC" =~ "nmssm_split7" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT7"
    elif [[ "$PROC" =~ "nmssm_split8" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT8"
    elif [[ "$PROC" =~ "nmssm_split9" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT9"
    elif [[ "$PROC" =~ "nmssm_split_10" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT10"
    elif [[ "$PROC" =~ "nmssm_split_11" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT11"
    elif [[ "$PROC" =~ "nmssm_split_12" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT12"
    elif [[ "$PROC" =~ "nmssm_split_13" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT13"
    elif [[ "$PROC" =~ "nmssm_split_14" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT14"
    elif [[ "$PROC" =~ "nmssm_split_15" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT15"
    elif [[ "$PROC" =~ "nmssm_split_16" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT16"
    elif [[ "$PROC" =~ "nmssm_split_17" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT17"
    elif [[ "$PROC" =~ "nmssm_split_18" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT18"
    elif [[ "$PROC" =~ "nmssm_split_19" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT19"
    elif [[ "$PROC" =~ "nmssm_split_20" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_SPLIT20"
    elif [[ "$PROC" =~ "nmssm_mH1000" ]]
    then
        PROCESSES="$PROCESSES,$NMSSM_mH1000"
    elif [[ "$PROC" =~ "all" ]]
    then
        echo "all"
        BKG_PROCS1="data,emb"
        BKG_PROCS2="ttt,ttl,ttj"
        BKG_PROCS3="ztt,zl,zj"
        BKG_PROCS4="vvt,vvl,vvj,w"
        SIG_PROCS="ggh,qqh,tth,vh"
        PROCESSES="$BKG_PROCS1,$BKG_PROCS2,$BKG_PROCS3,$BKG_PROCS4,$SIG_PROCS,$NMSSM_SPLIT1,$NMSSM_SPLIT2,$NMSSM_SPLIT3,$NMSSM_SPLIT4,$NMSSM_SPLIT5,$NMSSM_SPLIT6,$NMSSM_SPLIT7,$NMSSM_SPLIT8,$NMSSM_SPLIT9,$NMSSM_SPLIT10,$NMSSM_SPLIT11,$NMSSM_SPLIT12,$NMSSM_SPLIT13,$NMSSM_SPLIT14,$NMSSM_SPLIT15,$NMSSM_SPLIT16,$NMSSM_SPLIT17,$NMSSM_SPLIT18,$NMSSM_SPLIT19,$NMSSM_SPLIT20"
        echo $PROCESSES
    else
        echo "[INFO] Add selection of single process $PROC"
        PROCESSES="$PROCESSES,$PROC"
    fi
done

# Remove introduced leading comma again.
PROCESSES=$(sort_string ${PROCESSES#,})

if [[ "$SUBMIT_MODE" == "multigraph" ]]
then
    echo "[ERROR] Not implemented yet."
    exit 1
elif [[ "$SUBMIT_MODE" == "singlegraph" ]]
then
    echo "[INFO] Preparing graph for processes $PROCESSES for submission..."
    OUTPUT=output/submit_files/${ERA}-${CHANNEL}-${PROCS_ARR[@]}-${CONTROL}-${TAG}
    [[ ! -d $OUTPUT ]] && mkdir -p $OUTPUT
    echo $OUTPUT
    echo $PROCESSES
    python shapes/produce_shapes_condor.py --channels $CHANNEL \
        			    --output-file dummy.root \
        			    --directory $ARTUS_OUTPUTS \
                                    --et-friend-directory $SVFit_Friends $NNScore_Friends $FF_Friends $HHKinFit_Friends \
                                    --mt-friend-directory $SVFit_Friends $NNScore_Friends $FF_Friends $HHKinFit_Friends \
                                    --tt-friend-directory $SVFit_Friends $NNScore_Friends $FF_Friends $HHKinFit_Friends \
                                    --era $ERA \
                                    --proc_arr ${PROCS_ARR[@]} \
                                    --optimization-level 1 \
                                    --process-selection $PROCESSES \
                                    --only-create-graphs \
                                    --graph-dir $OUTPUT \
                                    --tag $TAG
                                    $CONTROL_ARG
    # # Set output graph file name produced during graph creation.
    GRAPH_FILE=${OUTPUT}/analysis_unit_graphs-${TAG}-${ERA}-${CHANNEL}-${PROCS_ARR[@]}.pkl
    [[ $CONTROL == 1 ]] && GRAPH_FILE=${OUTPUT}/control_unit_graphs-${ERA}-${CHANNEL}-${PROCS_ARR[@]}.pkl
    # # Prepare the jdl file for single core jobs.
    echo "[INFO] Creating the logging direcory for the jobs..."
    GF_NAME=$(basename $GRAPH_FILE)
    if [[ ! -d log/condorShapes/${TAG}/${GF_NAME%.pkl}/ ]]
    then
        mkdir -p log/condorShapes/${TAG}/${GF_NAME%.pkl}/
    fi
    if [[ ! -d log/${GF_NAME%.pkl}/ ]]
    then
        mkdir -p log/${GF_NAME%.pkl}/
    fi

    echo "[INFO] Preparing submission file for single core jobs for variation pipelines..."
    cp submit/produce_shapes_cc7.jdl $OUTPUT
    echo "output = log/condorShapes/${TAG}/${GF_NAME%.pkl}/\$(cluster).\$(Process).out" >> $OUTPUT/produce_shapes_cc7.jdl
    echo "error = log/condorShapes/${TAG}/${GF_NAME%.pkl}/\$(cluster).\$(Process).err" >> $OUTPUT/produce_shapes_cc7.jdl
    echo "log = log/condorShapes/${TAG}/${GF_NAME%.pkl}/\$(cluster).\$(Process).log" >> $OUTPUT/produce_shapes_cc7.jdl
    echo "queue a3,a2,a1 from $OUTPUT/arguments.txt" >> $OUTPUT/produce_shapes_cc7.jdl
    
    # # Prepare the multicore jdl.
    echo "[INFO] Preparing submission file for multi core jobs for nominal pipeline..."
    cp submit/produce_shapes_cc7.jdl $OUTPUT/produce_shapes_cc7_multicore.jdl
    # Replace the values in the config which differ for multicore jobs.
    sed -i '/^RequestMemory/c\RequestMemory = 5000' $OUTPUT/produce_shapes_cc7_multicore.jdl
    sed -i '/^RequestCpus/c\RequestCpus = 8' $OUTPUT/produce_shapes_cc7_multicore.jdl
    sed -i '/^arguments/c\arguments = $(a1) $(a2) $(a3) $(a4)' ${OUTPUT}/produce_shapes_cc7_multicore.jdl
    # Add log file locations to output file.
    echo "output = log/condorShapes/${TAG}/${GF_NAME%.pkl}/multicore.\$(cluster).\$(Process).out" >> $OUTPUT/produce_shapes_cc7_multicore.jdl
    echo "error = log/condorShapes/${TAG}/${GF_NAME%.pkl}/multicore.\$(cluster).\$(Process).err" >> $OUTPUT/produce_shapes_cc7_multicore.jdl
    echo "log = log/condorShapes/${TAG}/${GF_NAME%.pkl}/multicore.\$(cluster).\$(Process).log" >> $OUTPUT/produce_shapes_cc7_multicore.jdl
    echo "queue a3,a2,a4,a1 from $OUTPUT/arguments_multicore.txt" >> $OUTPUT/produce_shapes_cc7_multicore.jdl

    # Assemble the arguments.txt file used in the submission
    python submit/prepare_args_file.py --graph-file $GRAPH_FILE --output-dir $OUTPUT --pack-multiple-pipelines 20
    echo "[INFO] Submit shape production with 'condor_submit $OUTPUT/produce_shapes_cc7.jdl' and 'condor_submit $OUTPUT/produce_shapes_cc7_multicore.jdl'"
    condor_submit $OUTPUT/produce_shapes_cc7.jdl
    condor_submit $OUTPUT/produce_shapes_cc7_multicore.jdl
else
    echo "[ERROR] Given mode $SUBMIT_MODE is not supported. Aborting..."
    exit 1
fi
