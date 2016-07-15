
import cgi
import re
import urllib


RGX_HASHTAG = r'(#)(\w+)'
RGX_ATTAG = r'(@)(\w+)'


def hashtag_replfunc(mobj):
    hashtag = mobj.groups()[1]
    return '''<a class='hashtag' href='/tag/{0}'>#{1}</a>'''.format(
        urllib.quote(hashtag),
        cgi.escape(hashtag))


def usertag_replfunc(mobj):
    username = mobj.groups()[1]
    return '''<a class='usertag' href='/@{0}'>@{1}</a>'''.format(
        urllib.quote(username),
        cgi.escape(username))


def linkify_articlebody(bodytext):
    html, count = re.subn(RGX_HASHTAG, hashtag_replfunc, bodytext)
    html, count = re.subn(RGX_ATTAG, usertag_replfunc, html)
    return html
