import praw


def setupReddit(clientId=None, clientSecret=None, userAgent=None):
    if clientId is not None and clientSecret is not None and userAgent is not None:
        return {'reddit',
                praw.reddit(
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
                praw.reddit(
                    client_id=clientId,
                    client_secret=clientSecret,
                    user_agent=userAgent,
                    username=username,
                    password=password,
                )}
    else:
        return None
