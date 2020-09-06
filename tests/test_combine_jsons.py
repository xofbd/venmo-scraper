import json
import os
from unittest.mock import call, Mock, patch

from venmo_scraper.utils.consolidate_data import get_unique_dates, combine_jsons


@patch('venmo_scraper.utils.consolidate_data.datetime')
def test_get_unique_dates(mock_datetime):
    mock_datetime.now().strftime.return_value = '2020-09-01'

    dates = ['2020-01-01', '2020-01-02', '2020-09-01']
    files = ['venmo_data_' + d + '.json' for d in dates]
    unique_dates = {'2020-01-02', '2020-01-01'}

    assert unique_dates == get_unique_dates(files)


@patch('venmo_scraper.utils.consolidate_data.os.mkdir')
def test_combine_jsons(mock_mkdir):
    date = '2020-09-03'
    file_names = ['venmo_data_2020-09-03-17:32:18.json',
                  'venmo_data_2020-09-03-16:07:06.json',
                  'venmo_data_2020-09-03-15:49:25.json',
                  'venmo_data_2020-09-04-12:19:12.json',
                  'venmo_data_2020-09-04-15:49:16.json',
                  'venmo_data_2020-09-04-10:06:25.json']
    path_names = [os.path.join('tests', 'data', 'snapshots', f)
                  for f in file_names]
    calls = [call(p) for p in path_names[:3]]
    path_target = os.path.join('tests', 'data', 'daily_data',
                               f'venmo_data_{date}.json')
    with patch('venmo_scraper.utils.consolidate_data.os.path.join') as mock_join:
        mock_join.return_value = path_target
        with patch('venmo_scraper.utils.consolidate_data.os.remove') as mock_remove:
            combine_jsons(path_names, date)

    mock_remove.assert_has_calls(calls, any_order=False)
    assert mock_remove.call_count == 3

    # Testing output is same as expected
    path_output = os.path.join('tests', 'data', 'daily_data',
                               f'venmo_data_{date}.json')
    path_true = os.path.join('tests', 'data', 'daily_data',
                             f'venmo_data_{date}_TRUE.json')
    with open(path_output, 'r') as f:
        data_output = json.load(f)
    with open(path_true, 'r') as f:
        data_true = json.load(f)

    assert data_output == data_true
    os.remove(path_output)
