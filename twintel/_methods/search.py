def search(query, max_tweets=200, language='en'):

    '''Timeline Method

    WHAT: Gets up to 3,200 most recent tweets from a given user's
    timeline.

    HOW: timeline('someuser')

    INPUT: a single twitter username

    OUTPUT: a pandas dataframe
    '''

    import tweepy

    from twintel._processing.data_frame import data_frame
    from twintel._resources.keys import key

    keys = key()

    access_token = keys['token']
    access_secret = keys['token_secret']
    consumer_secret = keys['consumer_secret']
    consumer_key = keys['consumer_key']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True)

    # THE LANGUAGE IS CURRENT HARD CODED (have to remove soon)

    searched_tweets = []
    last_id = -1

    while len(searched_tweets) < max_tweets:

        count = max_tweets - len(searched_tweets)

        try:
            new_tweets = api.search(q=query,
                                    count=count,
                                    max_id=str(last_id - 1),
                                    lang=language,
                                    tweet_mode='extended')

            if not new_tweets:
                break

            searched_tweets.extend(new_tweets)
            last_id = new_tweets[-1].id

        except tweepy.TweepError as e:
            break
    
    df = data_frame(searched_tweets)
    df.meta_keyword = str(query)

    return df
