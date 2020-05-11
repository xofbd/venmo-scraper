#!/opt/conda/envs/data3/bin/python
"""
Note: As of Apri
"""

from datetime import datetime
import json
import os

import requests

from utils import dump_data, local_path


def get_data(url):
    """Return JSON of response from GET request of endpoint."""
    r = requests.get(url)
    data = r.json()['data']

    return data


def main():
    url = 'https://venmo.com/api/v5/public'
    output_dir = local_path('data')
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    data = get_data(url)
    dump_data(data, output_dir)


if __name__ == '__main__':
    main()
