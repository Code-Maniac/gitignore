import os
import subprocess

def isInstalled():
    with open(os.devnull, 'w') as devnull:
        stdin = stdout = stderr = devnull
        return subprocess.call(
            "hash git",
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            shell=True) == 0
    return False

def isRepo(gitDir=os.getcwd()):
    with open(os.devnull, 'w') as devnull:
        stdin = stdout = stderr = devnull
        return subprocess.call(
            "git status",
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            shell=True,
            cwd=gitDir) == 0
    return False

def getRoot(gitDir=os.getcwd()):
    with open(os.devnull, 'w') as devnull:
        stdin = stderr = devnull
        proc = subprocess.Popen(
            "git rev-parse --show-toplevel",
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=stderr,
            shell=True,
            cwd=gitDir)
        stdout = proc.communicate()[0]
        return str(stdout.decode("ascii")).partition('\n')[0]
    return ""

def getIgnore(gitDir=os.getcwd()):
    return getRoot(gitDir) + "/.gitignore"

def clone(srcURL, dstDir):
    with open(os.devnull, 'w') as devnull:
        stdin = stdout = stderr = devnull
        return subprocess.call(
            "git clone %s %s" % (srcURL, dstDir),
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            shell=True) == 0
    return False

def pull(remote="origin", branch="master", gitDir=os.getcwd()):
    with open(os.devnull, 'w') as devnull:
        stdin = stdout = stderr = devnull
        return subprocess.call(
            "git pull %s %s" % (remote, branch, gitDir),
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            shell=True,
            cwd=gitDir) == 0
    return False
