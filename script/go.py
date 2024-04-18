#! /usr/bin/env python3

import my_task
import process_task
from make_rss import rss
import os

my_tasks = my_task.my_task_project
def refresh_xml_impl():
    print("REFRESHING XML....")
    all_tasks = my_tasks.all_tasks()
    with open("./docs/meetings.rss", 'w') as out: rss(all_tasks, out)
refresh_xml = lambda: my_tasks.visit_git_workdir(refresh_xml_impl)

if os.getenv("RSSONLY"):
    refresh_xml()
    my_tasks.unsafe_commit("Regenerate RSS xml")
    exit()

t = my_tasks.grab_task()
if t is None:
    raise ValueError(t)
try:
    print("SELECTED THIS TASK: " + repr(t))
    process_task.process_meeting(t)
except:
    my_task.my_task_project.abandon_task(t)
    raise
my_task.my_task_project.commit_task_results(t, cheap_operation=refresh_xml)
