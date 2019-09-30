#! /usr/bin/env python

import argparse

from usecases.TimeTracking import TimeTracking
from repos.local_storage.file import FileLocalStorage
from repos.task_tracker.asana import AsanaTaskTracker


parser = argparse.ArgumentParser()
parser.add_argument("action", help="The action you wish to complete [ start | stop | list ]")
parser.add_argument("id", help="The ID used to lookup the task.", nargs="?")

args = parser.parse_args()


if __name__ == "__main__":
    work_time = TimeTracking(AsanaTaskTracker(), FileLocalStorage())

    if args.action == "start":
        work_time.start_tracking(args.id)
    elif args.action == "stop":
        work_time.stop_tracking(args.id)
    elif args.action == "list":
        work_time.list_tasks()
    else:
        print("Invalid command.")
