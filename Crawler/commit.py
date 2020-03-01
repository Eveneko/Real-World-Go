import requests
import json
import os
import time
import logging
from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import ConnectionError
import repositories

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

"""
sha	    string	SHA or branch to start listing commits from. Default: the repository’s default branch (usually master).
path	string	Only commits containing this file path will be returned.
author	string	GitHub login or email address by which to filter by commits author.
since	string	Only commits after this date will be returned. 
                This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.
until	string	Only commits before this date will be returned. 
                This is a timestamp in ISO 8601 format: YYYY-MM-DDTHH:MM:SSZ.
"""
COMMIT_PARAMS = {
    'sha': '',
    # 'path': '',
    # 'author': '',
    # 'since': '2000-01-01:00:00Z',
    # 'until': ''
}
COMMIT_HEADERS = {
    'Connection': 'close',
}

"""
protected	boolean	Setting to true returns only protected branches. When set to false, 
            only unprotected branches are returned. Omitting this parameter returns all branches.
"""
BRANCH_PARAMS = {
    'protected': False,
}
BRANCH_HEADERS = {
    'Connection': 'close',
}

OUTPATH = 'output/'


def main():
    if not os.path.exists(OUTPATH):
        os.mkdir(OUTPATH)
    for repo in repositories.repo_list:
        repo_path = os.path.join(OUTPATH, repo.split('/')[-1])
        if not os.path.exists(repo_path):
            os.mkdir(repo_path)
        commit_path = os.path.join(OUTPATH, repo.split('/')[-1], 'commits')
        if not os.path.exists(commit_path):
            os.mkdir(commit_path)
        branch_url = 'https://api.github.com/repos/' + repo + '/branches'
        branches = requests.get(url=branch_url, params=BRANCH_PARAMS, headers=BRANCH_HEADERS)
        logger.info('Repositories ' + repo.split('/')[-1] + ': ' + branch_url)
        for branch in branches.json():
            while True:
                try:
                    file_name = os.path.join(commit_path, branch['name'])
                    commit_url = 'https://api.github.com/repos/' + repo + '/commits'
                    COMMIT_PARAMS['sha'] = branch['name']
                    response = requests.get(url=commit_url, params=COMMIT_PARAMS, headers=COMMIT_HEADERS)
                    logger.info('- Branch ' + branch['name'] + ': ' + commit_url)
                    data = json.dumps(response.json(), sort_keys=True, indent=2)
                    with open(file_name, 'w+') as f:
                        f.writelines(data)
                    break
                except (ConnectionError, ConnectionRefusedError, NewConnectionError, MaxRetryError) as e:
                    logger.warning('Connection Refused! Sleep For 5 Seconds...')
                    time.sleep(5)
    logger.info('All Repositories Done')


if __name__ == '__main__':
    main()
