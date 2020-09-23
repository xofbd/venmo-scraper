# Venmo Transaction Data

Venmo is a service that allows people to easily send money to each other. Depending on a person's profile setting, their Venmo transactions are made public. This repo contains code to obtain that public transaction data. This project is purely for academic use.

## Installation

To get started, follow these steps. Note, unless otherwise noted, all paths are relative to project's root directory, `venmo_scraper`.

1. Clone this repo.
1. Create a virtual environment. The project requires `selenium`, `requests`, and `dotenv` Python packages. A `requirements.txt` file is provided and a virtual environment can be created by running:
```bash
make venv
```
1. The following steps are required if you wish to run `scrape_public_feed.py`. You will need to install Firefox, at least version 60 or above. Once you have the appropriate Firefox version installed, run
```bash
make driver
```
to install the appropriate browser driver. Note, running `make all` takes care of this and the previous step.
1. You need to create a Venmo account and create a file named `.env` in the project's root directory. Use the below template for your `.env` file, filling in your details. You can also run `generate_env` to help generate the file.
```bash
PROFILE_PATH=/path/to/profile
LOGIN=my_email@example.com
PASSWORD=password_1234
```
The `PROFILE_PATH` is the path to your Firefox profile. Providing your profile will prevent Venmo from asking you to enter a verification code every time you run `scrape_public_feed.py`. You will need to at least sign into Venmo once using Firefox to prevent asking for the verification code. The profile path may vary across installations but mine is located in `~/.mozilla/firefox/nh3otjry.default`. You can also specify the optional `DEFAULT_OUTPUT_DIR` which is the default output directory of the JSONs obtained from Venmo.

## Usage

Make sure to activate the virtual environment by running (in the root directory) `source venv/bin/activate`. To obtain public transaction data,  you can either run:
* `get_public_feed.py`: makes a GET request to Venmo's public API.
* `scrape_public_feed.py`: logs into your Venmo account and scrapes the public feed.

Note, as of late March, Venmo started putting out fake data to their public web API. The fake data consists of twenty or so transactions with generic user names and messages. You can no longer use `get_public_feed.py` and will have to use `scrape_public_feed.py` if you want to get real Venmo transaction data.

The data will be dumped in `data/snapshots`, by default, as a JSON file. If you want to use a different directory, specify using the `--output_dir` option of `scrape_public_feed.py`. The `consolidate_json.py` script helps you combine JSON files of the same day into one JSON file. The `analysis` directory contains several Python files that helps analyze the transaction data.

If you run `scrape_public_feed.py` too frequently, you might at the very least receive a soft ban where Venmo prevents you from signing in for several hours. Run this script at your own risk but running it several times a day should be fine. If you wish to use cron to automate `scrape_public_feed.py`, using `run_scraper` may be helpful. It is wrapper around `scrape_public_feed.py` that activates the virtual environment and adds a sleep option.

Running `make clean` removes any logs the driver may have generated and `make remove_venv` deletes the virtual environment. After removing the environment you will need to run `make all` to create the environment and download the browser driver.

## License

The project uses the GNU General Public License v3.0. The full license can be found in `LICENSE`.
