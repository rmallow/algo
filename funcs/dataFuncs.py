import praw
import pandas as pd


def setupReddit(clientId=None, clientSecret=None, userAgent=None):
    if clientId is not None and clientSecret is not None and userAgent is not None:
        return {'reddit',
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
        return {'reddit',
                praw.Reddit(
                    client_id=clientId,
                    client_secret=clientSecret,
                    user_agent=userAgent,
                    username=username,
                    password=password,
                )}
    else:
        return None


def redditTest(reddit=None, subreddit="learnpython"):
    data = None
    if reddit is not None:
        d = {'title': [], 'time': []}
        for submission in reddit.subreddit(subreddit).hot(limit=10):
            d['title'].append(submission.title)
            d['time'].append(submission.created_utc)
        data = pd.DataFrame(d)
        data.set_index('time', inplace=True)
    return data
