import praw
from config import *
from time import sleep
import os
from better_profanity import profanity
from badwords import badwords
# import logging

# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
# for logger_name in ("praw", "prawcore"):
#     logger = logging.getLogger(logger_name)
#     logger.setLevel(logging.DEBUG)
#     logger.addHandler(handler)

print("Logging in...")
reddit = praw.Reddit(username = username,
			password = password,
			client_id = client_id,
			client_secret = client_secret,
			user_agent = "CummyBot1984 by /u/jartwobs")
print("Logged in!")


def comment(op): #Filter Spam
	if op.comment_karma + op.link_karma < 10:
		print("OP's karma is too low. Bypassing submission.")
		return False
	return True

def reply(title, body):
	replytext = (title +'\n\n' + body)
	profanity.load_censor_words(badwords)
	return profanity.censor(replytext)

def streaming():
	subreddit = reddit.subreddit("jartwobs")
	for submission in subreddit.stream.submissions(skip_existing=True):
		title = submission.title
		body = submission.selftext
		op = submission.author

		if comment(op):
			submission.reply(reply(title,body))
			print(f'Replied to {op.name}')

			sleep(10)

		sleep(10)

if __name__ == "__main__":
	streaming()


