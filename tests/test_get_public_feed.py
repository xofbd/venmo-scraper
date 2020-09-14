from unittest.mock import patch

from venmo_scraper.constants import DEFAULT_OUTPUT_DIR, URL_API
from venmo_scraper.get_public_feed import get_data, get_public_feed


@patch('venmo_scraper.get_public_feed.requests.get')
def test_get_data(mock_get):
    headers = {'user-agent': 'transactions'}
    json_payload = {'data': [{'key': 'value'}]}
    mock_get.return_value.json.return_value = json_payload

    assert get_data() == json_payload['data']
    mock_get.assert_called_once_with(URL_API, headers=headers)


@patch('venmo_scraper.get_public_feed.create_dir')
@patch('venmo_scraper.get_public_feed.dump_data')
@patch('venmo_scraper.get_public_feed.get_data')
def test_get_public_feed(mock_get_data, mock_dump_data, mock_create_dir):
    data = [{'key': 'value'}]
    mock_get_data.return_value = data

    get_public_feed(DEFAULT_OUTPUT_DIR)
    mock_create_dir.assert_called_once_with(DEFAULT_OUTPUT_DIR)
    mock_dump_data.assert_called_once_with(data, DEFAULT_OUTPUT_DIR)
