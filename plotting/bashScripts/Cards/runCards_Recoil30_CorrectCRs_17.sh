#!/bin/bash

python datacardMaker.py ZH/samples_withSF_nocuts_UL17.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards/Recoil30_CorrectCRs_Replay/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/Recoil30_17/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region SR --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL17.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards/Recoil30_CorrectCRs_Replay/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/Recoil30_CRDY_17/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region CRDY --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL17.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/Cards/Recoil30_CorrectCRs_Replay/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/Plots/Recoil30_CRTT_17/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region CRTT --doAll --floatB ;
wait