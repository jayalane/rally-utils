#! /bin/env pypy

import requests  # needed for pyral somehow
from pyral import Rally

import cal_state

apikey = cal_state.get_secret_state('passwords', 'rally-api-key')
#  Get apikey by logging into Rally and then clicking on:
#  https://rally1.rallydev.com/login/?redirect_uri=%2Flogin%2Faccounts%2Findex.html#/keys .


def enable_http_logging():
    """Thanks stacktrace"""
    import logging
    import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


# enable_http_logging()   # uncomment to see HTTP layer
server = "rally1.rallydev.com"
import my_config
project = my_config.project()
todo_story = my_config.live_support()


def make_story(story_name, story_detail):
    r = Rally(server, apikey=apikey, project=project)

    wksp = r.getWorkspace()
    proj = r.getProject()
    info = {"Workspace":   wksp.ref,
            "Project":     proj.ref,
            "Name":        story_name + " (web intake form)",
            "Description": story_detail}

    story = r.put('Story', info)
    return story.details()


def make_task(task_name, task_user, task_detail, task_hours):

    r = Rally(server, apikey=apikey, project=project)

    wksp = r.getWorkspace()
    proj = r.getProject()

    aa = r.get('UserStory', fetch='FormattedID', query='FormattedID = "' + todo_story + '"')
    for story in aa:
        info = {"Workspace":   wksp.ref,
                "Project":     proj.ref,
                "WorkProduct": story.ref,
                "Name":        task_name + " (" + task_user + ")",
                "State":       "Completed",
                "Estimate":    hours,
                "Actuals":   hours,
                "TaskIndex":   1,
                "Description": task_detail + " autocreated."}

        task = r.put('Task', info)
        for b in task:
            return b.details()


if __name__ == '__main__':
    import getpass
    hours = raw_input('How many hours: ')
    task_name = raw_input('Title of task: ')
    task_detail = raw_input('One line of task detail: ')
    print make_task(task_name, getpass.getuser(), task_detail, hours)
