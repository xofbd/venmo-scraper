import json
import os
from unittest.mock import call, patch

from venmo_scraper.utils.consolidate_data import (combine_jsons,
                                                  get_unique_dates)


@patch('venmo_scraper.utils.consolidate_data.datetime')
def test_get_unique_dates(mock_datetime):
    mock_datetime.now().strftime.return_value = '2020-09-01'

    dates = ['2020-01-01', '2020-01-02', '2020-09-01']
    files = ['venmo_data_' + d + '.json' for d in dates]
    unique_dates = {'2020-01-02', '2020-01-01'}

    assert unique_dates == get_unique_dates(files)


@patch('venmo_scraper.utils.consolidate_data.dump_data')
@patch('venmo_scraper.utils.consolidate_data.create_dir')
@patch('venmo_scraper.utils.consolidate_data.os.remove')
def test_combine_jsons(mock_remove, mock_create_dir, mock_dump_data):
    date = '2020-09-03'
    output_dir = os.path.join('tests', 'data', 'daily_data')
    data_dir = os.path.join('tests', 'data', 'snapshots')

    # Setting up files to be processed
    file_names = ['venmo_data_2020-09-03-17:32:18.json',
                  'venmo_data_2020-09-03-16:07:06.json',
                  'venmo_data_2020-09-03-15:49:25.json',
                  'venmo_data_2020-09-04-12:19:12.json',
                  'venmo_data_2020-09-04-15:49:16.json',
                  'venmo_data_2020-09-04-10:06:25.json']
    path_names = [os.path.join(data_dir, f) for f in file_names]
    calls = [call(p) for p in path_names[:3]]

    # Testing correct calls of utility/mocked functions
    combine_jsons(path_names, output_dir, date)
    mock_remove.assert_has_calls(calls, any_order=False)
    assert mock_remove.call_count == 3
    mock_create_dir.assert_called_once_with(output_dir)

    # Testing output is same as expected
    path_true = os.path.join(output_dir, f'venmo_data_{date}_TRUE.json')

    with open(path_true, 'r') as f:
        data_true = json.load(f)

    mock_dump_data.assert_called_once_with(data_true, output_dir, date=date)
