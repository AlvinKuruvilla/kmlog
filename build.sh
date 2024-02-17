#!/bin/bash

echo "Creating spec file..."
pyi-makespec src/kmlog.py

echo "Building executable..."
pyinstaller --clean kmlog.spec
