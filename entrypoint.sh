#!/bin/bash

poetry run app -l info &
nginx -g "daemon off;"