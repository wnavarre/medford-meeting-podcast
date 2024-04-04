import subprocess
import os

from git_task import *

os.chdir(os.getenv("HOME"))

if os.path.exists("medford-meeting-podcast-DATA"):
    os.chdir("/root/medford-meeting-podcast-DATA")
    subprocess.run([ "git", "pull", "origin", "main", "--ff-only" ])
    subprocess.run([ "git", "reset", "--hard", "origin/main" ])
else:
    subprocess.run([ "git", "clone", "git@github.com:wnavarre/medford-meeting-podcast.git", "medford-meeting-podcast-DATA"])

my_task_project = TaskProject("./medford-meeting-podcast-DATA", "tasks.dat")

__all__ = [ "my_task_project" ]
