#!/bin/bash

python datacardMaker.py ZH/samples_withSF_nocuts_UL17.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/0JetVeto_17/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region SR --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL17_CR.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/CRDY_17/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region CRDY --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL17_CR.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2017 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/CRTT_17/leadclustertracks --var leadclustertracks --ABCD --year 2017 --region CRTT --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL18.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2018 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/0JetVeto_18/leadclustertracks --var leadclustertracks --ABCD --year 2018 --region SR --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL18_CR.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2018 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/CRDY_18/leadclustertracks --var leadclustertracks --ABCD --year 2018 --region CRDY --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL18_CR.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2018 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/CRTT_18/leadclustertracks --var leadclustertracks --ABCD --year 2018 --region CRTT --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2016 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/0JetVeto_16/leadclustertracks --var leadclustertracks --ABCD --year 2016 --region SR --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16_CR.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2016 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/CRDY_16/leadclustertracks --var leadclustertracks --ABCD --year 2016 --region CRDY --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16_CR.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2016 --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/CRTT_16/leadclustertracks --var leadclustertracks --ABCD --year 2016 --region CRTT --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16APV.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2016APV --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/0JetVeto_16APV/leadclustertracks --var leadclustertracks --ABCD --year 2016APV --region SR --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16APV_CR.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2016APV --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/CRDY_16APV/leadclustertracks --var leadclustertracks --ABCD --year 2016APV --region CRDY --doAll --floatB ;
wait

python datacardMaker.py ZH/samples_withSF_nocuts_UL16APV_CR.py ZH/systs_fullcorr.py /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisCards_0JetVeto/2016APV --rootfile /eos/user/g/gdecastr/SUEPCoffea_dask/doAnalysisPlots/CRTT_16APV/leadclustertracks --var leadclustertracks --ABCD --year 2016APV --region CRTT --doAll --floatB ;
wait