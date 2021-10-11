import praw
from config import *
from time import sleep
from better_profanity import profanity
from badwords import badwords
from datetime import datetime


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

def logging(op):
	f = open('log.txt', "a")
	time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
	f.write(f"{time} --- Replied to {op.name}.\n")
	f.close()


def comment(op): #Filter Spam
	if op.comment_karma + op.link_karma < 10:
		print(f"{op.name}'s karma is too low. Bypassing submission.")
		f = open('log.txt', "a")
		time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
		f.write(f"{time} --- Bypassed {op.name}, karma too low.\n")
		f.close()
		return False
	return True

def reply(title, body): #Censor slurs
	replytext = (title +'\n\n' + body)
	profanity.load_censor_words(badwords)
	return profanity.censor(replytext)

def streaming():
	subreddit = reddit.subreddit("copypasta")
	for submission in subreddit.stream.submissions(skip_existing=True):
		title = submission.title
		body = submission.selftext
		op = submission.author

		if comment(op):
			submission.reply(reply(title,body))
			print(f'Replied to {op.name}')
			logging(op)
			sleep(10)

if __name__ == "__main__":
	streaming()


