#!/bin/bash

echo "Building executable..."
pyinstaller -F --clean --onefile kmlog.spec                                                              