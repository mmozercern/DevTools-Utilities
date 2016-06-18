#!/usr/bin/env python
import os
import sys
import argparse

import ROOT


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Dump contents of tfile')

    parser.add_argument('filename', type=str)
    parser.add_argument('path', type=str, default='', nargs='?')

    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    tfile = ROOT.TFile(args.filename)
    if not args.path:
        tfile.ls()
    else:
        tobj = tfile.Get(args.path)
        if tobj.InheritsFrom('TDirectoryFile'):
            tobj.ls()
        else:
            tobj.Print()
        


if __name__ == "__main__":
    status = main()
    sys.exit(status)
