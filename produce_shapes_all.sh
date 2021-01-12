ulimit -s unlimited
 
for era in 2016 2017 2018
do
    for channel in  et mt tt
    do
        echo $era $channel
        mkdir output/uncert_shapes/${era}-${channel}-control-shapes
        python shapes/produce_shapes.py --channels ${channel} --output-file output/uncert_shapes/${era}-${channel}-control-shapes/shapes-analysis-${era}-${channel} --directory /ceph/jbechtel/nmssm/ntuples/${era}/${channel}/ --${channel}-friend-directory /ceph/jbechtel/nmssm/friends/${era}/${channel}/SVFit/ /ceph/rschmieder/nmssm/friends/${era}/${channel}/FakeFactors_nmssm/ /ceph/jbechtel/nmssm/friends/${era}/${channel}/HHKinFit/ /ceph/jbechtel/nmssm/friends/${era}/${channel}/NNScore_train_all/NNScore_workdir/500_3/NNScore_workdir/NNScore_collected/ --era ${era} --num-processes 5 --num-threads 4 --optimization-level 1 --control-plot-set ${channel}_max_score 

        bash shapes/do_estimations.sh ${era} output/uncert_shapes/${era}-${channel}-control-shapes/shapes-analysis-${era}-${channel}.root 0

        python shapes/convert_to_synced_shapes.py --era ${era} --input output/uncert_shapes/${era}-${channel}-control-shapes/shapes-analysis-${era}-${channel}.root --output output/uncert_shapes/synced_shapes
        
        hadd output/uncert_shapes/synced_shapes/${era}-${channel}-synced-NMSSM.root output/uncert_shapes/synced_shapes/${era}-${channel}-synced-NMSSM*
    done
done
