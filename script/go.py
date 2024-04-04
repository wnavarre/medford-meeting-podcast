#! /usr/bin/env python3

import my_task
import process_task

t = my_task.my_task_project.grab_task()
if t is None: raise ValueError(t)
try:
    print("SELECTED THIS TASK: " + repr(t))
    process_task.process_meeting(t)
except:
    my_task.my_task_project.abandon_task(t)
    raise
my_task.my_task_project.commit_task_results(t)
