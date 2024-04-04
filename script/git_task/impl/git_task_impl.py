import git_task.impl.git_ops as git_ops
from uuid import uuid4
from git_task.impl.clean_tsv import TSVFileReader

import functools
import os
import sys

def in_git_workdir(f):
    @functools.wraps(f)
    def wrapper(self, *argp, **argkv):
        previous_cwd = os.getcwd()
        os.chdir(self._git_workdir)
        out = f(self, *argp, **argkv)
        os.chdir(previous_cwd)
        return out
    return wrapper

def grab_task_local_fp(old_tasks_file, new_tasks_file, job_colname):
    out = None
    reader = TSVFileReader(old_tasks_file)
    reader.print_headings(new_tasks_file)
    for entry in reader:
        if (out is None) and (not entry.get(job_colname)):
            out = entry
            out[job_colname] = "TODO-" + str(uuid4())
        entry.print_entry(new_tasks_file)
    return out

def done_task_local_fp(task, old_tasks_file, new_tasks_file, job_colname):
    job_id = task[job_colname]
    if job_id[0:5] != "TODO-": raise ValueError(task[job_colname])
    reader = TSVFileReader(old_tasks_file)
    reader.print_headings(new_tasks_file)
    for entry in reader:
        if entry[job_colname] == task[job_colname]:
            task = task.update_other(entry)
            task[job_colname] = "DONE-" + task[job_colname][5:]
            task.print_entry(new_tasks_file)
            task.print_entry(sys.stdout)
        else:
            entry.print_entry(new_tasks_file)

