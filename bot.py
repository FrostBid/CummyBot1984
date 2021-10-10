import praw
import config
import time
import os

def bot_login():
	print "Logging in..."
	r = praw.Reddit(username = config.username,
				password = config.password,
				client_id = config.client_id,
				client_secret = config.client_secret,
				user_agent = "CummyBot1984 by /u/jartwobs")
	print "Logged in!"
	return r


def copypaste:
