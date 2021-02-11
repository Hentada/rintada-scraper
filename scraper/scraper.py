# Library imports
from ftplib import FTP
import praw
import json
import requests


# Save image file to ftp
def save_file(ftp, url, id_, display=True):
	# Display status
	if display:
		print("Preparing to save file at {} to file named {}".format(url, id_))

	# Get file-like image object at url
	r = requests.get(url, stream=True)

	# Save raw
	ftp.storbinary("STOR {}".format(id_), r.raw)

	if display:
		print("Successfully saved file.")


if __name__ == "__main__":
	# Get client info
	with open("client.json", "r") as f:
		client = json.load(f)

	# Reddit api
	reddit = praw.Reddit(client_id=client["id"], client_secret=client["secret"], user_agent=client["user-agent"], username=client["username"], password=client["password"])

	# FTP client
	ftp = FTP()
	ftp.connect(host=client["ftp-ip"], port=8000)
	ftp.login(user="moogloof", passwd=client["ftp-passwd"])

	# Change to image directory
	ftp.cwd("moogwoof/rin-images")

	# Rin subreddit
	subr = reddit.subreddit("OneTrueTohsaka")

	for submission in subr.top("all"):
		# Save image to file in ftp
		save_file(ftp, submission.url, submission.url.split("/")[-1])

	# Display full list of image files
	print(ftp.nlst())

	# Quit ftp conn
	ftp.quit()

