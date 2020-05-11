from datetime import datetime
import json
import os


def dump_data(data, output_dir):
    now = datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
    file_name = 'venmo_data' + '_' + now + '.json'
    path_name = os.path.join(output_dir, file_name)
    print("Dumping {}".format(file_name))

    with open(path_name, 'w') as f:
        json.dump(data, f)


def local_path(path):
    """Return path relative to local file."""
    return os.path.join(os.path.dirname(__file__), path)
