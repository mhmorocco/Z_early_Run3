for era in 2016 2017 2018
do
    for channel in et mt tt
    do
        echo $era $channel
        python shapes/produce_shapes.py --channels ${channel} --output-file output/shapes/${era}-${channel}-control-shapes/shapes-analysis-${era}-${channel} --directory /ceph/jbechtel/nmssm/ntuples/${era}/${channel}/ --${channel}-friend-directory /ceph/jbechtel/nmssm/friends/${era}/${channel}/SVFit/ /ceph/jbechtel/nmssm/friends/${era}/${channel}/FakeFactors_nmssm/ /ceph/jbechtel/nmssm/friends/${era}/${channel}/HHKinFit/ /ceph/jbechtel/nmssm/friends/${era}/${channel}/NNScore_retrain_cutonChi2/NNScore_workdir/NNScore_collected/ --era ${era} --num-processes 4 --num-threads 3 --optimization-level 1 --control-plots --skip-systematic-variations --control-plot-set mjj,pt_1,pt_2,m_vis,ptvis,m_sv_puppi,jpt_1,njets,jdeta,mjj,dijetpt,bpt_bReg_1,bpt_bReg_2,jpt_2,mbb_highCSV_bReg,pt_bb_highCSV_bReg,m_ttvisbb_highCSV_bReg,kinfit_mH,kinfit_mh2,kinfit_chi2,nbtag,bm_bReg_1,bm_bReg_2,bcsv_1,bcsv_2,highCSVjetUsedFordiBJetSystemCSV
        bash shapes/do_estimations.sh ${era} output/shapes/${era}-${channel}-control-shapes/shapes-analysis-${era}-${channel}.root 0
    done
done

