#!/bin/bash

python datacardMaker.py ZH/samples_withSF_nocuts_UL18_dR_HighStats.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards_OptimalBounds/CRTT/2018 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/CRTT_18_OptimalBounds/leadclustertracks --var leadclustertracks --ABCD --year 2018 --region CRTT --floatB --doAll ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL17_dR_HighStats.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards_OptimalBounds/CRTT/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/CRTT_17_OptimalBounds/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region CRTT --floatB --doAll ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16_dR_HighStats.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards_OptimalBounds/CRTT/2016 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/CRTT_16_OptimalBounds/leadclustertracks --var leadclustertracks --ABCD --year 2016 --region CRTT --floatB --doAll ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16APV_dR_HighStats.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards_OptimalBounds/CRTT/2016APV --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/CRTT_16APV_OptimalBounds/leadclustertracks --var leadclustertracks --ABCD --year 2016APV --region CRTT --floatB --doAll ;
wait
