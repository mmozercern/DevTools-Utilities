import os
import sys
import errno
import operator
import subprocess
import logging
import math
import json
import pickle

# common definitions
ZMASS = 91.1876

# jsons
jsons = {
    'Collisions15': '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/'\
                    'Collisions15/13TeV/'\
                    'Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt', # 2.32/fb
    'Collisions16': '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/'\
                    'Collisions16/13TeV/'\
                    'Cert_271036-276811_13TeV_PromptReco_Collisions16_JSON.txt', # 12.9/fb
}

def getJson(runPeriod):
    if runPeriod in jsons: return jsons[runPeriod]

# normatags
normtags = {
    'Collisions15': '/afs/cern.ch/user/l/lumipro/public/normtag_file/moriond16_normtag.json',
    'Collisions16': '/afs/cern.ch/user/l/lumipro/public/normtag_file/normtag_DATACERT.json',
}

def getNormtag(runPeriod):
    if runPeriod in normtags: return normtags[runPeriod]


# helper functions
def python_mkdir(dir):
    '''A function to make a unix directory as well as subdirectories'''
    try:
        os.makedirs(dir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(dir):
            pass
        else: raise

def runCommand(command):
    return subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]


def getCMSSWMajorVersion():
    return os.environ['CMSSW_VERSION'].split('_')[1]

def getCMSSWMinorVersion():
    return os.environ['CMSSW_VERSION'].split('_')[2]

def getCMSSWVersion():
    return ''.join([getCMSSWMajorVersion(),getCMSSWMinorVersion(),'X'])

def sumWithError(*args):
    val = sum([x[0] for x in args])
    err = (sum([x[1]**2 for x in args]))**0.5
    return (val,err)

def diffWithError(a,b):
    val = a[0]-b[0]
    err = (a[1]**2 + b[1]**2)**0.5
    return (val,err)

def prod(iterable):
    return reduce(operator.mul, iterable, 1)

def prodWithError(*args):
    val = prod([x[0] for x in args])
    err = val * (sum([(x[1]/x[0])**2 for x in args if x[0]]))**0.5
    return (val,err)

def divWithError(num,denom):
    val = num[0]/denom[0] if denom[0] else 0.
    err = val * ((num[1]/num[0])**2 + (denom[1]/denom[0])**2)**0.5 if num[0] and denom[0] else 0.
    return (val, err)

def sqrtWithError(a):
    val = a[0]**0.5
    err = 0.5*a[1]
    return (val,err)

def sOverB(s,b):
    return s[0]/b[0] if b[0] else 0.

def poissonSignificance(s,b):
    return s[0]/b[0]**0.5 if b[0] else 0.

def poissonSignificanceWithError(s,b):
    return s[0]/(b[0]+b[1]**2)**0.5 if b else 0.

def asimovSignificance(s,b):
    return (2*((s[0]+b[0])*math.log(1+s[0]/b[0])-1))**0.5 if b[0] else 0.

def asimovSignificanceWithError(s,b):
    return (2*((s[0]+b[0])*math.log((s[0]+b[0])*(b[0]+b[1]**2)/(b[0]**2+(s[0]+b[0])*b[1]**2))-b[0]**2/b[1]**2*math.log(1+b[1]**2*s[0]/(b[0]*(b[0]+b[1]**2)))))**0.5 if b[0] and b[1] else 0.

def dumpResults(results,analysis,name):
    jfile = 'jsons/{0}/{1}.json'.format(analysis,name)
    pfile = 'pickles/{0}/{1}.pkl'.format(analysis,name)
    python_mkdir(os.path.dirname(jfile))
    python_mkdir(os.path.dirname(pfile))
    with open(jfile,'w') as f:
        f.write(json.dumps(results, indent=4, sort_keys=True))
    with open(pfile,'wb') as f:
        pickle.dump(results,f)


# hdfs functions
def strip_hdfs(directory):
    return '/'.join([x for x in directory.split('/') if x not in ['hdfs']])

def hdfs_ls_directory(storeDir):
    '''Utility for ls'ing /hdfs at UW'''
    storeDir = strip_hdfs(storeDir)
    command = 'gfal-ls srm://cmssrm2.hep.wisc.edu:8443/srm/v2/server?SFN=/hdfs/{0}'.format(storeDir)
    out = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]
    if 'gfal-ls' in out:
        logging.error(out)
        return []
    return out.split()

def get_hdfs_root_files(topDir,lastDir=''):
    '''Utility for getting all root files in a directory (and subdirectories)'''
    lsDir = strip_hdfs('{0}/{1}'.format(topDir,lastDir)) if lastDir else strip_hdfs(topDir)
    nextLevel = hdfs_ls_directory(lsDir)
    out = []
    for nl in nextLevel:
        if nl=='failed': # dont include
            continue
        elif nl[-4:]=='root': # its a root file
            out += ['{0}/{1}'.format(lsDir,nl)]
        else: # keep going down
            out += get_hdfs_root_files(lsDir,nl)
    return out

