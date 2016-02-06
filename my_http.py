"""HTTP dict -> posting funcs"""

# this is not pretty 

import urllib         # to URL encode the POST body
import httplib        # for HTTP
import time           # time how slow twiki is

# edit these to change use cases
my_http_cookie_header="set-cookie"  # python decaps it already


def get_ary_from_re(reg_exp, a_string):
    """Returns the first expr in the parens in an RE in the string - for cookies"""
    retval = []
    a_match = reg_exp.search(a_string)
    if a_match is not None:
        for rv in a_match.groups():
            retval.append(rv)
    return retval


def post_url(url, host, a_dict,
             ret_re=None,
             cookie_name="",
             cookie_val="",
             cookie2_name="",
             cookie2_val="",
             do_get=False,
             basic_auth=""):
    """Talks to TWIKI to login or edit (generic, could do other stuff)"""
    conn = httplib.HTTPConnection(host)
    headers = {}
    if not cookie_val == "":  # are we logged in?
        if cookie2_val == "":
            headers['Cookie'] = "%s=%s;" % (cookie_name, cookie_val)
        else:
            headers['Cookie'] = "%s=%s; %s=%s;" % (cookie_name, cookie_val,
                                                   cookie2_name, cookie2_val)

    if not a_dict == {}:
        headers["Content-type"] = "application/x-www-form-urlencoded"
    if basic_auth != "":
        headers["Authorization"] = "Basic %s" % basic_auth
    headers['User-Agent'] = "jayalane/script"
    headers['Accept'] = "*/*"
    body = urllib.urlencode(a_dict)
    # conn.set_debuglevel(10)
    if do_get:
        conn.request("GET", url, body, headers)
    else:
        conn.request("POST", url, body, headers)
    r1 = conn.getresponse()
    if (r1.status in (200, 302)):  # logging in or POST ok
        if ret_re:  # want the cookies
            if 0 == 0:
                cookie_line = r1.getheader(my_http_cookie_header)
                new_session_ids = get_ary_from_re(ret_re,
                                                  cookie_line)
        else:  # get the body
            try:
                body = r1.read()
                new_session_ids = ""
            except:  # if we can
                body = ""
    else:  # oh well  - failure
        body = ""
        new_session_ids = []
    conn.close()
    if ret_re:  # if logging in
        r = new_session_ids
    else:
        r = body
    return r


def get_url(url,
            host,
            use_ssl=False,
            cookie_name="",
            cookie_val="",
            basic_auth=''):
    """Talks to host to GET the URL"""
    if use_ssl:
        conn = httplib.HTTPSConnection(host)
    else:
        conn = httplib.HTTPConnection(host)
#   conn.set_debuglevel(10)
    if cookie_name != '':
        cookie_header = {'Cookie': "%s=%s;" % (cookie_name, cookie_val)}
    else:
        cookie_header = {}
    if basic_auth != "":
        cookie_header["Authorization"] = "Basic %s" % basic_auth
    conn.request("GET", url, "", cookie_header)
    r1 = conn.getresponse()
    if r1.status != 200:
        retval = ""
    else:
        try:
            retval = r1.read()
        except:
            retval = ""
    conn.close()
    return retval
