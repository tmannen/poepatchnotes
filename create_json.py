from bs4 import BeautifulSoup
import os
import json
import re

patchnote_dir = "patchnotes"
poe_forum_url_root = "https://www.pathofexile.com/forum/view-thread/"
patchnotes = []

def handle_content_update(soup):
	# Big content updates are special cases and need different extraction rules
	notes = []
	for note in soup.find("div", {'class': 'content'}).findAll("li"):
		# Some changes - like ascendancies - are bunched up with the topic as 'strong' element before the list.
		# Add the strong element text in front of the patch note to make it more searchable
		if note.parent.findPrevious().name == 'strong':
			notes.append(note.parent.findPrevious().text + ": " + note.text)
		else:
			notes.append(note.text)

	return notes

for page in sorted(os.listdir(patchnote_dir)):
	if page == '.DS_Store':
		continue
	with open(os.path.join(patchnote_dir, page), "r") as forumpage:
		html = forumpage.read()

	soup = BeautifulSoup(html, "lxml")
	
	notes = handle_content_update(soup)

	title = soup.title.text
	topic = soup.find("h1", {'class': 'topBar'})
	url = poe_forum_url_root + page
	date = soup.find("span", {'class': 'post_date'}).text

	noteinfo = {}
	noteinfo['notes'] = notes
	noteinfo['title'] = title
	noteinfo['url'] = page
	try:
		noteinfo['patch'] = re.search('[0-9]([A-Za-z0-9]|\.)*', title).group(0)
	except AttributeError:
		# no patch numbers sometimes
		if 'hotfix' in title.lower():
			noteinfo['patch'] = "Hotfix"
		elif soup.find(string=re.compile("Content Update")) is not None:
			# If there's no patch number and page has 'Content update' in it, treat it as so
			noteinfo['patch'] = re.search('[0-9]([A-Za-z0-9]|\.)*', soup.find(string=re.compile("Content Update"))).group(0)
		else:
			noteinfo['patch'] = "N/A"

	noteinfo['date'] = date

	patchnotes.append(noteinfo)

with open(os.path.join("web", "data.json"), "w") as jsoni:
   json.dump(patchnotes, jsoni)
