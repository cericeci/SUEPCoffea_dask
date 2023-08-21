import ROOT

def cut(x):
  return (x["njets"] >= 0) 

plots = {
  "ntracks": {
             "name"     : "ntracks",
             "bins"     : ["uniform", 15, 0, 500],
             "channel"  : "onecluster",
             "value"    : lambda x, y : (x["ntracks"], y*cut(x)),
             "logY"     : True,
             "normalize": True,
             "maxY"     : 100,
             "minY"     : .001,
             "ratiomaxY": 10,
             "ratiominY": 0,
             "plotname" : "ntracks",
             "xlabel"   : "N_{tracks}",
             "vars"     : ["ntracks"]
  },
  "leadclustertracks": {
             "name"     : "leadclustertracks",
             "bins"     : ["uniform", 15, 0, 250],
             "channel"  : "onecluster",
             "value"    : lambda x, y : (x["leadcluster_ntracks"], y*cut(x)),
             "logY"     : True,
             "normalize": True,
             "maxY"     : 100,
             "minY"     : .001,
             "ratiomaxY": 10,
             "ratiominY": 0,
             "plotname" : "leadclustertracks",
             "xlabel"   : "N_{tracks}^{SUEP}",
             "vars"     : ["leadcluster_ntracks"]
  },
}

 