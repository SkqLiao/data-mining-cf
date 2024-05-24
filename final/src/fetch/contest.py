import json
from lib.api import API
from lib.logger import Logger
import os

data_dir = './data/contests'
log_dir = './logs'

os.makedirs(data_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

logger = Logger(os.path.join(log_dir, 'contest.log'))
api = API('https://codeforces.com/api/contest.list', logger)

def fetchContests(gym=False):
    return api.getResponse(params={'gym': gym})

if __name__ == '__main__':
    logger.info('Start fetching contests')
    contests_cf = fetchContests()
    contests_gym = fetchContests(gym=True)
    json.dump(contests_cf, open(os.path.join(data_dir, 'cf.json'), 'w'), indent=4)
    logger.info(f'Fetched {len(contests_cf)} contests hosted by Codeforces')
    json.dump(contests_gym, open(os.path.join(data_dir, 'gym.json'), 'w'), indent=4)
    logger.info(f'Fetched {len(contests_gym)} contests in gym')