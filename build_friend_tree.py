import ROOT
import argparse
import yaml
import os
import time
import glob
from tqdm import tqdm
from multiprocessing import Pool, current_process, RLock


def base_filename(path):
    return path.split("/")[-3]


def job_wrapper(args):
    print(args)
    return friend_producer(*args)


def friend_producer(rfile, dataset_proc):
    # output_path = rfile.replace("ntuples", "friends/crosssection")
    output_path = rfile.replace(
        "/storage/gridka-nrg/moh/CROWN_samples/EarlyRun3_V00/CROWNRun",
        "/ceph/moh/CROWN_samples/EarlyRun3_V00/friends/crosssection",
    )
    os.makedirs(output_path, exist_ok=False)
    rdf = ROOT.RDataFrame("ntuple", rfile)
    numberGeneratedEventsWeight = 1 / float(dataset_proc["nevents"])
    crossSectionPerEventWeight = float(dataset_proc["xsec"])
    rdf = rdf.Define(
        "numberGeneratedEventsWeight",
        "(float){ngw}".format(ngw=numberGeneratedEventsWeight),
    )
    rdf = rdf.Define(
        "crossSectionPerEventWeight",
        "(float){xsec}".format(xsec=crossSectionPerEventWeight),
    )
    rdf.Snapshot(
        "ntuple",
        output_path,
        ["numberGeneratedEventsWeight", "crossSectionPerEventWeight"],
    )


def generate_friend_trees(dataset, ntuples, nthreads):
    arguments = [(ntuple, dataset[base_filename(ntuple)]) for ntuple in ntuples]
    pool = Pool(nthreads, initargs=(RLock(),), initializer=tqdm.set_lock)
    for _ in tqdm(
        pool.imap_unordered(job_wrapper, arguments),
        total=len(arguments),
        desc="Total progess",
        position=nthreads + 1,
        dynamic_ncols=True,
        leave=True,
    ):
        pass


if __name__ == "__main__":
    # base_path = "ntuples/2018/*/*/*.root"
    # dataset = yaml.load(open("datasets.yaml"), Loader=yaml.Loader)
    # base_path = "/ceph/rschmieder/run3/CROWN_tutorial/ntuples/2018/*/*/*.root"
    # dataset = yaml.load(open("dataset_tut.yml"), Loader=yaml.Loader)

    base_path = "/storage/gridka-nrg/moh/CROWN_samples/EarlyRun3_V00/CROWNRun/2018/*/*/*.root"
    dataset = yaml.load(open("datasets.yaml"), Loader=yaml.Loader)

    ntuples = glob.glob(base_path)
    ntuples_wo_data = ntuples.copy()
    for ntuple in ntuples:
        if "Run201" in ntuple:
            ntuples_wo_data.remove(str(ntuple))
    nthreads = 2
    if nthreads > len(ntuples_wo_data):
        nthreads = len(ntuples_wo_data)
    generate_friend_trees(dataset, ntuples_wo_data, nthreads)
