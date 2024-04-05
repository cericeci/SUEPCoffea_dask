#!/bin/bashwait

python datacardMaker.py ZH/samples_withSF_nocuts_UL18_dR_HighStats.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards_CommonBounds/CRTT_Rebinned/2018 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/CRTT_18_CommonBounds_Rebin/leadclustertracks --var leadclustertracks --ABCD --year 2018 --region CRTT --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL17_dR_HighStats.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards_CommonBounds/CRTT_Rebinned/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/CRTT_17_CommonBounds_Rebin/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region CRTT --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16_dR_HighStats.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards_CommonBounds/CRTT_Rebinned/2016 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/CRTT_16_CommonBounds_Rebin/leadclustertracks --var leadclustertracks --ABCD --year 2016 --region CRTT --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16APV_dR_HighStats.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards_CommonBounds/CRTT_Rebinned/2016APV --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/CRTT_16APV_CommonBounds_Rebin/leadclustertracks --var leadclustertracks --ABCD --year 2016APV --region CRTT --doAll --floatB ;
wait