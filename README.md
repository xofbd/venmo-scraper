# Venmo Transaction Data
Venmo is a service that allows people to easily send money to each other. Depending on a person's profile setting, their Venmo transactions are made public. This repo contains code to obtain that public transaction data. This project is purely for academic use.

## Installation

To get started, follow these steps. Unless otherwise noted, all paths are relative to project's root directory, `venmo_scraper`. If you have Make installed, simply

1. Clone this repo.
1. Run `make all`.

If you don't have Make installed, you can follow these steps instead.

1. Clone this repo.
1. Create a virtual environment.
```bash
python3 -m venv venv
```
1. Install project and requirements.
```bash
pip install -r requirements/requirements.txt
pip install -e .
```
Once the application is installed, follow these steps if you wish to use the `scrape_public_feed.py` script (see the Usage section for details).

1. Install Firefox version 60 or above.
1. Download the [Firefox browser driver](https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz), unpack, and move to `venv/bin`. Note, this step is taken care of if you ran `make install`.
1. Create a [Venmo](https://venmo.com) account.
1. Create a file named `.env` in the project's root directory. Use the template below for your `.env` file, filling in your details. You can also run `generate_env` to help generate the file.
```bash
PROFILE_PATH=/path/to/profile
LOGIN=my_email@example.com
PASSWORD=password_1234
```
The `PROFILE_PATH` is the path to your Firefox profile. Providing your profile will prevent Venmo from asking you to enter a verification code every time you run `scrape_public_feed.py`. You will need to at least sign into Venmo once using Firefox to prevent asking for the verification code. The profile path may vary across installations but mine is located in `~/.mozilla/firefox/nh3otjry.default`. You can also specify the optional `DEFAULT_OUTPUT_DIR` which is the default output directory of the JSONs obtained from Venmo.

## Usage

Make sure to activate the virtual environment by running (in the root directory) `source venv/bin/activate`. To obtain public transaction data, you can either run:
* `get_public_feed.py`: makes a GET request to Venmo's public API.
* `scrape_public_feed.py`: logs into your Venmo account and scrapes the public feed.

Note, as of late March 2020, Venmo started putting out fake data to their public web API. The fake data consists of twenty or so transactions with generic user names and messages. You can no longer use `get_public_feed.py` and will have to use `scrape_public_feed.py` if you want to get real Venmo transaction data.

The data will be dumped in `data/snapshots`, by default, as a JSON file. If you want to use a different directory, specify using the `--output_dir` option of `scrape_public_feed.py`. The `consolidate_json.py` script helps you combine JSON files of the same day into one JSON file. The `analysis` directory contains several Python files that helps analyze the transaction data.

If you run `scrape_public_feed.py` too frequently, you might at the very least receive a soft ban where Venmo prevents you from signing in for several hours. Run this script at your own risk but running it several times a day should be fine. If you wish to use cron to automate `scrape_public_feed.py`, using `run_scraper` may be helpful. It is wrapper around `scrape_public_feed.py` that activates the virtual environment and adds a sleep option.

Running `make clean` removes any logs the driver created and the virtual environment. After removing the environment you will need to run `make all` to create the environment, install the application, and download the browser driver.

## Testing

The project uses [`pytest`](https://docs.pytest.org/en/stable/) for testing. You can run the tests easily by running `make tests`. The project uses [pip-tools](https://github.com/jazzband/pip-tools) to manage project requirements for both production and testing.

## License

The project uses the GNU General Public License v3.0. The full license can be found in `LICENSE`.
