TODO:

- add small footer that it's not affiliated with ggg?
- ~~add a blurb near the top saying that this contains all patch notes from forums and when it was last updated.~~ DONE
- scrape all ggg reddit and forum posts and create another tab for these changes? when searched, return the word searched and like 20 words around it? also a link to the post?
- poista se paskasti formatoitu legion patch note?
- search by patch/version number? DONE? searches also in patch
- ~~endless scrolling?~~ DONE
- Content update json creation - remove top level li-items?
- Automate json uploading to s3
- handle patch notes with no list items somehow? just text. maybe add them but prefix with BIGNOTE or something?
- TODO: trying to handle big notes: why new create_json has so many fewer notes? check what's in old notes but not in new
- test on https://www.pathofexile.com/forum/view-thread/12419, weirdly some replies get scraped?

How-to:

- Update patch notes json:
    - Run spider again (TODO: crawl only first page?) ```scrapy runspider patchforums_scraper.py```
    - run create_json: ```python create_json.py```
