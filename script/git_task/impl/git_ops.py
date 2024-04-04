import subprocess
import itertools

ORIGIN = "origin"
BRANCH = "main"

class GitError(Exception):
    def __init__(self, args): self._args = args
    def __str__(self): return " ".join(self._args)

def _git_run(*ls):
    if subprocess.run([ "git" ] + list(ls)).returncode:
        raise GitError(ls)
    
def git_clone(url, name=None):
    if not name:
        return _git_run("clone", url)
    else:
        return _git_run("clone", url, "-o", name)

def git_pull(): return _git_run("pull", "--ff-only")

def _git_commit(msg):
    _git_run("config", "user.name", "AUTOMATED SCRIPT")
    _git_run("config", "user.email", "<>")
    args = [ "commit" ]
    args.extend(itertools.chain.from_iterable(
        zip(itertools.repeat("-m"),
            (x.strip() for x in msg.split("\n")))
    ))
    return _git_run(*args)

def git_send(msg):
    if _git_run("add", "-u"): raise GitError()
    _git_commit(msg)
    return _git_run("push", ORIGIN, BRANCH)

def git_reset(): return _git_run("reset", "--hard", "{}/{}".format(ORIGIN, BRANCH))

def send_or_abort():
    try:
        git_send()
        return
    except:
        pass
    git_reset()
    git_pull()
