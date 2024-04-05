#!/bin/bash

# Default
python plotter_vh.py ZH/samples_withSF_nocuts_UL18_dR_HighStats_EMu.py ZH/plots_forCardsEMu_dR_CommonCut.txt -l 59.9 --systFile ZH/systs_fullcorr_MC_EMuNoJec.py --toLoad /eos/cms/store/group/phys_exotica/SUEPs/ZH_Histos/EMu_18_CommonBounds_Fixed --plotdir  /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/EMu_18_CommonBounds_Fixed --plotAll --strict-order ;
wait

python plotter_vh.py ZH/samples_withSF_nocuts_UL17_dR_HighStats_EMu.py ZH/plots_forCardsEMu_dR_CommonCut.txt -l 41.6 --systFile ZH/systs_fullcorr_MC_EMuNoJec.py --toLoad /eos/cms/store/group/phys_exotica/SUEPs/ZH_Histos/EMu_17_CommonBounds_Fixed --plotdir  /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/EMu_17_CommonBounds_Fixed --plotAll --strict-order ;
wait

python plotter_vh.py ZH/samples_withSF_nocuts_UL16_dR_HighStats_EMu.py ZH/plots_forCardsEMu_dR_CommonCut.txt -l 16.4 --systFile ZH/systs_fullcorr_MC_EMuNoJec.py --toLoad /eos/cms/store/group/phys_exotica/SUEPs/ZH_Histos/EMu_16_CommonBounds_Fixed --plotdir  /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/EMu_16_CommonBounds_Fixed --plotAll --strict-order ;
wait

python plotter_vh.py ZH/samples_withSF_nocuts_UL16APV_dR_HighStats_EMu.py ZH/plots_forCardsEMu_dR_CommonCut.txt -l 19.9 --systFile ZH/systs_fullcorr_MC_EMuNoJec.py --toLoad /eos/cms/store/group/phys_exotica/SUEPs/ZH_Histos/EMu_16APV_CommonBounds_Fixed --plotdir  /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/EMu_16APV_CommonBounds_Fixed --plotAll --strict-order ;
wait

python plotter_vh.py ZH/samples_withSF_nocuts_RunII_dR_HighStats_EMu.py ZH/plots_forCardsEMu_dR_CommonCut.txt -l 137.8 --systFile ZH/systs_fullcorr_MC_EMuNoJec.py --toLoad /eos/cms/store/group/phys_exotica/SUEPs/ZH_Histos/EMu_{YEAR}_CommonBounds_Fixed --plotdir  /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/EMu_RunII_CommonBounds_Fixed --plotAll --strict-order ;
wait