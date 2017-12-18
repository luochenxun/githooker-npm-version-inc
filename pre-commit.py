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
pCommitMessage = ''  # git commit message
pProjectName = ''    # the git-project's name(for https://https://github.com/xx/usefulTool.git is usefulTool)
pProjectPath = ''    # the git-project's path


def hook():
    global pCommitMessage, pProjectName, pProjectPath
    # read the package.json
    # read the package's version
    packageJsonFile = pProjectPath + "/package.json"
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
    # subVersionNum = int(versionSplit[len(versionSplit)-1])

    lastVersionStr = versionSplit[len(versionSplit)-1]
    m = re.match("\d+(\D+)\d+",lastVersionStr)
    if m and len(m.groups()) > 0:
        buildDivide = m.group(1)
        subVersionNum = int(lastVersionStr.split(buildDivide)[1]) + 1
        versionSplit[len(versionSplit)-1] = lastVersionStr.split(buildDivide)[0]
        pConfig["version"] = (('.').join(versionSplit) + buildDivide + str(subVersionNum))
    else:
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
    global pCommitMessage, pProjectName, pProjectPath
    pCommitMessage = os.popen('git log -1 --pretty=format:"%s"').read()
    pProjectName = os.popen("git remote -v | sed -n \'1 s|\(.*\)/\(.*\).git\(.*\)|\\2|g p\'").read().replace("\n", "")
    pProjectPath = os.popen("pwd").read().replace("\n", "")


def _pass():
    os._exit(0)

def _failed():
    os._exit(1)


def _loadArgs(args_str):
    """ use to pass param through scripts """
    return pickle.loads(base64.decodestring(args_str))


def main():
    _initGitInfo()
    hook()


if __name__ == "__main__":
    main()
