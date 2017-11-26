#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys,subprocess
import os
import pickle
import base64
import re
import collections
import json

''' ---------- Hook method ---------- '''
pCommitTime = ''     # git commit time


# @param project:
#          {
#            "name":"projectName",  // the name of the project
#            "path":"/xx/xx/xx",    // the path of the project
#            "msgReg":"",           // the regular expression to match the commit message
#            "msgRegTips":"",       // the message to show by the invalid commit message
#          }
def hook(project):
    # read the package.json
    # read the package's version
    packageJsonFile = project["path"] + "/package.json"
    packageJsonReader = open(packageJsonFile)
    try:
        configText = packageJsonReader.read()
        pConfig = json.loads(configText, object_pairs_hook = collections.OrderedDict)
    except Exception as e:
        _failed()
    finally:
         packageJsonReader.close()

    # increate the version
    versionStr = pConfig["version"]
    versionSplit = versionStr.split('.')
    subVersionNum = int(versionSplit[len(versionSplit)-1])
    versionSplit[len(versionSplit)-1] = str(subVersionNum+1)
    pConfig["version"] = ('.').join(versionSplit)

    # write back to package.json
    packageJsonWritter = open(packageJsonFile, 'w')
    try:
         packageJsonWritter.write(json.dumps(pConfig, indent=2))
    except Exception as e:
        _failed()
    finally:
         packageJsonWritter.close()

    # add the package.json file to the commit
    ret = os.system("git add package.json")
    if ret == 0:
        print "Increate the version of package.json to : ",('.').join(versionSplit)
        _pass()
    else:
        _failed()


''' ---------- Private methods ---------- '''

# init some global variables of git environment
def _initGitInfo():
    None

def _pass():
    os._exit(0)

def _failed():
    os._exit(1)


def loadProject(obj_str):
  return pickle.loads(base64.decodestring(obj_str))

def main():
    _initGitInfo()
    hook(loadProject(sys.argv[1]))

if __name__ == "__main__":
    main()
