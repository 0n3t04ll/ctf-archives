#!/bin/bash

cd ctfs/$(`dirname $0`/initctf.py "$@")

git --no-pager diff
