#!/bin/bash

poetry run python -m backend_api  &
nginx -g "daemon off;"