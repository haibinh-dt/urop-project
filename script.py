import praw
import datetime as dt
import pandas as pd

# Fill in your API keys
CLIENT_ID = "-54AqnLAFs1hfJ9RZR29Yw"
CLIENT_SECRET = "gnHq8dtZt0aUvu22tQ-zqtQAIPPE4A"
USER_AGENT = "Scraper v1.0 by u/Reasonable-Tank-7799"

# Your custom input
keywords = ['LLM', 'human-AI collaboration', 'cothink', 'hybrid intelligence',
            'creative', 'labor', 'intellectual property', 'AI art',
            'ethical', 'copyright', 'law', 'rights'] # kw to search for
subreddits = ['AIRelationships', 'ChatGPT', 'ArtificialSentience', 'WritingWithAI'] # subreddits to crawl in
limit = 1 # limit on a single pair of keyword and subreddit

def initialize_reddit():
    reddit = praw.Reddit(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        user_agent= USER_AGENT,
    )

    return reddit

def build_dataset(reddit: praw.Reddit, keywords: list, subreddits: list, limit: int):
    data_dict = {"title": [],
                 "score": [],
                 "id": [],
                 "replied_to": [],
                 "num_comments": [],
                 "created_on": [],
                 "body": [],
                 "subreddit": [],
                 "type": []}

    for sub in subreddits:
        subreddit = reddit.subreddit(sub)

        for kw in keywords:
            # Collect posts
            for submission in subreddit.search(kw, limit = limit, sort = "new"):    # collect newest posts first
                data_dict["title"].append(submission.title)
                data_dict["score"].append(submission.score)
                data_dict["id"].append(submission.id)
                data_dict["replied_to"].append("")
                data_dict["num_comments"].append(submission.num_comments)
                data_dict["created_on"].append(dt.datetime.fromtimestamp(submission.created_utc))
                data_dict["body"].append(submission.selftext)
                data_dict["subreddit"].append(sub)
                data_dict["type"].append("post")

                # Collect comments of post
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    data_dict["title"].append("")
                    data_dict["score"].append(comment.score)
                    data_dict["id"].append(comment.id)
                    data_dict["replied_to"].append(comment.parent_id)
                    data_dict["num_comments"].append(0)
                    data_dict["created_on"].append(dt.datetime.fromtimestamp(comment.created_utc))
                    data_dict["body"].append(comment.body)
                    data_dict["subreddit"].append(sub)
                    data_dict["type"].append("comment")

    print(f"New reddit posts retrieved: {len(data_dict["title"])}")
    print(f"Time created: {dt.datetime.now()}")
    df = pd.DataFrame(data_dict)
    return df

if __name__ == "__main__":
    reddit = initialize_reddit()
    data = build_dataset(reddit, keywords, subreddits, limit)
    data.to_csv("crawl_reddit.csv", index=False)