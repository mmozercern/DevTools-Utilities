#!/usr/bin/env python

import os
import sys
import glob
import argparse
import logging

import ROOT

def getVar(rtrow,lep,var):
    return getattr(rtrow,'{0}_{1}'.format(lep,var))

def print_detailed_dy(rtrow):
    print '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
    print '    channel: {0}'.format(rtrow.channel)
    leps = ['z1','z2']
    for lep in leps:
         print '    {0}: pt {1}, eta {2}, phi {3}, pass: {4}'.format(lep, getVar(rtrow,lep,'pt'), getVar(rtrow,lep,'eta'), getVar(rtrow,lep,'phi'), getVar(rtrow,lep,'passMedium'))
    print '    z_mass: {0}, z_pt: {1}'.format(rtrow.z_mass,rtrow.z_pt)

def print_detailed_wz(rtrow):
    print '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
    print '    z_mass: {0}, z1: {1}, z2: {2}'.format(rtrow.z_mass,rtrow.z1_pt,rtrow.z2_pt)

def print_detailed_hpp3l(rtrow):
    print '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
    print rtrow.channel, rtrow.genChannel
    print rtrow.hpp1_pt, rtrow.hpp2_pt, rtrow.hm1_pt

def print_detailed_mini(rtrow):
    print '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
    for obj in ['electrons','muons','taus','jets','photons']:
        print '    {0}: {1}'.format(obj,getattr(rtrow,obj+'_count'))

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description="Print events from ntuple")

    parser.add_argument('files', nargs='+', help='File names w/ UNIX wildcards')
    parser.add_argument('-t','--tree',type=str,default='MiniTree',help='Tree name')
    parser.add_argument('-c','--cut',nargs='?',type=str,default='',help='Cut to be applied to tree')
    parser.add_argument('-e','--events',nargs='*',type=str,default=[],help='Events to print (form: run:lumi:event, space delimited)')
    parser.add_argument('-d','--detailed',action='store_true',help='Print detailed event information')
    parser.add_argument('--log',nargs='?',type=str,const='INFO',default='INFO',choices=['INFO','DEBUG','WARNING','ERROR','CRITICAL'],help='Log level for logger')
    args = parser.parse_args(argv)

    return args



def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    loglevel = getattr(logging,args.log)
    logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)s %(name)s: %(message)s', level=loglevel, datefmt='%Y-%m-%d %H:%M:%S', stream=sys.stderr)

    files = [filename for string in args.files for filename in glob.glob(string)]

    tchain = ROOT.TChain(args.tree)
    for f in files:
        tchain.Add(f)

    selectedEvents = tchain.CopyTree(args.cut) if args.cut else tchain

    rtrow = selectedEvents
    for r in xrange(rtrow.GetEntries()):
        rtrow.GetEntry(r)
        eventkey = '{0}:{1}:{2}'.format(rtrow.run, rtrow.lumi, rtrow.event)
        if args.events and eventkey not in args.events: continue
        if args.detailed:
            if args.tree=='miniTree/MiniTree': print_detailed_mini(rtrow)
            if args.tree=='DYTree': print_detailed_dy(rtrow)
            if args.tree=='WZTree': print_detailed_wz(rtrow)
            if args.tree=='Hpp3lTree': print_detailed_hpp3l(rtrow)
        else:
            print eventkey

if __name__ == "__main__":
    main()
