#!/usr/bin/env python3

from datetime import datetime
import glob
import json
import os
import re

from utils import local_path


def get_unique_dates(files):
    """Return a set of all unique dates from all JSON files."""
    current_date = datetime.now().strftime('%Y-%m-%d')
    past_files = [f for f in files if current_date not in f]

    re_date = re.compile(r'(\d{4}-\d{2}-\d{2})')
    unique_dates = {re_date.search(f).group(1) for f in past_files}

    return unique_dates


def combine_jsons(files, date):
    """Create JSON file from all JSONs of the same date."""

    # Load up all JSONs of the same date into one Python list
    data_all = []
    files_of_date = [f for f in files if date in f]

    for f in files_of_date:
        with open(f, 'r') as f:
            data_all.extend(json.load(f))

    # Dump collected JSON to disk
    try:
        os.mkdir(local_path('daily'))
    except OSError:
        pass

    file_name = 'venmo_data' + '_' + date + '.json'
    path_name = os.path.join(local_path('daily'), file_name)
    print("Dumping data to {}".format(path_name))

    with open(path_name, 'w') as f:
        json.dump(data_all, f)

    # Delete snapshot files
    for f in files_of_date:
        os.remove(f)


def main():
    files = glob.glob(local_path(os.path.join('data', '*.json')))
    unique_dates = get_unique_dates(files)

    for date in unique_dates:
        combine_jsons(files, date)


if __name__ == '__main__':
    main()
