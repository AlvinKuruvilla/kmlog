#!/bin/bash

echo "Cleaning build directories..."
rm -r dist/ > /dev/null 2>&1
rm -r build/ > /dev/null 2>&1
if [ $? -ne 0 ]
then
    echo "Nothing to clean..."
else
    echo "An error occurred while cleaning"
fi
