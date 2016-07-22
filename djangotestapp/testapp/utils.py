
"""
Utilities for linkifying #hashtags and @usertags in a string

:Author: @westurner

"""
import cgi
import re
import urllib

from collections import OrderedDict
from functools import partial

from django.contrib.auth import get_user_model

RGX_HASHTAG = r'\B(#)([\w\d]+)'
RGX_USERTAG = r'\B(@)([\w\d]+)'
RGX_TAGS = r'\B(#|@)([\w\d]+)'


def tag_replfunc(mobj, hashtags=None, usertags=None, users_by_name=None):
    """
    A replfunc for re.subn

    Args:
        mobj (re match object): a re match object
    Kwargs:
        hashtags (list): a list to which matching hashtag strs will be appended
        usertags (list): a list to which matching usertag strs will be appended
        users_by_name (dict): a {username: User} dict of existing users
    Returns:
        str: replacement string for the given #hashtag or @usertag
    """
    usertags = usertags if usertags is not None else []
    hashtags = hashtags if hashtags is not None else []

    prefixChar = mobj.groups()[0]
    if prefixChar == '#':
        hashtag = mobj.groups()[1]
        hashtags.append(hashtag.lower())
        return u'''<a class='hashtag' href='/tag/{0}'>#{1}</a>'''.format(
            urllib.quote(hashtag),
            cgi.escape(hashtag))
    elif prefixChar == '@':
        username = mobj.groups()[1]
        if users_by_name is not None:
            username_lower = username.lower()
            user = users_by_name.get(username_lower)
            if user is None:
                return u'@%s' % username
            else:
                usertags.append(user)
        else:
            usertags.append(username)
        return u'''<a class='usertag' href='/@{0}'>@{1}</a>'''.format(
            urllib.quote(username),
            cgi.escape(username))


def lookup_usernames(usernames):
    """
    Lookup the given list of usernames and return a {username: User} dict

    Args:
        usernames (list[str]): list of usernames (without ``@`` prefix)
    Returns:
        OrderedDict: {username: User} dict of existing users
    """
    User = get_user_model()
    users = User.objects.filter(username__in=usernames)
    users_by_name = OrderedDict((u.username.lower(), u) for u in users)
    return users_by_name


def linkify_text(text, usernamelookupfn=lookup_usernames):
    """
    Given a string text, replace #hashtags and @usertags with links.

    Args:
        text (str): text to linkify
    Kwargs:
        lookup_usernames (function): A function which,
            given a list of username strs,
            returns a dict of {username: User} pairs which exist.
            If the usernames do not exist, they will not be linkified.
            if lookup_usernames is None, all @usertags will be linked.
    Returns:
        dict: ``{'html': linkified_html,
                'hashtags': list[str],
                'usertags': list[str],
                'users_by_name': {str: User}}``
    """
    hashtags = []
    usertags = []
    usernames = [x[1].lower() for x in re.findall(RGX_USERTAG, text)]
    if usernamelookupfn is not None:
        users_by_name = usernamelookupfn(usernames)
    else:
        users_by_name = None
    tag_replfunc_ = partial(tag_replfunc,
                        hashtags=hashtags,
                        usertags=usertags,
                        users_by_name=users_by_name)
    html, count = re.subn(RGX_TAGS, tag_replfunc_, text, flags=re.UNICODE)
    return {'html': html,
            'hashtags': hashtags,
            'usertags': usertags,
            'users_by_name': users_by_name}

