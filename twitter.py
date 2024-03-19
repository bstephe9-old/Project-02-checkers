import tweepy
import pandas as pd


API_Key = "nK0no7k7Qugn6cXjlufgWwaaM"
API_Key_Secret = "jtvVuAuKMsbcw7rJiwcXPtSH38S1PAcrwuvCJBBEE2JnWXgHFP"
Access_token = "1768474190628233217-llh7BQek11jD0X1SOXqGvqxdhEpkO5"
Access_token_secret = "VkzYDsH4PgUOTiDvyxiOcHwKI9wbxBLip6wBNk622iVzx"

auth = tweepy.OAuth1UserHandler(
    API_Key, API_Key_Secret,
    Access_token, Access_token_secret
)

api = tweepy.API(auth, wait_on_rate_limit=True)

search_query = "'Elon Musk' 'fired' -filter:retweets AND -filter:replies AND -filter:links"
no_of_tweets = 10


if __name__ == "__main__":
    try:
        tweets = api.search_tweets(q=search_query, lang='en', count=no_of_tweets, tweet_mode='extended')
        attributes_container = [[tweet.user_name, tweet.created_at, tweet.favorite_count, tweet.source] for tweet in tweets]
        columns = ['User', 'Date Created', 'Likes', 'Source of Tweet']

        tweets_df = pd.DataFrame(attributes_container, columns = columns)

        print(tweets_df)
    except BaseException as e:
        print(e)
