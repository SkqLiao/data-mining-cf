import requests
from bs4 import BeautifulSoup
from time import sleep
import os
from lib.logger import Logger

data_dir = './data/tags'
log_dir = './logs'
os.makedirs(data_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)
logger = Logger(os.path.join(log_dir, 'tag.log'))

def scrape_dark_td_content(url):
    #retry 3 times
    response = None
    for i in range(3):
        try:
            response = requests.get(url)
            break
        except Exception as e:
            logger.warning(f'Failed to fetch {url} for {i + 1} times')
            sleep(10)
            
    soup = BeautifulSoup(response.text, 'html.parser')
    tags = soup.find_all('a', class_='notice')
    return set(tag.text for tag in tags)


max_page = 94
template_url = 'https://codeforces.com/problemset/page/{page}'
tags = set()

logger.info('Start fetching tags from page 1 to {max_page}'.format(max_page=max_page))

for i in range(1, max_page + 1):
    url = template_url.format(page=i)
    new_tags = scrape_dark_td_content(url)
    tags = tags.union(new_tags)
    logger.info(f'Fetched {len(new_tags)} tags from page {i}, {len(tags)} tags in total')
    logger.info('tags: {tags}'.format(tags=tags))
    sleep(10)

with open(os.path.join(data_dir, 'tags.txt'), 'w') as f:
    f.write('\n'.join(tags))