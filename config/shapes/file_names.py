common_files_2018 = {
    "DY": [
        "DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8",
        "DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
        "DY1JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
        "DY2JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
        "DY3JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
        "DY4JetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8",
    ],
    "TT": [
        "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
        "TTToHadronic_TuneCP5_13TeV-powheg-pythia8",
        "TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8",
    ],
    "VV": [
        "WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
        "WW_TuneCP5_13TeV-pythia8",
        "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",
        "WZ_TuneCP5_13TeV-pythia8",
        "ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8",
        "ZZTo4L_TuneCP5_13TeV_powheg_pythia8",
        "ZZ_TuneCP5_13TeV-pythia8",
        "ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
        "ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8",
        "ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
        "ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8",
    ],
    "W": [
        "W1JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
        "W2JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
        "W3JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
        "W4JetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
        "WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8",
    ],
}

files = {
    "2018": {
        "mm": dict(
            {
                "data": [
                    "DoubleMuon_Run2018A",
                    "DoubleMuon_Run2018B",
                    "DoubleMuon_Run2018C",
                    "DoubleMuon_Run2018D",
                ],
            },
            **common_files_2018
        ),
    },
}
