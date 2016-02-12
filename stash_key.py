#! /env python

import sys

import base64

import cal_state

def main():
    #data = {}
    #data['username'] = sys.stdin.next()[:-1].lower()
    #data['password'] = sys.stdin.next()[:-1] # remove trailing "\n"
    #cal_state.set_secret_state('passwords', 'trac_login', '%s:%s' % (data['username'], data['password']))
    #cal_state.set_secret_state('passwords', 'unlock_login', base64.b64encode('%s:%s' % (data['username'], data['password'])))
    #data = {}
    #data['username'] = sys.stdin.next()[:-1].lower()
    #data['password'] = sys.stdin.next()[:-1] # remove trailing "\n"
    #cal_state.set_secret_state('passwords', 'jira_login', '%s:%s' % (data['username'], data['password']))
    output = ''
    with open('/x/home/caustinlane/.ssh/id_rsa_2') as f:
        output = f.read()
    cal_state.set_secret_state('keys', 'pp2-key', base64.b64encode(output))
        
# enddef main() #



if (__name__ == '__main__'):
    main()
    print base64.b64decode(cal_state.get_secret_state('keys', 'pp2-key'))
# endif #
