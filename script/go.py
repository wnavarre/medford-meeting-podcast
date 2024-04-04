import my_task
import process_task

t = my_task.my_task_project.grab_task()
if t is None: raise ValueError(t)
process_task.process_meeting(t)
my_task.my_task_project.commit_task_results(t)
