#setting ig login session cookie

from argparse import ArgumentParser
from ctypes import sizeof
from glob import glob
from os.path import expanduser
from platform import system
import random
from sqlite3 import OperationalError, connect
import time

try:
	from instaloader import ConnectionException, Instaloader
except ModuleNotFoundError:
	raise SystemExit("Instaloader not found.\n  pip install [--user] instaloader")


def get_cookiefile():
	default_cookiefile = {
		"Windows": "~/AppData/Roaming/Mozilla/Firefox/Profiles/*/cookies.sqlite",
		"Darwin": "~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite",
	}.get(system(), "~/.mozilla/firefox/*/cookies.sqlite")
	cookiefiles = glob(expanduser(default_cookiefile))
	if not cookiefiles:
		raise SystemExit("No Firefox cookies.sqlite file found. Use -c COOKIEFILE.")
	return cookiefiles[0]


def import_session(cookiefile, sessionfile):
	print("Using cookies from {}.".format(cookiefile))
	conn = connect(f"file:{cookiefile}?immutable=1", uri=True)
	try:
		cookie_data = conn.execute(
			"SELECT name, value FROM moz_cookies WHERE baseDomain='instagram.com'"
		)
	except OperationalError:
		cookie_data = conn.execute(
			"SELECT name, value FROM moz_cookies WHERE host LIKE '%instagram.com'"
		)
	instaloader = Instaloader(max_connection_attempts=1)
	instaloader.context._session.cookies.update(cookie_data)
	username = instaloader.test_login()
	if not username:
		raise SystemExit("Not logged in. Are you logged in successfully in Firefox?")
	print("Imported session cookie for {}.".format(username))
	instaloader.context.username = username
	instaloader.save_session_to_file(sessionfile)


if __name__ == "__main__":
	p = ArgumentParser()
	p.add_argument("-c", "--cookiefile")
	p.add_argument("-f", "--sessionfile")
	args = p.parse_args()
	try:
		import_session(args.cookiefile or get_cookiefile(), args.sessionfile)
	except (ConnectionException, OperationalError) as e:
		raise SystemExit("Cookie import failed: {}".format(e))


#data scraping starts from here
import instaloader
import csv

bot4 = instaloader.Instaloader()

# login
try:
	bot4.load_session_from_file("wot_iz1")
except FileNotFoundError:
	bot4.context.log("Session file does not exist yet")


profile = instaloader.Profile.from_username(bot4.context, 'gap')

# Retrieving all posts in an object
if not (profile.is_private):
	posts = profile.get_posts()

followers = profile.get_followers()

with open('data.csv', 'w', encoding='UTF8', newline='') as f:
	writer = csv.writer(f)

	header = ['post_url', 'date']
	writer.writerow(header)

	limit = 0
	public_list = []
	for follower in followers:
		limit += 1
		tempProfile = instaloader.Profile.from_username(bot4.context, follower.username)
		if not (tempProfile.is_private):
			if not (tempProfile.is_verified): 	

				public_list.append(tempProfile)
				print(follower.username)
				posts = tempProfile.get_posts()
				pic_limit = 0
				for i, post in enumerate(posts, 1):
					time.sleep(random.uniform(2, 4)	)
					bot4.download_pic(f'{tempProfile.username}_{i}', post.url, post.date_utc)
					#writer.writerow([post.url,post.date])
					pic_limit+=1

					print(follower.username, " ", i)
					if pic_limit == 10:
						break
				
		time.sleep(random.uniform(2, 4)	)
		print(limit, " ", len(public_list))
		if limit == 10: 
			break

	print(len(public_list) , "  -total num ")
