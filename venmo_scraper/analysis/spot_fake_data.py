"""
This script looks to spot when Venmo started releasing fake data to their
public API.
"""
import glob
import json
import os

from venmo_scraper.utils import load_data


def name_counter(data):
    """Return the number of unique names."""
    names = [x['actor']['firstname'].lower() for x in data]

    return len(set(names))


def spot_fakes(threshold=20):
    """Print out the earliest JSON file suspected to be fake."""
    fake_files = []

    for f in glob.glob(os.path.join('data', 'daily_data', '*.json')):
        data = load_data(f)
        num_names = name_counter(data)

        if num_names < threshold:
            fake_files.append(f)

    fake_files.sort()
    filename = os.path.basename(fake_files[0])

    print(f"Earliest file deemed fake: {filename}")


if __name__ == '__main__':
    spot_fakes()
