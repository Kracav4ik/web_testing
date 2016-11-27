import time

import requests
import sys

if __name__ == '__main__':
    time.sleep(10)
    url = 'http://localhost:6543/answer'
    requests.get(url, params={
        "result": "awe",
        "run_id": sys.argv[1],
    })
