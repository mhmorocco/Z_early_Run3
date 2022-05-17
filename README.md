
Framework to produce analysis histograms (shapes)

Before cloning the early Run3 analysis framework start the ssh agent:
```bash
eval $(ssh-agent)
ssh-add
```
Àfterwards checkout the early Run3 analysis framework:
```bash
git clone --recursive git@github.com:KIT-CMS/Z_early_Run3.git
```
1. setup the environment
```bash
source utils/setup_root.sh
```
2. For producing control shapes for ```m_vis``` an example command is:
```bash
python shapes/produce_shapes.py --channels mm --output-file output/run3_crown_2018_mm --directory /ceph/rschmieder/run3/CROWN_tutorial/ntuples  --era 2018 --num-processes 2 --num-threads 2 --optimization-level 1 --control-plots --control-plot-set m_vis --ntuple_type crown --mm-friend-directory /ceph/rschmieder/run3/CROWN_tutorial/friends/crosssection
```
3. For plotting the control shapes use:
```bash
bash plotting/plot_shapes_control.sh 2018 output/run3_crown_2018_mm.root m_vis mm run3_tut
```
