import os
from unittest.mock import Mock, patch

import pytest

from venmo_scraper.constants import DEFAULT_OUTPUT_DIR
from venmo_scraper.scrape_public_feed import (scrape_public_feed,
                                              sign_into_venmo,
                                              visit_public_feed)

parameter_str = 'headless, sleep_duration, current_url, bad_url'
test_data = [(True, 2, 'https://venmo.com/?feed=public#public', False),
             (False, 1, 'https://venmo.com/?feed=public#publi', True)]


def create_mock_driver(current_url):
    """Return mock driver object based on provided current URL."""
    driver = Mock()
    driver.current_url = current_url

    return driver


@pytest.mark.parametrize(parameter_str, test_data)
@patch('venmo_scraper.scrape_public_feed.time.sleep')
@patch('venmo_scraper.scrape_public_feed.sign_into_venmo')
def test_visit_public_feed(mock_sign_into_venmo, mock_sleep,
                           headless, sleep_duration, current_url, bad_url):

    mock_driver = create_mock_driver(current_url)
    mock_sign_into_venmo.return_value = mock_driver

    if bad_url:
        with pytest.raises(Exception):
            _ = visit_public_feed(headless, sleep_duration)
    else:
        _ = visit_public_feed(headless)

    mock_sign_into_venmo.assert_called_once_with(headless)
    mock_sleep.assert_called_once_with(sleep_duration)


@patch('venmo_scraper.scrape_public_feed.create_dir')
@patch('venmo_scraper.scrape_public_feed.get_data')
@patch('venmo_scraper.scrape_public_feed.dump_data')
@patch('venmo_scraper.scrape_public_feed.visit_public_feed')
def test_scrape_public_feed(mock_visit_public_feed, mock_dump_data,
                            mock_get_data, mock_create_dir):
    data = {"key": "value"}
    output_dir = os.path.join('test', 'snapshots')
    headless = True
    mock_get_data.return_value = data

    scrape_public_feed(output_dir)

    mock_create_dir.assert_called_once_with(output_dir)
    mock_get_data.assert_called_once_with(mock_visit_public_feed.return_value)
    mock_dump_data.assert_called_once_with(data, output_dir)
    mock_visit_public_feed.assert_called_once_with(headless)
