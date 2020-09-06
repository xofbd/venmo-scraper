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
    long_description=long_description
)
