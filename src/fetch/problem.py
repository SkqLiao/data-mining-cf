import json
from lib.api import API
from lib.logger import Logger
from time import sleep
import os

data_dir = './data/problems'
log_dir = './logs'


os.makedirs(data_dir, exist_ok=True)
os.makedirs(log_dir, exist_ok=True)

logger = Logger(os.path.join(log_dir, 'problem.log'))
api = API('https://codeforces.com/api/problemset.problems', logger)
exist_problems = set()
problem_info = []

def fetchProblems(tag):
    local_file = os.path.join(data_dir, '{tag}.json'.format(tag=tag))
    problems = None
    if os.path.exists(local_file):
        problems = json.load(open(local_file))
        logger.info('Load "{tag}" locally: total {cnt} problems'.format(tag=tag, cnt=len(problems)))
    else:
        logger.info('Load "{tag}" remotely: total {cnt} problems'.format(tag=tag, cnt=len(problems)))
        response = api.getResponse({'tags': tag})
        problems, solved = response['problems'], response['problemStatistics']
        assert len(problems) == len(solved)
        for i in range(len(problems)):
            problem, solve = problems[i], solved[i]
            assert problem['contestId'] == solve['contestId']
            assert problem['index'] == solve['index']
            problems[i]['solvedCount'] = solve['solvedCount']
        for problem in problems:
            pid = '{contestId}-{index}'.format(contestId=problem['contestId'], index=problem['index'])
            if pid in exist_problems:
                continue
            exist_problems.add(pid)
            problem_info.append(problem)
    return problems

"""
Extract tags from problems
"""
def extractTags(problems):
    tags = set()
    for problem in problems:
        for tag in problem['tags']:
            tags.add(tag)
    return tags

"""
Get all problems with the given tags, and explore all tags appeared in the problems
"""
def nextProblem(tags):
    from queue import Queue
    finished_tags = {}
    q = Queue()
    for tag in tags:
        q.put(tag)
    while not q.empty():
        tag = q.get()
        if tag in finished_tags:
            continue
        problems = fetchProblems(tag)
        if problems is None:
            continue
        tags = extractTags(problems)
        for t in tags:
            if t not in finished_tags:
                q.put(t)
        finished_tags[tag] = len(finished_tags)
        yield tag, problems
    logger.info('Finished fetching problems by {} tags with {} problems'.format(len(finished_tags), len(problem_info)))
    json.dump(problem_info, open(os.path.join(data_dir, 'problem_info.json'), 'w'))

if __name__ == '__main__':
    logger.info('Start fetching problems by tags')
    tag = ['implementation']
    for tag, problems in nextProblem(tag):
        sleep(2)
    
    