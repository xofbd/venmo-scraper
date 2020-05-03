#!/bin/bash

rsync -avh --stats --delete vagrant@don:~/venmo/daily .
