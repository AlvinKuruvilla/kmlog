#!/bin/bash
# Taken from Amber Jain, https://gist.github.com/amberj/5166112
SELF_NAME=$(basename $0)
# Prints warning/error $MESSAGE in red foreground color
#
# For e.g. You can use the convention of using RED color for [E]rror messages
red_echo() {
echo -e "\x1b[1;31m[E] $SELF_NAME: $MESSAGE"
}
simple_red_echo() {
echo -e "\x1b[1;31m$MESSAGE"
}
# Prints success/info $MESSAGE in green foreground color
#
# For e.g. You can use the convention of using GREEN color for [S]uccess messages
green_echo() {
echo -e "\x1b[1;32m[S] $SELF_NAME: $MESSAGE\e[0m"
}
simple_green_echo() {
echo -e "\x1b[1;32m$MESSAGE"
}
# Prints $MESSAGE in blue foreground color
#
# For e.g. You can use the convetion of using BLUE color for [I]nfo messages
# that require special user attention (especially when script requires input from user to continue)
blue_echo() {
echo -e "\x1b[1;34m[I] $SELF_NAME: $MESSAGE"
}
simple_blue_echo() {
echo -e "\x1b[1;34m$MESSAGE"
}
#########
# Usage #
#########
echo "This is a 'normal' echo!"
echo
MESSAGE="This is a RED colored message!" ; red_echo
MESSAGE="This is a simple RED colored message!" ; simple_red_echo
echo
MESSAGE="This is a GREEN colored message!" ; green_echo
MESSAGE="This is a simple GREEN colored message!" ; simple_green_echo
echo
MESSAGE="This is a BLUE colored message!" ; blue_echo
MESSAGE="This is a simple BLUE colored message!" ; simple_blue_echo
