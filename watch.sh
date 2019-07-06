#!/usr/bin/env bash

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

inotifywait -qrme close_write --format '%w%f' ./paycalc ./tests | \
while read file ; do
  if [ -z "$file" ] ; then
    continue
  fi

  # we have a filename

  if [ -z "${file##*.py}" ] ; then
    # gives a nice visual marker
    echo -e "${GREEN}--------------------- STARTING TEST RUN ----------------------${NC}"
    nosetests
  fi

done
