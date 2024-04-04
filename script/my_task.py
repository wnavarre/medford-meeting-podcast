import subprocess
import os

from git_task import *

os.chdir(os.getenv("HOME"))

os.chdir("/root/medford-meeting-podcast")
subprocess.run([ "git", "pull", "origin", "main", "--ff-only" ])
subprocess.run([ "git", "reset", "--hard", "origin/main" ])

my_task_project = TaskProject("/root/medford-meeting-podcast", "tasks.dat")

__all__ = [ "my_task_project" ]
