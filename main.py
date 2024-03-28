import requests
import json
import logging
import datetime
from time import sleep

api = 'https://codeforces.com/api/{methodName}'
problem_vote = {}
problem_rating = {}
logger = None


def getUserRawSubmissions(handle):
    # if file data/handle.json exists, return the data
    try:
        with open('data/{}.json'.format(handle), 'r') as f:
            logger.info('handle: %s, data/%s.json exists', handle, handle)
            return json.load(f)
    except FileNotFoundError:
        pass

    method = 'user.status'
    url = api.format(methodName=method)
    params = {'handle': handle}

    def getResponse(url, params):
        try:
            return requests.get(url, params=params).json()
        except requests.exceptions.ConnectionError:
            return None

    response = getResponse(url, params)
    try_count = 1
    while response is None:
        logger.warning('handle: %s, get response failed', handle)
        logger.warning(
            'try again after %d seconds, failed %d times', 5 * try_count, try_count)
        sleep.sleep(5 * try_count)
        response = getResponse(url, params)
        try_count += 1
    with open('data/{}.json'.format(handle), 'w') as f:
        json.dump(response, f)
    logger.info('handle: %s, data/%s.json saved', handle, handle)
    return response


def extractSubmissions(submission_json, handle):
    global problem_rating
    if submission_json['status'] != 'OK':
        logger.warning('handle: %s, status: %s, comment: %s', handle,
                       submission_json['status'], submission_json['comment'])
        return []
    submissions = []
    total = 0
    for submission in submission_json['result']:
        if submission['verdict'] != 'OK':
            continue
        try:
            submissions.append(
                str(submission['contestId']) + str(submission['problem']['index']))
            problem_rating[submissions[-1]
                           ] = int(submission['problem']['rating']) // 100 * 100
            total += 1
        except KeyError:
            logger.warning(
                'Error: handle: %s, id: %d', handle, submission['id'])
    submissions = list({v: v for v in submissions}.values())
    logger.info('handle: %s, get submission: %d', handle, total)
    return submissions


def readHandles():
    with open('handles.txt', 'r') as f:
        handles = f.readlines()
    handles = [handle.strip() for handle in handles]
    print(handles)
    return [handle.split()[1] for handle in handles][::5]


def voteProblem(submissions):
    global problem_vote
    for problem in submissions:
        if problem in problem_vote:
            problem_vote[problem] += 1
        else:
            problem_vote[problem] = 1


def getTopKProblem(k, min_rating, handles):
    if k == -1:
        k = len(problem_vote)
    now = datetime.datetime.now()
    problem_vote_sorted = sorted(
        problem_vote.items(), key=lambda x: x[1], reverse=True)
    with open('top_k_problem{}.txt'.format(now.strftime('%Y%m%d-%H-%M')), 'w') as f:
        f.write('handles: {}\n'.format(', '.join(handles)))
        f.write('mininum problem rating: {}\n'.format(min_rating))
        f.write('top {} problems:\n'.format(k))
        for problem in problem_vote_sorted:
            prob, count = problem[0], problem[1]
            rating = problem_rating.get(prob, 0)
            if rating < min_rating:
                continue
            f.write('{}: rating={}, count={}\n'.format(
                prob, rating, count))
            k -= 1
            if k == 0:
                break
    logger.info('top_k_problem%s.txt saved',
                now.strftime('%Y%m%d-%H%M'))


def setupLogger():
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)


if __name__ == '__main__':
    setupLogger()
    k = int(input('input k: (input -1 to get all problems)'))
    rating = int(input('input mininum problem rating:'))
    handles = readHandles()
    now, total = 1, len(handles)
    for handle in handles:
        logger.info('handle: %s, %d/%d', handle, now, total)
        info = getUserRawSubmissions(handle)
        submissions = extractSubmissions(info, handle)
        voteProblem(submissions)
        now += 1
        # sleep(1)
    getTopKProblem(k, rating, handles)
