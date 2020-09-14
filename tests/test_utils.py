from datetime import datetime
import os
from unittest.mock import mock_open, patch

import pytest

from venmo_scraper.utils import create_dir, dump_data, load_data

parameters = [('venmo_data_2020-09-06-22:15:01.json', None),
              ('venmo_data_2020-09-07.json', '2020-09-07')]
dirs = [(os.path.join('data', 'snapshots'), True),
        (os.path.join('new_dir', 'snapshots'), False)]


@pytest.mark.parametrize('file_name, date', parameters)
@patch('venmo_scraper.utils.utils.open', new_callable=mock_open)
@patch('venmo_scraper.utils.utils.datetime')
@patch('venmo_scraper.utils.utils.json.dump')
def test_dump_data(mock_dump, mock_datetime, mock_file, file_name, date):
    data = {"key": "value"}
    mock_file.read_data = data
    mock_datetime.now.return_value = datetime(2020, 9, 6, 22, 15, 1)

    output_dir = os.path.join('tests', 'data', 'snapshots')
    path_name = os.path.join(output_dir, file_name)
    dump_data(data, output_dir, date=date)

    mock_file.assert_called_once_with(path_name, 'w')
    mock_dump.assert_called_once_with(data, mock_file())


@patch('venmo_scraper.utils.utils.open', new_callable=mock_open)
@patch('venmo_scraper.utils.utils.json.load')
def test_load_data(mock_load, mock_file):
    output_dir = os.path.join('tests', 'data', 'snapshots')
    path_name = os.path.join(output_dir, '2020-09-07.json')
    load_data(path_name)

    mock_file.assert_called_once_with(path_name, 'r')
    mock_load.assert_called_once_with(mock_file())


@pytest.mark.parametrize('dir_, exists', dirs)
@patch('venmo_scraper.utils.utils.os.mkdir')
def test_create_dir(mock_mkdir, dir_, exists):
    if exists:
        mock_mkdir.side_efffect = OSError

    create_dir(dir_)
    mock_mkdir.assert_called_once_with(dir_)
