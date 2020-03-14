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
milestone	integer 要么 string	如果integer通过，则应按其number字段引用里程碑。如果*传递了字符串，则将接受任何具有里程碑意义的问题。如果none传递了字符串，则返回没有里程碑的问题。
state	    string	指示要返回的问题的状态。可以是open，closed或all。默认：open
assignee	string	可以是用户名。通过在none对问题没有分配的用户，并*分配给任何用户的问题。
creator	    string	创建问题的用户。
mentioned	string	问题中提到的用户。
labels	    string	逗号分隔标签名称的列表。例：bug,ui,@high
sort	    string	结果排序依据。可以是created，updated，comments。默认：created
direction	string	排序的方向。可以是asc或desc。默认：desc
since	    string	仅返回在此时间或之后更新的问题。这是ISO 8601格式的时间戳记：YYYY-MM-DDTHH:MM:SSZ。
"""
ISSUE_PARAMS = {

}
ISSUE_HEADERS = {
    'Connection': 'close',
}

OUTPATH = 'Crawler/output/'


def main():
    if not os.path.exists(OUTPATH):
        os.mkdir(OUTPATH)
    for repo in repositories.repo_list:
        repo_path = os.path.join(OUTPATH, repo.split('/')[-1])
        if not os.path.exists(repo_path):
            os.mkdir(repo_path)
        issue_url = 'https://api.github.com/repos/' + repo + '/issues'
        while True:
            try:
                response = requests.get(url=issue_url, params=ISSUE_PARAMS, headers=ISSUE_HEADERS)
                logger.info('Issues ' + repo.split('/')[-1] + ': ' + issue_url)
                data = json.dumps(response.json(), sort_keys=True, indent=2)
                file_name = os.path.join(repo_path, 'issues')
                with open(file_name, 'w+') as f:
                    f.writelines(data)
                break
            except (ConnectionError, ConnectionRefusedError, NewConnectionError, MaxRetryError) as e:
                logger.warning('Connection Refused! Sleep For 5 Seconds...')
                time.sleep(5)
    logger.info('All issues Done')


if __name__ == '__main__':
    main()
