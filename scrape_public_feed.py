#!/usr/bin/env python

import json
import os
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.webdriver import FirefoxProfile

from utils import dump_data, local_path


def visit_public_feed(secrets, sleep_duration=2):
    """Return web driver on the public feed page."""
    driver = sign_into_venmo(secrets)
    time.sleep(sleep_duration)

    driver.get('https://venmo.com/?feed=public')

    return driver


def sign_into_venmo(secrets):
    """Return web driver signed into Venmo."""
    profile = FirefoxProfile('/home/dbf/.mozilla/firefox/nh3otjry.default')
    driver = webdriver.Firefox(profile)
    driver.get('https://venmo.com/account/sign-in')

    # Fill in login credentials
    inputs = driver.find_elements_by_css_selector('input.auth-form-input')
    button = driver.find_element_by_css_selector('button.ladda-button')

    inputs[0].send_keys(secrets['username'])
    inputs[1].send_keys(secrets['password'])
    button.click()

    return driver


def get_data(driver):
    """Return list of parsed Venmo transactions."""
    data = []

    for story in get_stories(driver):
        try:
            data.append(parse_story(story))
        except NoSuchElementException:
            pass

    return data


def get_stories(driver):
    """Return list of stories/transactions elements from public feed."""
    return driver.find_elements_by_css_selector('div.feed-story-payment')


def parse_story(element):
    """Return scraped data from Venmo's public feed."""

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


def scrape_public_feed():
    output_dir = local_path('data')
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    with open('secrets/secrets.json', 'r') as f:
        secrets = json.load(f)

    driver = visit_public_feed(secrets)
    data = get_data(driver)
    dump_data(data, output_dir)
    driver.close()


if __name__ == '__main__':
    import random

    # Randomly sleep to mimic human behavior
    scale = 60
    wait = scale * random.random()
    time.sleep(wait)

    scrape_public_feed()
