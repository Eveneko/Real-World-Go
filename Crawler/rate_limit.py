import requests
import json
import os
import time
from urllib3.exceptions import NewConnectionError, MaxRetryError
from requests.exceptions import ConnectionError
from log import FileLogger

URL = 'https://api.github.com/rate_limit'
OUTPATH = 'Crawler/output/'


def main():
    while True:
        try:
            response = requests.get(url=URL)
            data = json.dumps(response.json(), sort_keys=True, indent=2)
            file_name = os.path.join(OUTPATH, 'rate_limit')
            with open(file_name, 'w+') as f:
                f.writelines(data)
            break
        except (ConnectionError, ConnectionRefusedError, NewConnectionError, MaxRetryError) as e:
            FileLogger.warning('Connection Refused! Sleep For 5 Seconds...')
            time.sleep(5)
    FileLogger.info('Get Rate_limit Done')


if __name__ == '__main__':
    main()
