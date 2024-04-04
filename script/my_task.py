import subprocess
import os

from git_task import *

os.chdir(os.getenv("HOME"))

if not os.path.exists("test"):
    subprocess.run([ "git", "clone", "/root/test.git" ])
else:
    os.chdir("test")
    subprocess.run([ "git", "pull", "origin", "main", "--ff-only" ])
    subprocess.run([ "git", "reset", "--hard", "origin/main" ])
    os.chdir(os.getenv("HOME"))

my_task_project = TaskProject("./test", "tasks.dat")

__all__ = [ "my_task_project" ]
