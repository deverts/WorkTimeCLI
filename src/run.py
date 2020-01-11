#! /usr/bin/env python

import argparse
import sys
from typing import List
from datetime import datetime, timedelta

from entities import TaskTrackerTask
from repos.task_tracker.exceptions import RemoteTaskNotFound
from usecases.TimeTracking import TimeTracking
from repos.local_storage.file import FileLocalStorage
from repos.local_storage.exceptions import TaskDoesNotExist, TaskAlreadyExists
from repos.task_tracker.asana import AsanaTaskTracker

from prettytable import PrettyTable
from termcolor import cprint


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--magic", help="Usage: -m <task name slug>. This will look through your assigned tasks for anything starting with 'em' and use this. If multiple options come up, you will be prompted.", action="store")
parser.add_argument("action", help="The action you wish to complete [ start | stop | list | read | complete ]")
parser.add_argument("id", help="The ID used to lookup the task.", nargs="?")
parser.add_argument("--today", help="Only used with `list` option. Will only show tasks due today.", action="store_true")
parser.add_argument("--thisweek", help="Only used with the `list` option. Will only show tasks due this week.", action="store_true")
parser.add_argument("--tomorrow", help="Only used with the `list` option. Will only show tasks due tomorrow.", action="store_true")
parser.add_argument("--running", help="Show tasks i'm currently tracking for.", action="store_true")

args = parser.parse_args()


def pick_task_from_list(choices: List[TaskTrackerTask]) -> str:
    for c, p in enumerate(choices):
        print(f"{c + 1}. {p.name}")

    while True:
        choice = input("Enter which you'd like to use (or Q to quit): ")

        if choice.lower() == "q":
            print("* Quitting")
            sys.exit(0)

        try:
            # -1 since we don't 0 index
            selection = int(choice) - 1

            if selection < 0:
                raise ValueError

            return choices[selection].id
        except ValueError:
            print("* Please input a valid option.")
        except IndexError:
            print("* Please input a valid option.")


def find_task_from_slug(work_time: TimeTracking, slug: str) -> str:
    assigned_tasks = work_time.list_tasks()

    matches = []

    for task in assigned_tasks:
        if task.name.lower().startswith(slug.lower()):
            matches.append(task)

    if len(matches) == 0:
        raise RemoteTaskNotFound
    elif len(matches) == 1:
        return matches[0].id
    else:
        print(f"* Too many matches found. Which would you like to use? ")
        return pick_task_from_list(matches)


if __name__ == "__main__":
    work_time = TimeTracking(AsanaTaskTracker(), FileLocalStorage())

    if args.magic:
        try:
            args.id = find_task_from_slug(work_time, args.magic)
        except RemoteTaskNotFound:
            print("-> Task not found. Please try another slug.")
            sys.exit(0)

    if args.action == "start":
        try:
            work_time.start_tracking(args.id)
            print(f"-> Started tracking {args.id}")
        except TaskAlreadyExists:
            print("-> Already tracking. Doing nothing.")

    elif args.action == "stop":
        try:
            work_time.stop_tracking(args.id)
            print(f"-> Stopped tracking {args.id}")
        except TaskDoesNotExist:
            print("x Task ID either is not tracking, or does not exist.")
    elif args.action == "list":
        tasks = work_time.list_tasks()

        table = PrettyTable()
        table.field_names = ["ID", "Name", "Due"]
        table.align["ID"] = "l"
        table.align["Name"] = "l"
        table.align["Due"] = "l"

        if args.today:
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            tasks = [x for x in tasks if x.due == today]
        elif args.tomorrow:
            tomorrow = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            tasks = [x for x in tasks if x.due == tomorrow]
        elif args.thisweek:
            current_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

            ok_dates = [current_day]
            while current_day.isoweekday() != 5:
                current_day = current_day + timedelta(days=1)
                ok_dates.append(current_day)

            tasks = [x for x in tasks if x.due in ok_dates]

        [table.add_row([x.id, x.name, x.due]) for x in tasks]

        print(table)
    elif args.action == "read":
        try:
            task_info = work_time.read_task(args.id)

            cprint(task_info.name, attrs=['bold'])
            print("Assigned to: ", end="")
            cprint(task_info.assigned_to, attrs=['bold'])
            print("Task due: ", end="")
            cprint(f"{task_info.due} ({'Completed' if task_info.complete else 'Incomplete'})", attrs=["bold"])
            print("Time spent: ", end="")
            cprint(f"{task_info.time_spent} hours", attrs=['bold'])
            print("Description: ")
            cprint(task_info.description, attrs=['bold'])
        except RemoteTaskNotFound:
            print("We're not able to find this task. Are you sure it exists?")
    elif args.action == "complete":
        work_time.complete_task(args.id)
        print("Done!")
    elif args.acion == "running":
        tasks = work_time.list_tracking()
    else:
        print("Invalid command.")
