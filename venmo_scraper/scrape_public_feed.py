#!/usr/bin/env python
import os
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import FirefoxProfile

from venmo_scraper import logger
from venmo_scraper.constants import DEFAULT_OUTPUT_DIR, URL_PUBLIC_FEED
from venmo_scraper.utils import create_dir, dump_data

# Load secrets
load_dotenv()
PROFILE_PATH = os.getenv('PROFILE_PATH')
LOGIN = os.getenv('LOGIN')
PASSWORD = os.getenv('PASSWORD')
DEFAULT_OUTPUT_DIR = os.getenv('OUTPUT_DIR', DEFAULT_OUTPUT_DIR)


def visit_public_feed(headless, sleep_duration=2):
    """Return web driver on the public feed page."""
    driver = sign_into_venmo(headless)
    time.sleep(sleep_duration)
    driver.get(URL_PUBLIC_FEED)

    if driver.current_url != 'https://venmo.com/?feed=public#public':
        message = ('Could not sign into Venmo. '
                   f'The current URL of the driver is {driver.current_url}')
        logger.error(message)
        raise Exception

    return driver


def sign_into_venmo(headless):
    """Return web driver signed into Venmo."""

    # Create browser driver. Note, needs to be headless to run via CLI.
    # The profile is needed because Venmo will need to recognize your device to
    # avoid two-factor authentication.
    profile = FirefoxProfile(PROFILE_PATH)
    options = Options()
    options.headless = headless  # needed to run via CLI
    driver = webdriver.Firefox(profile, options=options)

    # Fill in login credentials.
    driver.get('https://venmo.com/account/sign-in')
    inputs = driver.find_elements_by_css_selector('input.auth-form-input')
    button = driver.find_element_by_css_selector('button.ladda-button')

    inputs[0].send_keys(LOGIN)
    inputs[1].send_keys(PASSWORD)
    button.click()

    return driver


def get_data(driver):
    """Return list of parsed Venmo transactions."""
    data = []

    for story in get_stories(driver):
        try:
            data.append(parse_story(story))
        except NoSuchElementException:
            logger.warning('Could not parse story.', exc_info=True)

    return data


def get_stories(driver):
    """Return list of stories/transactions elements from public feed."""
    return driver.find_elements_by_css_selector('div.feed-story-payment')


def parse_story(element):
    """Return scraped data from Venmo's public feed as dictionary."""

    # Define CSS selectors to use
    username_sender_slctr = 'p.feed-description__notes__headline a'
    name_sender_slctr = 'p.feed-description__notes__headline a > strong'
    username_receiver_slctr = 'p.feed-description__notes__headline span a'
    name_receiver_slctr = 'p.feed-description__notes__headline span a > strong'
    date_slctr = 'span.feed-description__notes__meta > span'
    message_slctr = 'div.feed-description__notes__content > p'

    image = (element
             .find_element_by_css_selector('img')
             .get_property('src'))
    username_sender = (element
                       .find_element_by_css_selector(username_sender_slctr)
                       .get_property('href')
                       .split('/')[-1])
    name_sender = (element
                   .find_element_by_css_selector(name_sender_slctr)
                   .text)
    username_receiver = (element
                         .find_element_by_css_selector(username_receiver_slctr)
                         .get_property('href')
                         .split('/')[-1])
    name_receiver = (element
                     .find_element_by_css_selector(name_receiver_slctr)
                     .text)
    date = (element
            .find_element_by_css_selector(date_slctr)
            .text)
    message = (element
               .find_element_by_css_selector(message_slctr)
               .text)

    return {
        'image': image,
        'sender': {'name': name_sender, 'username': username_sender},
        'receiver': {'name': name_receiver, 'username': username_receiver},
        'date': date,
        'message': message
    }


def scrape_public_feed(output_dir, headless=True):
    """Scrape Venmo public feed data and dump to disk."""
    create_dir(output_dir)
    driver = visit_public_feed(headless)
    data = get_data(driver)
    dump_data(data, output_dir)
    driver.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Scrape Venmo's public feed")
    parser.add_argument('-d', '--headless',
                        default=False,
                        action='store_true',
                        help="use the browser's GUI")
    parser.add_argument('-o', '--output_dir',
                        default=DEFAULT_OUTPUT_DIR,
                        action='store',
                        help="specify Venmo data output directory")
    args = parser.parse_args()

    logger.info("Running scraper")
    scrape_public_feed(args.output_dir, headless=args.headless)
