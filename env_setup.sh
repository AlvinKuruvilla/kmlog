#!/bin/bash
items=(
"Creating your virtual environment (if it doesn't exist already)"
"Installing dependencies"
"Providing instructions on next stpes"
)
final_items=("Run the keylogger TUI using kmlog.py" "Run the headless keylogger using kmlog_headless.py and use one of the data collection pages in fake_pages/")
RED='\033[0;31m'
COLOR_RESET='\033[0m' # No Color
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
virtual_env_file="pyvenv.cfg"


echo "This script is responsible for setting up your environment to make using kmlog's tools easier!"
echo "This script handles:"
for i in "${!items[@]}"; do
    # Format the number to always be two digits (e.g., 01, 02, etc.)
    printf "    %02d. %s\n" "$((i + 1))" "${items[$i]}"
done
echo -e "${YELLOW}Note: this script won't build the kmlog executable see ${COLOR_RESET}${GREEN}build.sh${COLOR_RESET} ${YELLOW}for that! ${COLOR_RESET}"

# Search for the pyenv.cfg in the current directory and subdirectories

if find . -type f -name "$virtual_env_file" -print -quit | grep -q .; then
    # If the file is found, print a success message
    echo -e "\033[32mSuccess! '$virtual_env_file' found!\033[0m"  # Green text for success
else
    # If the file is not found, print a failure message
    echo -e "\033[31mFailure! '$virtual_env_file' not found.\033[0m"  # Red text for failure
    echo "Creating virtual environment: env"
    python3 -m venv env
fi
echo "Installing dependencies"
source env/bin/activate
pip3 install -r requirements.txt

echo -e "${GREEN}Dependencies installed! ${COLOR_RESET}"

echo "Now you can:"
for i in "${!final_items[@]}"; do
    printf "    %02d. %s\n" "$((i + 1))" "${final_items[$i]}"
done
