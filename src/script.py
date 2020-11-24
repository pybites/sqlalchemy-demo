import json

from dateutil.parser import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Tweet, HashTag, Base

engine = create_engine('sqlite:///:memory:', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


def import_twitter_data(tweets_dump='all_tweets.js'):
    with open(tweets_dump) as f:
        data = json.loads(f.read())

    for row in data:
        tweet = row['tweet']
        tags = [tag['text'] for tag in tweet['entities']['hashtags']]

        new_tweet = Tweet(tweetid=tweet['id'],
                          text=tweet['full_text'],
                          created=parse(tweet['created_at']),
                          favorites=tweet['favorite_count'],
                          retweets=tweet['retweet_count'])

        for tag in tags:
            htag = session.query(HashTag).filter_by(name=tag).first()

            if not htag:
                htag = HashTag(name=tag)
                session.add(htag)

            new_tweet.hashtags.append(htag)

        session.add(new_tweet)

    session.commit()


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    import_twitter_data()
    breakpoint()
    # session.query(Tweet).order_by(Tweet.favorites.desc())[:10]: ...
