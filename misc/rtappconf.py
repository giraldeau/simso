#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import json

from argparse import ArgumentParser

from simso.configuration import Configuration

def usec(msec):
    return int(msec * 1000)

def save_rtapp(config, output):

    root = {
            "resources": 0,
            "tasks" : {},
            "global": {
                "spacing" : 0,
                "default_policy" : "SCHED_OTHER",
                "duration" : 1,
                "gnuplot" : False,
                "logdir" : "/tmp/",
                "log_basename" : "rt-app",
                "lock_pages" : True,
                "frag" : 1
           }
    }

    for task in config.task_info_list:
        tsk = {
            "policy": "SCHED_DEADLINE",
            "exec": usec(task.wcet),
            "period": usec(task.period),
            "deadline": usec(task.deadline)
        }
        root["tasks"][task.name] = tsk

    with open(output, "w") as out:
        json.dump(root, out, indent=4, encoding="utf-8")
        out.write("\n")

def main():
    parser = ArgumentParser()
    parser.add_argument("input", help="input xml configuration")
    parser.add_argument("output", help="output rt-app json configuration")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        raise(Exception("file not found: {}".format(args.input)))

    config = Configuration(args.input)

    save_rtapp(config, args.output)

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception, e:
        print("Exception: {}".format(e.message))
        sys.exit(1)
