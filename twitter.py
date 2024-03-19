import praw

"""
client_id = "l3y6Fcw_RTsqR-St6pG1Yw",
client_secret = "VV8k08BdaGFODbnqWWaCxnL3lcSxNw",
user_agent = "my-app by u/tun_51789",
username = "tun_51789",
password = "Ela070042"
"""

reddit = praw.Reddit(
    client_id = "l3y6Fcw_RTsqR-St6pG1Yw",
    client_secret = "VV8k08BdaGFODbnqWWaCxnL3lcSxNw",
    user_agent = "my-app by u/tun_51789",
    username = "tun_51789",
    password = "Ela070042"
)

def getNewPost(num) -> list:
    subreddit = reddit.subreddit("temple")
    posts = subreddit.new(limit=num)
    post_arr = []
    for post in posts:
        #Title, author, likes, date created UTC
        post_arr.append([post.title, post.author, post.score, post.created_utc])
    return post_arr
