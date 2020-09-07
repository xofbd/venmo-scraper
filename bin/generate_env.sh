#!/bin/bash

function generate {
    echo -n "Enter login: "
    read LOGIN
    echo -n "Enter password: "
    read PASSWORD
    echo -n "Enter path to profile: "
    read PROFILE_PATH
    echo -e "\nIs this correct? (y/n)"

    for response in $LOGIN $PASSWORD $PROFILE_PATH; do
	echo $response
    done

    read CONFIRMATION
    if [[ $CONFIRMATION == "y" ]]; then
	echo "export LOGIN=$LOGIN" > .env
	echo "export PASSWORD=$PASSWORD" >> .env
	echo "export PROFILE_PATH=$PROFILE_PATH" >> .env
	echo "Created .env"
    else
	echo "Existing without creation of .env."
    fi
}

if [[ -e .env ]]; then
    while read -p ".env already exists; do you want to overwrite it? (y/n) " yn; do
	case $yn in
	    [Yy] ) echo -e "Overwriting .env.\n"; generate; exit 0;;
	    [Nn] ) echo "Exiting."; exit 1;;
	    *) echo "Please answer y (yes) or n (no)." && continue;
	esac
    done
else
    generate
fi
