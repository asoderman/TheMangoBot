'''
A basic reddit bot built to perpetuate a meme
'''

import time
import praw
import os
import datetime
import re


USERNAME = ''
PASSWORD = ''
MASTER = ''
KEYWORDS = ['mango does', 'mango do', 'what does mango', 'mango did']
USER_AGENT = "ThatsTheMango 0.1 by /u/ %s" % MASTER

# Read in the credentials
with open("config.txt", "r") as f:
	USERNAME = f.readline().replace('\n','')
	PASSWORD = f.readline().replace('\n', '')
	MASTER = f.readline()

def main():
	write_log("Script started")
	r = praw.Reddit(user_agent=USER_AGENT)
	r.login(USERNAME, PASSWORD, disable_warning=True)

	write_log("Logged in")
	while True:
		subreddit = r.get_subreddit("ssbm")
		ddt = ''

		## Find the daily discussion thread
		for submission in subreddit.get_hot(limit=5):
			if re.search("Daily Discussion Thread", submission.title, re.IGNORECASE):
				ddt = submission

		## Extract the comments (we don't care about the order just the content)
		comments = praw.helpers.flatten_tree(ddt.comments)

		parse_comments(comments)
		write_log("Sleeping for 30 mins")
		time.sleep(1800)

def check_messages(r):
	# NOT IMPLEMENTED
	for message in r.get_unread(limit=None):
		send_to_master(message.subject, message.body, r)

def send_to_master(subject, message, r):
	# NOT IMPLEMENTED
	r.send_message(MASTER, subject, message)

def parse_comments(comments):
	# Parses the comments for phrases defined in the keywords constant
	for comment in comments:
		if not isinstance(comment, praw.objects.Comment):
			## Code to ensure the comment is actually a comment. Otherwise errors happen
			continue
		else:
			for word in KEYWORDS:
				if word in comment.body.lower() and not replied(comment.id):
					reply_to_comment(comment)
	write_log("Parsed %d comments" % len(comments))

def reply_to_comment(comment):
	# Reply to the comment with the signature phrase
	write_posts_replied_to([comment.id])
	comment.reply("That's the Mango.")
	write_log("Replied to /u/%s " % str(comment.author))
	
def write_posts_replied_to(post_ids):
	# Takes a list of post_ids that were replied to and appends them to a file to ensure multiple
	# replies are not sent
	with open("posts_replied_to.txt", "a") as f:
		for id in post_ids:
			f.write(id + '\n')

def replied(post_id):
	# Checks to see if a post was replied to
	if not os.path.isfile("posts_replied_to.txt"):
		with open("posts_replied_to.txt", "w"):
			pass
		return False
	with open("posts_replied_to.txt", "r") as f:
		ids = f.read().split('\n')
		if post_id in ids:
			return True
		else:
			return False

def write_log(message):
	# Writes a message to log.txt
	now = datetime.datetime.now()
	out = str(now) + ' - ' + message + '\n'
	with open("log.txt", "a") as f:
		f.write(out)


if __name__ == '__main__':
	main()