import praw
from config import *
from time import sleep
from better_profanity import profanity
from badwords import badwords
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk
import pandas as pd

nltk.download('vader_lexicon')
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
			user_agent = user_agent)
print("Logged in!")

def logging(op,replytext): #log timestamp
	f = open('log.txt', "a")
	time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
	f.write(f"{time} --- Replied to {op.name}, SIA score is {SIA().polarity_scores(replytext)['compound']}.\n")
	f.close()


def comment(op,replytext):
	f = open('log.txt', "a")
	time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
	if op.comment_karma + op.link_karma < 10: #Filter Spam
		print(f"{op.name}'s karma is too low. Bypassing submission.")
		f.write(f"{time} --- Bypassed {op.name}, karma too low.\n")
		f.close()
		return False
	elif SIA().polarity_scores(replytext)['compound'] <= -0.5: # Added a sentinment analysis to score post.
		print(f"{op.name}'s SIA score is {SIA().polarity_scores(replytext)['compound']}, below the limit of 0.5. Bypassing submission.")
		f.write(f"{time} --- Bypassed {op.name}, SIA score is {SIA().polarity_scores(replytext)['compound']}, below the limit of 0.5.\n")
		f.close()
		return False
	f.close()
	return True

def reply(title, replytext):
	print(f"SIA score:{SIA().polarity_scores(replytext)['compound']}")
	profanity.load_censor_words(badwords) #Censor slurs
	for i in badwords:
		replytext = replytext.replace(i, '*' * len(i))
	return profanity.censor(replytext)

def streaming():
	subreddit = reddit.subreddit("copypasta")
	for submission in subreddit.stream.submissions(skip_existing=True):
		title = submission.title
		body = submission.selftext
		op = submission.author
	if len(body) <= 1:  # Use title as comment if the post does not have body.
		replytext = title
	elif len(body) > 9900
		replytext = body[:9899]  # Implements a maximum length of text
		try:
			if comment(op,replytext):
				submission.reply(reply(replytext))
				print(f'Replied to {op.name}')
				logging(op,replytext)
				sleep(10)

		except:
			print('Failed to reply. Error has occurred. Please check.')

if __name__ == "__main__":
	streaming()


