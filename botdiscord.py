import praw
import asyncpraw
from time import sleep
from better_profanity import profanity
from datetime import datetime
import discord
import os
from badwords import badwords
from config import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

nltk.download('vader_lexicon')
# import nest_asyncio
# nest_asyncio.apply()


# import logging

# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# for logger_name in ("praw", "prawcore"):
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(handler)

client = discord.Client()

print("Logging in Reddit...")
reddit = praw.Reddit(username=username,
                     password=password,
                     client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     check_for_async=False)
print("Logged in Reddit!")


@client.event
async def on_ready():
    print('Logged in Discord as {0.user}'.format(client))


def comment(op, replytext):  # Filter Spam
    if op.comment_karma + op.link_karma < 10:
        print(f"{op.name}'s karma is too low. Bypassing submission.")
        return False
    elif SIA().polarity_scores(replytext)['compound'] <= -0.5:  # Added a sentinment analysis to score post.
        print(
            f"{op.name}'s SIA score is {SIA().polarity_scores(replytext)['compound']}, below the limit of 0.5. Bypassing submission.")
        return False
    return True


def reply(replytext):
    print(f"SIA score:{SIA().polarity_scores(replytext)['compound']}")
    profanity.load_censor_words(badwords)  # Censor slurs
    for i in badwords:
        replytext = replytext.replace(i, '*' * len(i))
    return profanity.censor(replytext)


@client.event
async def on_message(message):
    subreddit = reddit.subreddit("copypasta")
    channel = client.get_channel(channelid)
    for submission in subreddit.stream.submissions(skip_existing=True):
        title = submission.title
        body = submission.selftext
        op = submission.author
        if len(body) <= 1:  # Use title as comment if the post does not have body.
            replytext = title
        elif len(body) > 9900:
            replytext = body[:9899]  # Implements a maximum length of text
        else:
            replytext = body
        try:
            if comment(op, replytext):
                submission.reply(reply(replytext))
                print(f'Replied to {op.name}')
                time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                await channel.send(f"{time} --- Replied to {op.name}.")
                sleep(10)

            if not comment(op, body):
                time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                await channel.send(f"{time} --- Bypassed {op.name}, karma too low.")
        except:
            time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
            await channel.send(f"{time} --- Failed to reply. Error has occurred!!")


if __name__ == "__main__":
    client.run(discordtoken)