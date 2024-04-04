#! /usr/bin/env python3

import my_task
import process_task
from make_rss import rss

my_tasks = my_task.my_task_project

t = my_tasks.grab_task()
def refresh_xml_impl():
    all_tasks = my_tasks.all_tasks()
    with open("./docs/meetings.rss", 'w') as out: rss(all_tasks, out)
refresh_xml = lambda: my_tasks.visit_git_workdir(refresh_xml_impl)
if t is None:
    refresh_xml()
    raise ValueError(t)
try:
    print("SELECTED THIS TASK: " + repr(t))
    process_task.process_meeting(t)
except:
    my_task.my_task_project.abandon_task(t)
    raise
def refresh_xml():
    all_tasks = t.all_tasks()
    with open("./docs/meetings.rss", 'w'): rss(all_tasks, out)
my_task.my_task_project.commit_task_results(t, cheap_operation=refresh_xml)
