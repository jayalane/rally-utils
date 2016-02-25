import os
import json

import rally

from bottle import run, route
from bottle import request, response
import bottle


bottle.debug(True)


@route('/')
def form(month=None, day=None, year=None):
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns='http://www.w3.org/1999/xhtml'
          xml:lang='en'><head><meta http-equiv='Content-Type'
          content='application/xhtml+xml;
          charset=utf-8'/><meta name='generator'
          content='emacs,lisp'/>
<head>
<style type="text/css">body{font-family: Monospace; margin:4px;max-width:650px;line-height:0.8;font-size:16px;color:#444;padding:010px}h1,h2,h3{line-height:1.2}</style>
 <title>Sherlock Feature Request Experiment</title>
</head><body><h1>Sherlock Feature Request Experiment</h1>
<div>Make a Rally Story for Sherlock Team (in backlog, sorry!)
<form id='rally-story' action ='/rally_story' method='post'>
<fieldset>
<label for='name'>Name:</label>
<input type='text' name='name' placeholder='Put the name of the story here'/>
<label for='detail'>Detail of Story:</label>
<textarea name='detail' placeholder='Describe the story in detail here' rows='8' cols='50'></textarea>
<input type='submit' value='Submit'/></fieldset></form>
</div>
<h3>Note: It takes about 2 minutes to process, and I haven't done any fancy disabling of the form button.</h3></body></html>
    """


@route('/rally_story', method='POST')
def rally_story():
    if request.forms.detail:
        detail = request.forms.detail
    else:
        detail = ""
    if request.forms.name:
        name = request.forms.name
    else:
        name = ""
    if name == "" and detail == "":
        return "Not enough data!"
    stuff = rally.make_story(name, detail)
    return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
          "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns='http://www.w3.org/1999/xhtml'
          xml:lang='en'><head><meta http-equiv='Content-Type'
          content='application/xhtml+xml;
          charset=utf-8'/><meta name='generator'
          content='emacs,lisp'/>
<head>
<style type="text/css">body{font-family: Monospace; margin:4px;max-width:650px;line-height:0.8;font-size:16px;color:#444;padding:010px}h1,h2,h3{line-height:1.2}</style>
 <title>Sherlock Feature Request Experiment</title>
</head><body><h1>Sherlock Feature Request Experiment</h1><pre>""" + stuff  + "</pre></body></html>"


@route('/story', method='PUT')
def rally_create():
    try:
        response.content_type = 'application/json'
        data = request.json
        detail = data.get('detail', '')
        name = data.get('name', '')
    except Exception as e:
        return {"error": repr(e)}
    if name == "" and detail == "":
        return {"error": "Not enough data!"}

    stuff = rally.make_story(name, detail)
    return stuff

if os.uname()[0] == 'Darwin':
    run(host='localhost', port=8888, server='cherrypy')
else:
    run(host=os.uname()[1], port=8888, server='cherrypy')
