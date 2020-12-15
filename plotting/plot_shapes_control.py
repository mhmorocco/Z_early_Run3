#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Dumbledraw.dumbledraw as dd
import Dumbledraw.rootfile_parser_inputshapes as rootfile_parser
import Dumbledraw.styles as styles
import ROOT

import argparse
import copy
import yaml
import os

import logging
logger = logging.getLogger("")
from multiprocessing import Pool
from multiprocessing import Process
import multiprocessing
def parse_arguments():
    parser = argparse.ArgumentParser(
        description=
        "Plot categories using Dumbledraw from shapes produced by shape-producer module."
    )
    parser.add_argument(
        "-l", "--linear", action="store_true", help="Enable linear x-axis")
    parser.add_argument("-e", "--era", type=str, required=True, help="Era")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="ROOT file with shapes of processes")
    parser.add_argument(
        "--variables",
        type=str,
        default=None,
        help="Enable control plotting for given variable")
    parser.add_argument(
        "--category-postfix",
        type=str,
        default=None,
        help="Enable control plotting for given category_postfix. Structure of a category: <variable>_<postfix>")
    parser.add_argument(
        "--channels",
        type=str,
        default=None,
        help="Enable control plotting for given variable")
    parser.add_argument(
        "--normalize-by-bin-width",
        action="store_true",
        help="Normelize plots by bin width")
    parser.add_argument(
        "--fake-factor",
        action="store_true",
        help="Fake factor estimation method used")
    parser.add_argument(
        "--embedding",
        action="store_true",
        help="Fake factor estimation method used")
    parser.add_argument(
        "--draw-jet-fake-variation",
        type=str,
        default=None,
        help="Draw variation of jetFakes or QCD in derivation region.")

    return parser.parse_args()


