from datetime import datetime
import json
import os

from venmo_scraper import logger


def load_data(path):
    """Return decoded JSON."""
    with open(path, 'r') as f:
        return json.load(f)


def dump_data(data, output_dir):
    """Dump data to disk given target directory."""

    now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    file_name = 'venmo_data' + '_' + now + '.json'
    path_name = os.path.join(output_dir, file_name)
    message = f"Dumping data to {path_name}"
    logger.info(message)

    with open(path_name, 'w') as f:
        json.dump(data, f)
