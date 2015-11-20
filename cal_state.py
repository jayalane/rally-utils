"""Class to keep info across runs.

   They need to specify the name of their chat room and the functions below to call
   on message receipt"""


import my_http
import json

my_cache = {}


# my_secret_host = "localhost:8000"
my_secret_host = "hyperlvs80.qa.paypal.com:8007"


def override_secret_host(new_host):
    global my_secret_host
    my_secret_host = new_host


def get_state_keys(path1):
    raw_data = get_state(path1)
    if raw_data == '':
        return []
    the_data = json.loads(raw_data)
    return sorted(the_data.keys())
    

def get_state(path1, path2=None):
    global my_cache
    body = 'Undefined'
    if path2 is None:
        url = '/get/%s' % (path1)
    else:
        url = '/get/%s/%s' % (path1, path2)
    try:
        body = my_http.get_url(url, my_secret_host, True)
    except Exception as inst:
        print "Secret host Problem! {{{0!r}}}".format(inst)
        if url in my_cache:
            # print "Using cache for %s" % (url)
            return my_cache[url]
    if body == 'Undefined':
        if url in my_cache:
            print "Using cache for %s" % (url)
            return my_cache[url]
        return ''
    my_cache[url] = body.lstrip('"').rstrip('"')
    return my_cache[url]


def set_state(path1, path2, path3):
    body = my_http.get_url('/set/%s/%s/%s' % (path1, path2, path3),
                           my_secret_host, True)
    return body.replace('"', '')


def set_state_if_less(path1, path2, path3):
    body = my_http.get_url('/set_if_less/%s/%s/%s' % (path1, path2, path3),
                           my_secret_host, True)
    return body.replace('"', '')


def set_state_incr(path1, path2):
    body = my_http.get_url('/set_incr/%s/%s' % (path1, path2),
                           my_secret_host, True)
    return body.replace('"', '')


def delete_state(path1, path2):
    my_http.get_url('/delete/%s/%s' % (path1, path2),
                    my_secret_host, True)


def set_secret_state(path1, path2, path3):
    if path3 is None:
        url = '/secret_set/%s/%s' % (path1, path2)
    else:
        url = '/secret_set/%s/%s/%s' % (path1, path2, path3)
    try:
        body = my_http.get_url(url, my_secret_host, True)

    except Exception as inst:
        print "Secret host Problem! {{{0!r}}}".format(inst)
        if url in my_cache:
            return my_cache[url]
    if body == 'Undefined' or body == "Not Allowed":
        return ''
    my_cache[url] = body.lstrip('"').rstrip('"')
    return my_cache[url]


def get_secret_state(path1, path2):
    global my_cache
    body = ''
    if path2 is None:
        url = '/secret_get/%s' % (path1)
    else:
        url = '/secret_get/%s/%s' % (path1, path2)
    try:
        body = my_http.get_url(url, my_secret_host, True)
    except Exception as inst:
        print "Secret host Problem! {{{0!r}}}".format(inst)
        if url in my_cache:
            return my_cache[url]
    if body == 'Undefined':
        return ''
    my_cache[url] = body.lstrip('"').rstrip('"')
    return my_cache[url]


if __name__ == "__main__":
    print get_state('names', 'chris')
    print get_state_keys('release')
    # print get_state_keys('release')
