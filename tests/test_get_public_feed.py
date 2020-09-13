import os
from unittest.mock import patch

from venmo_scraper.get_public_feed import get_data, main


@patch('venmo_scraper.get_public_feed.requests.get')
def test_get_data(mock_get):
    url = 'https://venmo.com/api/v5/public'
    headers = {'user-agent': 'transactions'}
    json_payload = {'data': [{'key': 'value'}]}
    mock_get.return_value.json.return_value = json_payload

    assert get_data(url) == json_payload['data']
    mock_get.assert_called_once_with(url, headers=headers)


@patch('venmo_scraper.get_public_feed.dump_data')
@patch('venmo_scraper.get_public_feed.get_data')
@patch('venmo_scraper.get_public_feed.os.mkdir')
def test_main(mock_mkdir, mock_get_data, mock_dump_data):
    output_dir = os.path.join('data', 'snapshots')
    data = [{'key': 'value'}]
    mock_get_data.return_value = data

    main()
    mock_dump_data.assert_called_once_with(data, output_dir)
    mock_mkdir.assert_called_once_with(output_dir)
