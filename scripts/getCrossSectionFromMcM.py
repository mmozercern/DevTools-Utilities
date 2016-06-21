#!/usr/bin/env python
import requests, cookielib
import subprocess
import argparse
import os
import sys

requests.packages.urllib3.disable_warnings()


def parse_command_line(argv):
    parser = argparse.ArgumentParser(description='Get cross section from McM')

    parser.add_argument('dataset',type=str,help='Dataset name for query')

    args = parser.parse_args(argv)

    return args

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    args = parse_command_line(argv)

    temp_cookie_file = "mcmcookies.temp"
    mcm_address = "https://cms-pdmv.cern.ch/mcm"
    subprocess.call(["cern-get-sso-cookie", "--krb", "-r", "-u", mcm_address, "-o", temp_cookie_file])
    c = cookielib.MozillaCookieJar(temp_cookie_file)
    c.load()
    search_options = {
        "db_name" : "requests", 
        "page"    : -1,
        "dataset_name" : args.dataset,
    }
    r = requests.get("/".join([mcm_address, "search"]), params=search_options, cookies=c, verify=False)
    for sample in r.json()["results"]:
        gen_params = sample["generator_parameters"]
        if len(gen_params) and "GS" in sample["prepid"]:
                # Sometimes generator_parameters has ?empty? lists in it
                values = [i for i in gen_params if type(i) is dict]
                print "\nCross section for dataset {0} from request {1}.".format(sample["dataset_name"], sample["prepid"])
                print "---->  sigma = {0} pb".format(values[0]["cross_section"])
    os.remove(temp_cookie_file)

if __name__ == "__main__":
    status = main()
    sys.exit(status)
