from ntuple_processor import Histogram
from ntuple_processor.utils import Selection
import logging
import yaml

m_sv_hist = Histogram("m_sv_puppi", "m_sv_puppi", [i for i in range(0, 255, 5)])
mt_tot_hist = Histogram("mt_tot_puppi", "mt_tot_puppi", [i for i in range(0, 3900, 10)])

fine_binning=[0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]
et_hist = Histogram("et_max_score", "et_max_score", fine_binning)
mt_hist = Histogram("mt_max_score", "mt_max_score", fine_binning)
tt_hist = Histogram("tt_max_score", "tt_max_score", fine_binning)
em_hist = Histogram("em_max_score", "em_max_score", fine_binning)

#classdict for NMSSM Index
def nmssm_cat(channel,cdict):
        def readclasses():
                confFileName = "{clsdict}".format(clsdict=cdict)
                #logger.debug("Parse classes from " + confFileName)
                confdict = yaml.load(open(confFileName, "r"), Loader=yaml.Loader)
                classdict = {}
                for nnclass in set(confdict["classes"]):
                        classdict[nnclass] = confdict["classes"].index(nnclass)

                return classdict
        def hist():
                if channel=="et":
                        return et_hist
                elif channel=="mt":
                        return mt_hist
                else:
                        return tt_hist
        classdict=readclasses()
        print(classdict)
        nmssm_categorization={"{ch}".format(ch=channel) : []}
        catsL_=nmssm_categorization["{ch}".format(ch=channel)]
        for label in classdict.keys():               
                catsL_.append(
                        (Selection(name="{lab}".format(lab=label),  cuts=[("{ch}_max_index=={index}".format(ch=channel, index=classdict[label]), "category_selection")]),   [hist()]))
        nmssm_categorization={"{ch}".format(ch=channel) : catsL_}
        return nmssm_categorization
