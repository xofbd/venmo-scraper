from distutils.core import setup

from venmo_scraper import __version__

with open('README.md') as f:
    long_description = f.read()

setup(
    name='venmo_scraper',
    version=__version__,
    packages=['venmo_scraper'],
    license='GNU GPL',
    description='Venmo scraper',
    long_description=long_description,
    author='Don B. Fox',
    url='https://github.com/xofbd/venmo_scraper',
    download_url='https://github.com/xofbd/venmo_scraper',
    scripts=[
        'bin/run_scraper',
        'venmo_scraper/scrape_public_feed.py',
        'venmo_scraper/get_public_feed.py'
    ]
)
