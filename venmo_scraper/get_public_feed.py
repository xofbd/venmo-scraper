#!/usr/bin/env python3
"""
Note: As of late March, Venmo started putting out fake data to their public web
API. The fake data consists of twenty or so transactions with generic user
names and messages.
"""
import os
import logging

import requests

from venmo_scraper.utils import dump_data

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
                    level=logging.INFO)


def get_data(url):
    """Return JSON of response from GET request of endpoint."""
    r = requests.get(url, headers={'user-agent': 'transactions'})
    data = r.json()['data']

    return data


def main():
    url = 'https://venmo.com/api/v5/public'
    output_dir = os.path.join('data', 'snapshots')
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    data = get_data(url)
    dump_data(data, output_dir)


if __name__ == '__main__':
    main()
