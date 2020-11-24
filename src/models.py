from sqlalchemy import (Table, Column, Integer,
                        ForeignKey, String, DateTime)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

tweet_hashtags = Table(
    'tweet_hashtag',
    Base.metadata,
    Column('tweet_id', Integer, ForeignKey('tweet.id')),
    Column('hashtag_id', Integer, ForeignKey('hashtag.id'))
)


class Tweet(Base):
    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True)
    tweetid = Column(String(30))
    text = Column(String(280))
    created = Column(DateTime)
    favorites = Column(Integer)
    retweets = Column(Integer)
    hashtags = relationship(
        "HashTag",
        secondary=tweet_hashtags,
        backref="tweets")

    def __repr__(self):
        return (f"{self.__class__.__name__}('{self.tweetid}', "
                f"'{self.text}', '{self.created}', "
                f"'{self.favorites}', '{self.retweets}')")


class HashTag(Base):
    __tablename__ = 'hashtag'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return (f"{self.__class__.__name__}"
                f"('{self.name}')")