def setup_logging(output_file, level=logging.DEBUG):
    logger.setLevel(level)
    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    file_handler = logging.FileHandler(output_file, "w")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def main(info):

    #add NMSSM masses to plot
    mass_dict= yaml.load(open("shapes/mass_dict_nmssm.yaml"), Loader=yaml.Loader)["plots"]

    args = info["args"]
    variable = info["variable"]
    channel = info["channel"]
    channel_dict = {
        "ee": "#font[42]{#scale[0.85]{ee}}",
        "em": "#scale[0.85]{e}#mu",
        "et": "#font[42]{#scale[0.85]{e}}#tau_{#font[42]{h}}",
        "mm": "#mu#mu",
        "mt": "#mu#tau_{#font[42]{h}}",
        "tt": "#tau_{#font[42]{h}}#tau_{#font[42]{h}}"
    }
    if args.linear == True:
        split_value = 0.1
    else:
        if args.normalize_by_bin_width:
            split_value = 10001
        else:
            split_value = 101

    split_dict = {c: split_value for c in ["et", "mt", "tt", "em", "mm"]}

    bkg_processes = [
        "VVL", "TTL", "ZL", "jetFakesEMB", "EMB", "HTT" ] #"ggH125", "qqH125"
   
    if not args.fake_factor and args.embedding:
        bkg_processes = [
            "QCDEMB", "VVL", "VVJ", "W", "TTL", "TTJ", "ZJ", "ZL", "EMB"
        ]
    if not args.embedding and args.fake_factor:
        bkg_processes = [
            "VVT", "VVL", "TTT", "TTL", "ZL", "jetFakes", "ZTT"
        ]
    if not args.embedding and not args.fake_factor:
        bkg_processes = [
            "QCD", "VVT", "VVL", "VVJ", "W", "TTT", "TTL", "TTJ", "ZJ", "ZL", "ZTT"
        ]
    if args.draw_jet_fake_variation is not None:
        bkg_processes = [
            "VVL", "TTL", "ZL", "EMB"
        ]
        if not args.fake_factor and args.embedding:
            bkg_processes = [
                "VVL", "VVJ", "W", "TTL", "TTJ", "ZJ", "ZL", "EMB"
            ]
        if not args.embedding and args.fake_factor:
            bkg_processes = [
                "VVT", "VVL", "TTT", "TTL", "ZL", "ZTT"
            ]
        if not args.embedding and not args.fake_factor:
            bkg_processes = [
                "VVT", "VVL", "VVJ", "W", "TTT", "TTL", "TTJ", "ZJ", "ZL", "ZTT"
            ]
    all_bkg_processes = [b for b in bkg_processes]
    legend_bkg_processes = copy.deepcopy(bkg_processes)
    legend_bkg_processes.reverse()
    if "2016" in args.era:
        era = "Run2016"
    elif "2017" in args.era:
        era = "Run2017"
    elif "2018" in args.era:
        era = "Run2018"
    else:
        logger.critical("Era {} is not implemented.".format(args.era))
        raise Exception

    category = "_".join([channel, variable])
    if args.category_postfix is not None:
        category += "_%s"%args.category_postfix
    rootfile = rootfile_parser.Rootfile_parser(args.input, variable)
    bkg_processes = [b for b in all_bkg_processes]
    if "em" in channel:
        if not args.embedding:
            bkg_processes = [
                "QCD", "VVT", "VVL", "W", "TTT", "TTL", "ZL", "ZTT"
            ]
        if args.embedding:
            bkg_processes = [
                "QCDEMB", "VVL", "W", "TTL", "ZL", "EMB"
            ]
        if args.draw_jet_fake_variation is not None:
            if not args.embedding:
                bkg_processes = [
                    "VVT", "VVL", "W", "TTT", "TTL", "ZL", "ZTT"
                ]
            if args.embedding:
                bkg_processes = [
                    "VVL", "W", "TTL", "ZL", "EMB"
                ]

    if "mm" in channel:
        bkg_processes = [
            "QCD", "VVT", "VVL", "W", "TTT", "TTL", "ZTT", "ZL"
        ]

    legend_bkg_processes = copy.deepcopy(bkg_processes)
    legend_bkg_processes.reverse()

    # create plot
    width = 600
    if args.linear == True:
        plot = dd.Plot(
            [0.3, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14, width=width)
    else:
        plot = dd.Plot(
            [0.5, [0.3, 0.28]], "ModTDR", r=0.04, l=0.14, width=width)

    # get background histograms
    total_bkg = None
    if args.draw_jet_fake_variation is None:
        stype = "Nominal"
    else:
        stype = args.draw_jet_fake_variation
    for index,process in enumerate(bkg_processes):
        if index == 0:
            total_bkg = rootfile.get(channel, process, args.category_postfix,shape_type=stype).Clone()
            plot.add_hist(
                    rootfile.get(channel, process,args.category_postfix, shape_type=stype), process, "bkg")
        else:
            if process=="HTT":
                HTT=rootfile.get(channel, "ggH125",args.category_postfix, shape_type=stype).Clone()
                HTT.Add(rootfile.get(channel, "qqH125",args.category_postfix, shape_type=stype))
                total_bkg.Add(HTT)     
                plot.add_hist(HTT,"HTT","bkg")       
            else:
                total_bkg.Add(rootfile.get(channel, process,args.category_postfix, shape_type=stype))
                plot.add_hist(
                    rootfile.get(channel, process,args.category_postfix, shape_type=stype), process, "bkg")
        
        plot.setGraphStyle(
            process, "hist", fillcolor=styles.color_dict[process])    

    plot.add_hist(total_bkg, "total_bkg")
    plot.setGraphStyle(
        "total_bkg",
        "e2",
        markersize=0,
        fillcolor=styles.color_dict["unc"],
        linecolor=0)

    plot.add_hist(rootfile.get(channel, "data", args.category_postfix,shape_type=stype), "data_obs")
    data_norm = plot.subplot(0).get_hist("data_obs").Integral()
    plot.subplot(0).get_hist("data_obs").GetXaxis().SetMaxDigits(4)
    plot.subplot(0).setGraphStyle("data_obs", "e0")
    plot.subplot(0).setGraphStyle("data_obs", "e0")
    if args.linear:
        pass
    else:
        plot.subplot(1).setGraphStyle("data_obs", "e0")
    
    NMSSM_rfile_dict={}
    NMSSM_bkg_dict={}

    if "mm" not in channel:
        # get signal histograms
        for heavy_mass in mass_dict["heavy_mass"]:
            light_masses = mass_dict["light_mass_coarse"] if heavy_mass > 1001 else mass_dict["light_mass_fine"]
            for light_mass in light_masses:
                if light_mass+125<heavy_mass:
                    NMSSM_rfile_dict["NMSSM_{heavy_mass}_125_{light_mass}".format(heavy_mass=heavy_mass,light_mass=light_mass)] = rootfile.get(
                            channel, "NMSSM_{heavy_mass}_125_{light_mass}".format(heavy_mass=heavy_mass,light_mass=light_mass), args.category_postfix).Clone()
                    

        plot_idx_to_add_signal = [0,2] if args.linear else [1,2]
        for i in plot_idx_to_add_signal:
            for nmssm_signals in NMSSM_rfile_dict:
                if NMSSM_rfile_dict[nmssm_signals].Integral() > 0:
                    NMSSM_scale = 10
                else:
                    NMSSM_scale = 0.0                        
                if i in [0,1]: 
                    NMSSM_rfile_dict[nmssm_signals].Scale(NMSSM_scale)
                plot.subplot(i).add_hist(NMSSM_rfile_dict[nmssm_signals], 
                    nmssm_signals)
                plot.subplot(i).add_hist(NMSSM_rfile_dict[nmssm_signals], 
                    nmssm_signals+"_top")

    if "mm" not in channel:
        for nmssm_signals in NMSSM_rfile_dict:
            plot.subplot(0 if args.linear else 1).setGraphStyle(
                        nmssm_signals, "hist", linecolor=styles.color_dict[nmssm_signals], linewidth=3)
            plot.subplot(0 if args.linear else 1).setGraphStyle(nmssm_signals+"_top", "hist", linecolor=0)

    NMSSM_top=[]
    NMSSM_top_bkg=[]
    for nmssm_signals in NMSSM_rfile_dict:
        NMSSM_top.append(nmssm_signals+"_top")
        NMSSM_top_bkg.append("bkg_"+nmssm_signals+"_top")
    # assemble ratio
    if "mm" not in channel:
        for nmssm_signals in NMSSM_rfile_dict:
            NMSSM_bkg_dict["bkg_"+nmssm_signals]  = plot.subplot(2).get_hist(nmssm_signals)
            NMSSM_bkg_dict["bkg_"+nmssm_signals].Add(plot.subplot(2).get_hist("total_bkg"))            
            plot.subplot(2).add_hist(NMSSM_bkg_dict["bkg_"+nmssm_signals], "bkg_"+nmssm_signals)
            plot.subplot(2).add_hist(NMSSM_bkg_dict["bkg_"+nmssm_signals], "bkg_"+nmssm_signals+"_top")
            plot.subplot(2).setGraphStyle(
                        "bkg_"+nmssm_signals,
                        "hist",
                        linecolor=styles.color_dict[nmssm_signals],
                        linewidth=3)
            plot.subplot(2).setGraphStyle(
                        "bkg_"+nmssm_signals+"_top",
                        "hist", linecolor=0)
        plot.subplot(2).normalize([
                        "total_bkg", "data_obs"] + NMSSM_bkg_dict.keys()+NMSSM_top_bkg, "total_bkg")
    else:
        plot.subplot(2).normalize(["total_bkg", "data_obs"], "total_bkg")

    # stack background processes
    plot.create_stack(bkg_processes, "stack")

    # normalize stacks by bin-width
    if args.normalize_by_bin_width:
        plot.subplot(0).normalizeByBinWidth()
        plot.subplot(1).normalizeByBinWidth()

    # set axes limits and labels
    plot.subplot(0).setYlims(
        split_dict[channel],
        max(2 * plot.subplot(0).get_hist("data_obs").GetMaximum(),
            split_dict[channel] * 2))

    log_quantities = ["ME_ggh", "ME_vbf", "ME_z2j_1", "ME_z2j_2", "ME_q2v1", "ME_q2v2", "ME_vbf_vs_ggh", "ME_ggh_vs_Z"]
    if variable in log_quantities:
        plot.subplot(0).setLogY()
        plot.subplot(0).setYlims(
            1.0,
            1000 * plot.subplot(0).get_hist("data_obs").GetMaximum())

    plot.subplot(2).setYlims(0.75, 1.45)
    if channel == "mm":
        plot.subplot(0).setLogY()
        plot.subplot(0).setYlims(1, 10**10)

    if args.linear != True:
        plot.subplot(1).setYlims(0.1, split_dict[channel])
        plot.subplot(1).setYlabel(
            "")  # otherwise number labels are not drawn on axis
        plot.subplot(1).setLogY()
    if variable != None:
        if variable in styles.x_label_dict[channel]:
            x_label = styles.x_label_dict[channel][
                variable]
        else:
            x_label = variable
        plot.subplot(2).setXlabel(x_label)
    else:
        plot.subplot(2).setXlabel("NN output")
    if args.normalize_by_bin_width:
        plot.subplot(0).setYlabel("dN/d(NN output)")
    else:
        plot.subplot(0).setYlabel("N_{events}")

    plot.subplot(2).setYlabel("")
    plot.subplot(2).setGrid()
    plot.scaleYLabelSize(0.8)
    plot.scaleYTitleOffset(1.1)

    category = ""
    if not channel == "tt" and category in ["11", "12", "13", "14", "15", "16"]:
        plot.subplot(2).changeXLabels(["0.2", "0.4", "0.6", "0.8", "1.0"])


    # draw subplots. Argument contains names of objects to be drawn in corresponding order.
  
    if "mm" not in channel:
        # procs_to_draw = ["stack", "total_bkg", "ggH", "ggH_top", "qqH", "qqH_top", "VH", "VH_top", "ttH", "ttH_top", "data_obs"] if args.linear else ["stack", "total_bkg", "data_obs"]
        procs_to_draw = ["stack", "total_bkg" ,"data_obs"]+NMSSM_rfile_dict.keys()+NMSSM_top if args.linear else ["stack", "total_bkg", "data_obs"]
        if args.draw_jet_fake_variation is not None:
            procs_to_draw = ["stack", "total_bkg", "data_obs"]
        plot.subplot(0).Draw(procs_to_draw)
        if args.linear != True:
            plot.subplot(1).Draw([
                "stack", "total_bkg", "ggH", "ggH_top", "qqH", "qqH_top","data_obs"])
        if args.draw_jet_fake_variation is None:
            plot.subplot(2).Draw(["total_bkg", "data_obs"]+NMSSM_bkg_dict.keys()+NMSSM_top_bkg)
        else:
            plot.subplot(2).Draw([
                "total_bkg", "data_obs"
            ])
    else:
        procs_to_draw = ["stack", "total_bkg", "data_obs"] if args.linear else ["stack", "total_bkg", "data_obs"]
        plot.subplot(0).Draw(procs_to_draw)
        if args.linear != True:
            plot.subplot(1).Draw([
                "stack", "total_bkg", "data_obs"
            ])
        plot.subplot(2).Draw([
            "total_bkg", "data_obs"
        ])


    # create legends
    suffix = ["", "_top"]
    for i in range(2):
        plot.add_legend(width=0.625, height=0.15)
        for process in legend_bkg_processes:
            plot.legend(i).add_entry(
                0, process, styles.legend_label_dict[process.replace("TTL", "TT").replace("VVL", "VV").replace("NLO","")], 'f')

        plot.legend(i).add_entry(0, "total_bkg", "Bkg. stat. unc.", 'f')
        if "mm" not in channel and args.draw_jet_fake_variation is None:
            for nmssm_signals in NMSSM_rfile_dict:
                plot.legend(i).add_entry(0 if args.linear else 1, nmssm_signals+suffix[i], "H("+nmssm_signals[nmssm_signals.find("_")+1:nmssm_signals.find("125")-1]+")#rightarrowh(125)h'("+nmssm_signals[nmssm_signals.find("125")+4:]+")" , 'l')
        plot.legend(i).add_entry(0, "data_obs", "Observed", 'PE2L')
        plot.legend(i).setNColumns(2)
    plot.legend(0).Draw()
    plot.legend(1).setAlpha(0.0)
    plot.legend(1).Draw()

    for i in range(2):
        plot.add_legend(
            reference_subplot=2, pos=1, width=0.6, height=0.03)
        plot.legend(i + 2).add_entry(0, "data_obs", "Observed", 'PE2L')

        #add NMSSM legend in ratio plot
        # if "mm" not in channel and args.draw_jet_fake_variation is None:
        #     for nmssm_signals in NMSSM_rfile_dict:
        #         plot.legend(i + 2).add_entry(0 if args.linear else 1, nmssm_signals+suffix[i],
        #                                 nmssm_signals+"bkg.", 'l')
        plot.legend(i + 2).add_entry(0, "total_bkg", "Bkg. stat. unc.", 'f')
        plot.legend(i + 2).setNColumns(4)
    plot.legend(2).Draw()
    plot.legend(3).setAlpha(0.0)
    plot.legend(3).Draw()
    
    #draw scale text
    signal_cs=NMSSM_scale*0.1
    plot.DrawText(0.16, 0.8, "\sigma_{\mathrm{signal}}=%s\,\mathrm{pb}" %signal_cs,textsize=0.024)
    # draw additional labels
    plot.DrawCMS()
    if "2016" in args.era:
        plot.DrawLumi("35.9 fb^{-1} (2016, 13 TeV)")
    elif "2017" in args.era:
        plot.DrawLumi("41.5 fb^{-1} (2017, 13 TeV)")
    elif "2018" in args.era:
        plot.DrawLumi("59.7 fb^{-1} (2018, 13 TeV)")
    else:
        logger.critical("Era {} is not implemented.".format(args.era))
        raise Exception

    posChannelCategoryLabelLeft = None
    plot.DrawChannelCategoryLabel(
        "%s, %s" % (channel_dict[channel], "{cat}".format(cat=args.category_postfix)),
        begin_left=posChannelCategoryLabelLeft)

    # save plot
    if not args.embedding and not args.fake_factor:
        postfix = "fully_classic"
    if args.embedding and not args.fake_factor:
        postfix = "emb_classic"
    if not args.embedding and args.fake_factor:
        postfix = "classic_ff"
    if args.embedding and args.fake_factor:
        postfix = "emb_ff"
    if args.draw_jet_fake_variation is not None:
        postfix = postfix + "_" + args.draw_jet_fake_variation

    if not os.path.exists("plots/%s_plots_%s"%(args.era,postfix)):
        os.mkdir("plots/%s_plots_%s"%(args.era,postfix))
    if not os.path.exists("plots/%s_plots_%s/%s"%(args.era,postfix,channel)):
        os.mkdir("plots/%s_plots_%s/%s"%(args.era,postfix,channel))
    print "Trying to save the created plot"
    plot.save("plots/%s_plots_%s/%s/%s_%s_%s_%s.%s" % (args.era, postfix, channel, args.era, channel, variable, args.category_postfix, "pdf"))
    plot.save("plots/%s_plots_%s/%s/%s_%s_%s_%s.%s" % (args.era, postfix, channel, args.era, channel, variable, args.category_postfix, "png"))


if __name__ == "__main__":
    args = parse_arguments()
    setup_logging("{}_plot_shapes.log".format(args.era), logging.DEBUG)
    variables = args.variables.split(",")
    channels = args.channels.split(",")
    infolist = []

    if not args.embedding and not args.fake_factor:
        postfix = "fully_classic"
    if args.embedding and not args.fake_factor:
        postfix = "emb_classic"
    if not args.embedding and args.fake_factor:
        postfix = "classic_ff"
    if args.embedding and args.fake_factor:
        postfix = "emb_ff"

    if not os.path.exists("%s_plots_%s"%(args.era,postfix)):
        os.mkdir("%s_plots_%s"%(args.era,postfix))
    for ch in channels:
        if not os.path.exists("%s_plots_%s/%s"%(args.era,postfix,ch)):
            os.mkdir("%s_plots_%s/%s"%(args.era,postfix,ch))
        for v in variables:
            infolist.append({"args" : args, "channel" : ch, "variable" : v})
    pool = Pool(1)
    pool.map(main, infolist)
    # for info in infolist:
    #     main(info)



