#! /bin/env pypy

import os
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


def dict_from_story(story):
    details = {}
    for a_key in story.attributes():
        details[a_key] = str(story.__dict__[a_key])
    return details
    

def make_story(story_name, story_detail, username):
    r = Rally(server, apikey=apikey, project=project)
    r.enableLogging('rally.log')
    wksp = r.getWorkspace()
    proj = r.getProject(project)
    info = {"Workspace":   wksp.ref,
            "Project":     proj.ref,
            "Name":        story_name + " (web intake form from " + username + ")",
            "Story Type":  "New Feature",
            "Description": story_detail}

    story = r.put('Story', info)
    return dict_from_story(story)


def get_story(formatted_id):
    r = Rally(server, apikey=apikey, project=project)
    r.enableLogging('rally.log')
    aa = r.get('UserStory',
               fetch=True,
               query='FormattedID = "' + formatted_id + '"',
               instance=True)
    return dict_from_story(aa)


def make_task(task_name, task_user, task_detail, task_hours):
    r = Rally(server, apikey=apikey, project=project)
    wksp = r.getWorkspace()
    proj = r.getProject(project)

    aa = r.get('UserStory', fetch='FormattedID', query='FormattedID = "' + todo_story + '"', instance=True)
    info = {"Workspace":   wksp.ref,
            "Project":     proj.ref,
            "WorkProduct": aa.ref,
            "Name":        task_name + " (" + task_user + ")",
            "State":       "Completed",
            "Estimate":    hours,
            "Actuals":     hours,
            "TaskIndex":   1,
            "Description": task_detail + " autocreated."}

    task = r.put('Task', info)
    for b in task:
        return b.details()

if __name__ == '__main__':
    print get_story('US560419')
    os._exit()
    import getpass
    hours = raw_input('How many hours: ')
    task_name = raw_input('Title of task: ')
    task_detail = raw_input('One line of task detail: ')
    print make_task(task_name, getpass.getuser(), task_detail, hours)
