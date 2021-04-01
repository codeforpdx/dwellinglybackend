#!/bin/bash

if [ ! -f ./data-dev.sqlite3 ]; then
    flask db create
fi
flask run --reload --host=0.0.0.0
