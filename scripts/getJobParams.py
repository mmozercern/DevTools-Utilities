#!/usr/bin/env python
import sys
import os
import argparse
import glob
import math
import json
from prettytable import PrettyTable

def printSummary(args):
    table = PrettyTable(['Sample','Files','Jobs','Files per job','Mean time [min]','Max time [min]','Target [120 min]'])
    table.align = 'r'
    table.align['Sample'] = 'l'
    targetJson = {}
    for sampleDir in sorted(glob.glob('{0}/*'.format(args.jobDirectory))):
        if '_inputs' in sampleDir: continue
        sample = os.path.basename(sampleDir)
        jobDirs = glob.glob('{0}/*/'.format(sampleDir))
        jobtimes = []
        jobfiles = 0
        for jobDir in jobDirs:
            exetime = os.path.join(jobDir,'exe_time')
            times = {'real':0,'user':0,'var':0}
            if os.path.isfile(exetime):
                with open(exetime,'r') as f:
                    lines = f.readlines()
                for line in lines:
                    vals = line.split()
                    times[vals[0]] = float(vals[1])
            jobtimes += [times]
            inputs = glob.glob('{0}/*.inputs'.format(jobDir))
            if len(inputs)>0:
                with open(inputs[0],'r') as f:
                    nfiles = len(f.readlines())
            jobfiles += nfiles
        realtimes = [times['real'] for times in jobtimes if 'real' in times]
        meantimes = sum(realtimes)/len(realtimes)/60. if len(realtimes) else 0.
        maxtimes = max(realtimes)/60.
        jobs = len(jobDirs)
        filesPerJob = int(math.ceil(float(jobfiles)/jobs))
        target = min(int(math.ceil(min(120. * filesPerJob / meantimes, 240. * filesPerJob / maxtimes))),jobfiles) if meantimes and maxtimes else 1
        table.add_row([sample,jobfiles,jobs,filesPerJob,'{0:.2f}'.format(meantimes),'{0:.2f}'.format(maxtimes),target])
        targetJson[sample] = target
    print table.get_string()
    with open('target.json','w') as f:
        f.write(json.dumps(targetJson, indent=4, sort_keys=True))

    

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Get summary information about a condor job.')

    parser.add_argument('jobDirectory', type=str, help='Top level directory for jobs.')

    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)
    printSummary(args)

if __name__ == "__main__":
    status = main()
    sys.exit(status)
                           
