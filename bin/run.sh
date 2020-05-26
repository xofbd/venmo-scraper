#!/bin/bash

source venv/bin/activate

if venmo/scrape_public_feed.py --sleep; then
    echo "Success!"
else
    echo "An error occurred."
fi
