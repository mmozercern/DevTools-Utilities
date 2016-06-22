import os
import sys
import errno
import operator

# common definitions
ZMASS = 91.1876

# jsons
jsons = {
    'Collisions15': '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/'\
                    'Collisions15/13TeV/'\
                    'Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt', # 2.32/fb
    'Collisions16': '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/'\
                    'Collisions16/13TeV/'\
                    'Cert_271036-275125_13TeV_PromptReco_Collisions16_JSON.txt', # 3.99/fb
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
