#!/usr/bin/env python3
from datetime import datetime
import glob
import json
import os
import re

from venmo_scraper.utils import dump_data


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
        os.mkdir(os.path.join('data', 'daily_data'))
    except OSError:
        pass

    output_dir = os.path.join('data', 'daily_data')
    dump_data(data_all, output_dir)

    # Delete snapshot files
    for f in files_of_date:
        os.remove(f)


def main():
    files = glob.glob(os.path.join('data', 'snapshots', '*.json'))
    unique_dates = get_unique_dates(files)

    for date in unique_dates:
        combine_jsons(files, date)


if __name__ == '__main__':
    main()
