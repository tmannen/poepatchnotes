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
		# super scuffed.. basically in Heist they updated patch notes so the skill is not the parent of the note
		# this tests whether it has italic(?) text after previous strong element, in which case it's most likely a skill?
		# fix later. maybe have a dict with all skills and can match previous strong? might not work, wrong skill might get added
		# later: go through all strongs or something?
		if note.parent.findPrevious().findPrevious().name== 'em':
			probable_skill_name = note.parent.findPrevious().findPrevious().findPrevious().findPrevious().text
			notes.append(probable_skill_name + ": " + note.text)
			
		else:
			# TODO: kinda scuffed, fix?
			if 'a href' not in str(note):
				notes.append(note.text)
			else:
				print(note)

	if len(notes) == 0:
		print("no notes?")
		print(soup.title)

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
