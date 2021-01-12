#!/usr/bin/env python
from __future__ import print_function
import argparse

import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.ROOT.EnableImplicitMT(8)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True,
                        help="Input root file with friend trees.")
    parser.add_argument("-r", "--reference", required=True,
                        help="Reference root file with directories")
    parser.add_argument("-c", "--channels", nargs="*",
                        help="Channels for which structure should be reflected")
    parser.add_argument("--for-removal", action="store_true",
                        help="Print list of additional pipelines instead of adding them.")
    return parser.parse_args()


def get_folders(rootfile, channels):
    folder_set = [fold.GetName() for fold in rootfile.GetListOfKeys()]
    folders = []
    for folder in folder_set:
        if folder.split("_")[0] in channels:
            folders.append(folder)
    return folders


def main(args):
    if args.for_removal:
        ref_file = ROOT.TFile(args.reference, "READ")
        in_file = ROOT.TFile(args.input, "UPDATE")
        ref_folders = set(get_folders(ref_file, args.channels))
        in_folders = set(get_folders(in_file, args.channels))
        if ref_folders < in_folders:
            for folder in in_folders - ref_folders:
                print(folder)
    else:
        ref_file = ROOT.TFile(args.reference, "READ")
        in_file = ROOT.TFile(args.input, "UPDATE")
        ref_folders = set(get_folders(ref_file, args.channels))
        in_folders = set(get_folders(in_file, args.channels))
        print("Checking file {} for missing pipelines".format(args.input))
        if in_folders < ref_folders:
            for folder in ref_folders - in_folders:
                print(in_file)
                print("Creating directory {}".format(folder))
                print("Trying to get input {}".format("_".join([folder.split("_")[0], "nominal"]) + "/ntuple"))
                nominal_tree = in_file.Get("_".join([folder.split("_")[0], "nominal"]) + "/ntuple")
                print(nominal_tree)
                in_file.mkdir(folder)
                in_file.cd(folder)
                #emptytree=ROOT.TTree("ntuple","empty")
                #tree=emptytree  
                tree = nominal_tree.CopyTree("")           
                tree.Write()
        else:
            print("Nothing to do here.")
        in_file.Write()
        in_file.Close()
        ref_file.Close()
    return


if __name__ == "__main__":
    args = parse_args()
    main(args)
