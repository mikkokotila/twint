import pandas as pd
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def data_frame(data):

    df1 = pd.DataFrame([[tweet.user.statuses_count,
                        tweet.user.favourites_count,
                        tweet.user.followers_count,
                        tweet.user.friends_count,
                        tweet.user.listed_count,
                        tweet.user.screen_name,
                        pd.to_datetime(tweet.user.created_at),
                        tweet.user.default_profile,
                        tweet.user.default_profile_image,
                        tweet.user.description,
                        tweet.user.location,
                        tweet.user.time_zone,
                        tweet.created_at,
                        tweet.id_str,
                        tweet.retweet_count,
                        tweet.favorite_count,
                        tweet.user.profile_image_url_https] for tweet in data])

    df1.columns = ('user_tweets',
                   'user_favourites',
                   'user_followers',
                   'user_following',
                   'user_listed',
                   'handle',
                   'user_created_at',
                   'default_profile',
                   'egg_account',
                   'description',
                   'location',
                   'timezone',
                   'tweet_created_at',
                   'tweet_id',
                   'retweet_count',
                   'favorite_count',
                   'user_image')

    l2 = []

    data_backup = data

    temp = []
    for tweet in data:
        if 'media' in tweet.entities:
            for image in tweet.entities['media']:
                temp.append(image['media_url'])
        else:
            temp.append(None)

    df1['media'] = temp

    try:

        data = [data[i].entities for i in range(len(data))]

        for tweet in data:

            l = []

            try:
                l.append(tweet['urls'][0]['expanded_url'])
                l.append(tweet['urls'][0]['url'])

            except:
                l.append("None")
                l.append("None")

            l2.append(l)

    except:

        for tweet in data.entities:

            l = []

            try:
                l.append(tweet['urls'][0]['expanded_url'])
                l.append(tweet['urls'][0]['url'])
            except:
                l.append("None")
                l.append("None")

            l2.append(l)

    df4 = pd.DataFrame(l2)
    #df4 = df4.transpose()

    df4.columns = ['expanded_url','url']

    l = []

    for url in df4.expanded_url:

        try:
            l.append(url.split('/')[2].replace('www.', ''))
        except:
            l.append('None')

    df4['site_url'] = l

    data = data_backup

    #try:
    #    df4['text'] = [tweet.text for tweet in data]

    #except: 
    
    df4['text'] = [tweet._json['full_text'] for tweet in data]

    df = pd.concat([df1, df4], axis=1)
    del df4, df1, l2, l

    low_quality = pd.DataFrame({'default_profile': df.default_profile == True,
                                'egg_account': df.egg_account == True,
                                #'no_bio_url' : df.url == "",
                                'no_description': df.description == "",
                                'follows_more': df.user_following > df.user_followers,
                                'spam_account': df.user_tweets > 50 * df.user_followers,
                                'many_tweets': df.user_tweets > 50000,
                                'created_2016': df.user_created_at.dt.year == 2018,
                                'many_favorites': df.user_favourites > df.user_tweets,
                                'few_listed': df.user_listed < df.user_followers / 100})

    df4 = pd.DataFrame(10 - low_quality.sum(axis=1))
    df4.columns = ['quality_score']
    df = pd.concat([df4, df], axis=1)

    # COUNTING INFLUENCE SCORE
    try:
        df5 = pd.DataFrame((pd.to_datetime('today') - df.user_created_at).dt.days + 2)
    except TypeError:
        df5 = pd.DataFrame({'null' : [np.nan for i in range(len(df))]})

    df5.columns = ['days_since_creation']

    influence = pd.DataFrame({
            'listed_per_tweet': np.log(df.user_listed+1 / df.user_tweets+1),
            'followers_per_tweet': np.log(df.user_followers+1 / df.user_tweets+1),
            'followers_per_day': np.log(df.user_followers+1 / df5['days_since_creation']+1),
            'listed_per_day': np.log(df.user_listed+1 / df5['days_since_creation']+1),
            'listed_per_follower': np.log(df.user_listed+1 / df.user_followers+1)
        })

    df5['influence_score'] = pd.DataFrame(influence.sum(axis=1))
    df5['reach_score'] = df.user_followers / 10 * df5.influence_score + 1

    df5['influence_score'] = df5.influence_score.replace([np.inf, -np.inf], 1)

    df = pd.concat([df5, df], axis=1)

    sid = SentimentIntensityAnalyzer()
    l = [sid.polarity_scores(tweet).values() for tweet in df.text]

    df6 = pd.DataFrame(l, columns=('compound', 'neu', 'neg', 'pos'))

    df = pd.concat([df, df6], axis=1)
    del df5, df6, l
    return df
