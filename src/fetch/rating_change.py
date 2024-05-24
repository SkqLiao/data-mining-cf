import json
from lib.api import API
from lib.logger import Logger
import os

data_dir = './data/rating_changes'
log_dir = './logs'

os.makedirs(data_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

logger = Logger(os.path.join(log_dir, 'contest.log'))
api = API('https://codeforces.com/api/contest.ratingChanges', logger)

def fetchContests(contest_id):
    return api.getResponse(params={'contestId': contest_id}, retry=1)

if __name__ == '__main__':
    logger.info('Start fetching contests rating changes')
    for i in range(1500, 2000):
        rating_changes = fetchContests(i)
        if rating_changes is None:
            logger.error(f'Failed to fetch rating changes in contest {i}')
            continue
        json.dump(rating_changes, open(os.path.join(data_dir, f'{i}.json'), 'w'), indent=4)
        logger.info(f'Fetched {len(rating_changes)} rating changes in contest {i}')