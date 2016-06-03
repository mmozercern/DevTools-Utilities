import os
import sys
import argparse
import glob
import json

import ROOT

from FWCore.PythonUtilities.LumiList import LumiList


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Extract processed lumi sections.')

    parser.add_argument('inputFiles', type=str, nargs='*', help='Input files')
    parser.add_argument('-o','--outputFile', type=str, default='processedLumis.json', help='Output file')

    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    lumiTree = 'LumiTree'
    treeDir  = 'miniTree'

    tchain = ROOT.TChain('{0}/{1}'.format(treeDir,lumiTree))

    for f in args.inputFiles:
        for fname in glob.glob(f):
            tchain.Add(fname)

    allLumis = {}
    for row in tchain:
        if row.run not in allLumis: allLumis[row.run] = set()
        allLumis[row.run].add(row.lumi)

    lumiJson = LumiList(runsAndLumis = allLumis)
    #lumiJson.writeJSON(args.outputFile)
    print lumiJson
    

if __name__ == "__main__":
    status = main()
    sys.exit(status)

