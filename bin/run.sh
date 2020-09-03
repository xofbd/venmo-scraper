#!/bin/bash

source venv/bin/activate

if python -m venmo_scraper.scrape_public_feed --sleep; then
    echo "Success!"
else
    echo "An error occurred."
fi
