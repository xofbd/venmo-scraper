"""
This script looks to spot when Venmo started releasing fake data to their
public API.
"""
import glob
import json


def load_data(path):
    """Return decoded JSON."""
    with open(path, 'r') as f:
        return json.load(f)


def name_counter(data):
    """Return the number of unique names."""
    names = [x['actor']['firstname'].lower() for x in data]

    return len(set(names))


def spot_fakes(threshold=20):
    fake_files = []

    for f in glob.glob('../data/daily_data/*.json'):
        data = load_data(f)
        num_names = name_counter(data)

        if num_names < threshold:
            fake_files.append(f)

    fake_files.sort()

    print(f"Earliest file deemed fake: {fake_files[0]}")


if __name__ == '__main__':
    spot_fakes()
