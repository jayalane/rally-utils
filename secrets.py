"""Stuff to manage passwords and auth info

    TODO caching here and in cal_state - why"""


import sys;
import cal_state;

secrets_to_get = ['trac_login','unlock_login', 'jira_login']


my_secrets = {}

def get_secret(secret_name, depth = 0):
    """Returns the given secret - we aren't worrying about memory, just normal disk files"""
    if depth > 3:
        return ''
    if my_secrets.has_key(secret_name):
        return my_secrets[secret_name]
    else:
        init_secrets(True)
        return get_secret(secret_name, depth + 1)


def init_secrets(override = False):
    global my_secrets
    if len(my_secrets) > 0 and not override:
        return
    
    for sec in secrets_to_get:
        my_secrets[sec] = cal_state.get_secret_state('passwords', sec)
        if my_secrets[sec] == 'Invalid call':
            del my_secrets[sec]
