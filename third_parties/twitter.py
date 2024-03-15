import os
import logging
from dotenv import load_dotenv

load_dotenv()
import tweepy

logger = logging.getLogger("twitter")

twitter_client = tweepy.Client(
    bearer_token='AAAAAAAAAAAAAAAAAAAAAL0WswEAAAAAl3xy0Y1PkD%2B8ltUPX8xdqNgZrds%3DdcpqRmOHJdpKkWP9Ys71wJFpPQwSYD4l1fmdz9cMDqU4Vm4NiS',
    consumer_key='eZoxTV4yrYycxQn9J2q1G44Ge',
    consumer_secret='FNmYfnXLvDExkpauXNtCjLca5hfnu7J9TeVOWXc42Vx8VDM284',
    access_token='1682784344-jtQhZ7cByRmjS7niBdl3xcGjJfMFKUCEvxgP5QM',
    access_token_secret='5GBWtPRZtvROBIGQZXlEcslh79SexPbWjYCQPUsP3FL5N',
)


def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    user_id = twitter_client.get_user(username=username).data.id
    tweets = twitter_client.get_users_tweets(
        id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
    )

    tweet_list = []
    for tweet in tweets.data:
        tweet_dict = {}
        tweet_dict["text"] = tweet["text"]
        tweet_dict["url"] = f"https://twitter.com/{username}/status/{tweet.id}"
        tweet_list.append(tweet_dict)

    return tweet_list


if __name__ == "__main__":
    print(scrape_user_tweets(username="@elonmusk"))