import praw
import pandas as pd
from datetime import datetime


def setupReddit(clientId=None, clientSecret=None, userAgent=None, **kwargs):
    if clientId is not None and clientSecret is not None and userAgent is not None:
        return {'reddit':
                praw.Reddit(
                    client_id=clientId,
                    client_secret=clientSecret,
                    user_agent=userAgent,
                )}
    else:
        return None


def setupRedditAuth(clientId=None, clientSecret=None, userAgent=None, username=None, password=None):
    if clientId is not None and clientSecret is not None and userAgent is not None and \
       username is not None and password is not None:
        return {'reddit':
                praw.Reddit(
                    client_id=clientId,
                    client_secret=clientSecret,
                    user_agent=userAgent,
                    username=username,
                    password=password,
                )}
    else:
        return None


def redditTest(reddit=None, subreddit="learnpython", **kwargs):
    data = None
    if reddit is not None:
        d = {'title': [], 'time': [], 'uid': []}
        redditVals = None
        redditVals = reddit.subreddit(subreddit).new(limit=10)
        if redditVals:
            for submission in redditVals:
                d['title'].append(submission.title)
                d['time'].append(datetime.utcfromtimestamp(submission.created_utc))
                d['uid'].append(submission.id)
            data = pd.DataFrame(d)
    return data
