#!/usr/bin/env python
import os
import sys
import argparse
import glob
import json
import logging

import ROOT

from FWCore.PythonUtilities.LumiList import LumiList


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Extract processed lumi sections.')

    parser.add_argument('inputFiles', type=str, nargs='*', help='Input files')
    parser.add_argument('--log',nargs='?',type=str,const='INFO',default='INFO',choices=['INFO','DEBUG','WARNING','ERROR','CRITICAL'],help='Log level for logger')

    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    loglevel = getattr(logging,args.log)
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', level=loglevel, datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr)

    lumiTree = 'LumiTree'
    treeDir  = 'miniTree'

    allfiles = []
    for f in args.inputFiles:
        for fname in glob.glob(f):
            allfiles += [fname]

    logging.info('Adding {0} files to tchain'.format(len(allfiles)))
    tchain = ROOT.TChain('{0}/{1}'.format(treeDir,lumiTree))
    for fname in allfiles:
        tchain.Add(fname)

    nlumis = tchain.GetEntries()
    logging.info('Processing {0} lumis'.format(nlumis))
    allLumis = {}
    total = 0
    for row in tchain:
        total += 1
        if row.run not in allLumis: allLumis[row.run] = set()
        allLumis[row.run].add(row.lumi)

    lumiJson = LumiList(runsAndLumis = allLumis)
    #lumiJson.writeJSON(args.outputFile)
    print lumiJson
    

if __name__ == "__main__":
    status = main()
    sys.exit(status)

