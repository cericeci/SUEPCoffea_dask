systematicsAndShapes = {
 "yields": { # This always needs to be defined
           "name": "yields",
           "type": "yieldsWithShapes",
           "file": "[ROOTFILE]_[CHANNEL].root",
           "match": "[VAR]_[CHANNEL]_$PROCESS",
           "extendedABCD": {"SR": "_SR", "B1": "_B1", "B2":"_B2", "C1":"_C1", "C2":"_C2", "D1":"_D1", "D2":"_D2","E1":"_E1", "E2":"_E2"}
 },
 "TrigSF"  : {
            "name": "TrigSF",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"2016":["2016"], "2016APV":["2016APV"], "2017":["2017"],"2018":["2018"]},
 },
 "ElSF"  : {
            "name": "ElSF",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "MuSF"  : {
            "name": "MuSF",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "PU"  : {
            "name": "PU",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "L1"  : {
            "name": "L1",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"2016":["2016","2016APV"],"2017":["2017"]},
 },
 "ISR"  : {
            "name": "ISR",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "FSR"  : {
            "name": "FSR",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "LFCorr"  : {
            "name": "LFCorr",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "LFUnCorr"  : {
            "name": "LFUnCorr",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"2016":["2016"], "2016APV":["2016APV"],"2017":["2017"], "2018":["2018"]},

 },
 "HFCorr"  : {
            "name": "HFCorr",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "HFUnCorr"  : {
            "name": "HFUnCorr",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"2016":["2016"], "2016APV":["2016APV"],"2017":["2017"], "2018":["2018"]},
 },
 "Track"  : {
            "name": "Track",
            "type": "shape",
            "processes": [".*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Up",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "JES"  : {
            "name": "JES",
            "type": "shape",
            "processes": ["SUEP.*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "JER"  : {
            "name": "JER",
            "type": "shape",
            "processes": ["SUEP.*"],
            "match": "$PROCESS_$SYSTEMATIC",
            "up"  : "Up",
            "down": "Dn",
            "corrs": {"RunII":["2016","2016APV","2017","2018"]},
 },
 "lumi_2016"  : {
            "name": "lumi",
            "type": "lnN",
            "processes": [".*"],
            "size": 1.01,
            "corrs": {"2016":["2016","2016APV"]},
 },
 "lumi_2017"  : {
            "name": "lumi",
            "type": "lnN",
            "processes": [".*"],
            "size": 1.02,
            "corrs": {"2017":["2017"]},
 },
 "lumi_2018"  : {
            "name": "lumi",
            "type": "lnN",
            "processes": [".*"],
            "size": 1.015,
            "corrs": {"2018":["2018"]},
 },
 "lumi_RunII"  : {
            "name": "lumi",
            "type": "lnN",
            "processes": [".*"],
            "size": {"RunII":[1.006,1.006,1.009, 1.02]},
            "corrs": {"RunII":["2016","2016APV", "2017", "2018"]},
 },
 "lumi_20172018"  : {
            "name": "lumi",
            "type": "lnN",
            "processes": [".*"],
            "size": {"RunII":[1.006, 1.002]},
            "corrs": {"RunII":["2017", "2018"]},
 },
 "closure" : {
            "name": "closure",
            "type": "lnN",
            "processes": [".*"],
            "size": 1.2,
 },
# "DYnorm": {
#            "name": "lumi",
#            "type": "lnN",
#            "processes": ["DY.*"],
#            "size": 1.2,
# },
# "ttnorm": {
#            "name": "lumi",
#            "type": "lnN",
#            "processes": ["TT.*"],
#            "size": 1.2,
# },
# "VVnorm": {
#            "name": "lumi",
#            "type": "lnN",
#            "processes": ["VV.*"],
#            "size": 1.2,
# },
}
