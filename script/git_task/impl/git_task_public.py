__all__ = ( "TaskProject", "TaskRace")

import git_task.impl.git_ops as git_ops
import os
import shutil
from git_task.impl.git_task_impl import *

mv = os.rename

class TaskRace(Exception): pass

class TaskProject:
    def __init__(self, git_workdir, tasks_file, job_colname="JOB"):
        self._git_workdir = os.path.abspath(git_workdir)
        self._tasks_filename = tasks_file
        self._job_colname = job_colname
    @in_git_workdir
    def grab_task(self, *, fail_ungracefully=False, startup_function=None):
        tasks_file = self._tasks_filename
        new_file_name = tasks_file + ".NEW"
        git_ops.git_reset()
        git_ops.git_pull()
        if startup_function is not None: startup_function()
        with open(tasks_file, "r") as old_tasks:
            with open(new_file_name, "w") as new_tasks:
                out = grab_task_local_fp(old_tasks, new_tasks, self._job_colname)
        if not out: return
        mv(new_file_name, tasks_file)
        def finish():
            git_ops.git_send(out[self._job_colname])
            return out
        if fail_ungracefully: return finish()
        try:
            if not fail_ungracefully:
                return finish()
        except git_ops.GitError:
            pass
        git_ops.git_reset()
        git_ops.git_pull()
        raise TaskRace()
    @in_git_workdir
    def commit_task_results(self, task_data, cheap_operation=None, *, fail_ungracefully=False):
        tasks_file = self._tasks_filename
        new_file_name = tasks_file + ".NEW"
        git_ops.git_reset()
        git_ops.git_pull()
        if cheap_operation is not None: cheap_operation()
        with open(tasks_file, "r") as old_tasks:
            with open(new_file_name, "w") as new_tasks:
                done_task_local_fp(task_data, old_tasks, new_tasks, self._job_colname)
        mv(new_file_name, tasks_file)
        error_st = ""
        try:
            git_ops.git_send(task_data[self._job_colname])
            return
        except git_ops.GitError as e:
            error_st = repr(e)
        git_ops.git_reset()
        git_ops.git_pull()
        raise TaskRace(error_st)

