#!/bin/bash

poetry run app &
nginx -g "daemon off;"