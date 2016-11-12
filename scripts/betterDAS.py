#!/usr/bin/env python
import os
import sys
import time
import logging
import argparse

logging.basicConfig(level=logging.INFO, stream=sys.stderr)

# DBS modules
try:
    from dbs.apis.dbsClient import DbsApi
    dbsLoaded = True
except:
    dbsLoaded = False

def client(args):

    if not dbsLoaded:
        logging.error('You must source a crab environment to use DBS API.\nsource /cvmfs/cms.cern.ch/crab3/crab.sh')
        return

    url = 'https://cmsweb.cern.ch/dbs/prod/global/DBSReader'
    dbsclient = DbsApi(url)

    if args.datasets:
        for dataset in args.datasets:
            datasets = dbsclient.listDatasets(dataset=dataset)
            for d in sorted([dataset['dataset'] for dataset in datasets]):
                print d

def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Get information from DBS')

    parser.add_argument('--datasets', type=str, nargs="*", help='Dataset names with wildcards')

    return parser.parse_args(argv)

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    client(args)

if __name__ == "__main__":
    status = main()
    sys.exit(status)
