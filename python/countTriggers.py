# import ROOT in batch mode
import sys
oldargv = sys.argv[:]
sys.argv = [ '-b-' ]
import ROOT
ROOT.gROOT.SetBatch(True)
sys.argv = oldargv

# load FWLite C++ libraries
ROOT.gSystem.Load("libFWCoreFWLite.so");
ROOT.gSystem.Load("libDataFormatsFWLite.so");
ROOT.FWLiteEnabler.enable()

# load FWlite python libraries
from DataFormats.FWLite import Handle, Events

triggerBits, triggerBitLabel = Handle("edm::TriggerResults"), ("TriggerResults","","HLT")
triggerObjects, triggerObjectLabel  = Handle("std::vector<pat::TriggerObjectStandAlone>"), "selectedPatTrigger"
triggerPrescales, triggerPrescaleLabel  = Handle("pat::PackedTriggerPrescales"), "patTrigger"

events = Events("root://cmsxrootd.fnal.gov//store/data/Run2016B/MET/MINIAOD/PromptReco-v2/000/273/158/00000/06A9DFDA-201A-E611-858F-02163E0136F7.root")

triggerCounts = {}

for iev,event in enumerate(events):
    event.getByLabel(triggerBitLabel, triggerBits)
    event.getByLabel(triggerObjectLabel, triggerObjects)
    event.getByLabel(triggerPrescaleLabel, triggerPrescales)

    if iev%1000 ==1: print 'Processing event {0}'.format(iev)

    names = event.object().triggerNames(triggerBits.product())
    for i in xrange(triggerBits.product().size()):
        if names.triggerName(i) not in triggerCounts: triggerCounts[names.triggerName(i)] = 0
        if triggerBits.product().accept(i): triggerCounts[names.triggerName(i)] += 1

import operator
sorted_triggerCounts = sorted(triggerCounts.items(), key=operator.itemgetter(1))
for pair in sorted_triggerCounts:
    print pair
