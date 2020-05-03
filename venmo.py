#!/opt/conda/envs/data3/bin/python
"""
Note: As of Apri
"""

from datetime import datetime
import json
import os

import requests

from combine_jsons import local_path


def get_data(url):
    r = requests.get(url)
    data = r.json()['data']

    return data


def dump_data(data, output_dir):
    now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    file_name = 'venmo_data' + '_' + now + '.json'
    path_name = os.path.join(output_dir, file_name)
    print("Dumping {}".format(file_name))

    with open(path_name, 'w') as f:
        json.dump(data, f)


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
