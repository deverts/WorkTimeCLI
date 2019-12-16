#! /usr/bin/env python

import argparse
import sys
from datetime import datetime, timedelta

from repos.task_tracker.exceptions import RemoteTaskNotFound
from usecases.TimeTracking import TimeTracking
from repos.local_storage.file import FileLocalStorage
from repos.local_storage.exceptions import TaskDoesNotExist
from repos.task_tracker.asana import AsanaTaskTracker

from prettytable import PrettyTable
from termcolor import colored, cprint


parser = argparse.ArgumentParser()
parser.add_argument("-m", "--magic", help="Usage: -m <task name slug>. This will look through your assigned tasks for anything starting with 'em' and use this. If multiple options come up, you will be prompted.", action="store")
parser.add_argument("action", help="The action you wish to complete [ start | stop | list | read | complete ]")
parser.add_argument("id", help="The ID used to lookup the task.", nargs="?")
parser.add_argument("--today", help="Only used with `list` option. Will only show tasks due today.", action="store_true")
parser.add_argument("--thisweek", help="Only used with the `list` option. Will only show tasks due this week.", action="store_true")

args = parser.parse_args()


def find_task_from_slug(work_time: TimeTracking, slug: str) -> str:
    print(f"* Magic find for -> {slug}")
    tasks = work_time.list_tasks()

    potentials = []

    for task in tasks:
        if task.name.lower().startswith(slug.lower()):
            potentials.append(task)

    print(f"* Found {len(potentials)} matches.")

    if len(potentials) == 0:
        pass
    elif len(potentials) == 1:
        return potentials[0].id
    else:
        print(f"* Too many matches found. Which would you like to use? ")
        for c,p in enumerate(potentials):
            print(f"{c+1}. {p.name}")

        while True:
            choice = input("Enter which you'd like to use (or Q to quit): ")

            if choice.lower() == "q":
                print("* Quitting")
                sys.exit(0)

            try:
                return potentials[int(choice)].id
            except TypeError:
                print("* Please input a valid option.")
            except IndexError:
                print("* Please input a valid option.")


if __name__ == "__main__":
    work_time = TimeTracking(AsanaTaskTracker(), FileLocalStorage())

    if args.magic:
        args.id = find_task_from_slug(work_time, args.magic)

    if args.action == "start":
        work_time.start_tracking(args.id)
        print(f"-> Started tracking {args.id}")
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
            today = str(datetime.now().date())
            clean_tasks = []

            for task in tasks:
                if task.due == today:
                    clean_tasks.append(task)

            tasks = clean_tasks
        elif args.thisweek:
            current_day = datetime.now().date()

            start_date = current_day
            base_day = current_day.isoweekday()
            valid_days = list()

            # add today
            valid_days.append(str(current_day))

            while True:
                # If we're checking on a friday
                if base_day == 5:
                    break

                current_day = current_day + timedelta(days=1)

                # if it's friday or earlier, we will allow the day, Sunday is also valid
                if current_day.isoweekday() <= 5 or current_day.isoweekday() == 7:
                    valid_days.append(str(current_day))

                # If we're on Sat (i.e. processed friday). We've looped the week
                if current_day.isoweekday() == 6 and current_day > start_date:
                    break

            valid_tasks = []
            for task in tasks:
                if task.due in valid_days:
                    valid_tasks.append(task)

            tasks = valid_tasks

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
    else:
        print("Invalid command.")
