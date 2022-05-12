#!/bin/bash
# Print file names from a directory
for f in *
do
  echo "The base file name: ${f%\.*}"
done