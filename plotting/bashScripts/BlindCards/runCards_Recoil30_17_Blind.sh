#!/bin/bash

python datacardMaker.py ZH/samples_withSF_nocuts_UL17.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards/Blind/Recoil30/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/Recoil30_17/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region SR --thispoint SUEP_hadronic_mS125_mD3.00_T3.00 --floatB --blind ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL17.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards/Blind/Recoil30/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/Recoil30_CRDY_17/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region CRDY --thispoint SUEP_hadronic_mS125_mD3.00_T3.00 --floatB --blind ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL17.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards/Blind/Recoil30/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/Recoil30_CRTT_17/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region CRTT --thispoint SUEP_hadronic_mS125_mD3.00_T3.00 --floatB --blind ;
wait