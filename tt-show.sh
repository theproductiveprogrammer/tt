#!/bin/bash
PRJFOLDER=/Users/charleslobo/Desktop/chaRcoal/me/tt
cd $PRJFOLDER

source venv/bin/activate

if [ -z "$1" ]
then
	./tt.py show | less -K && ./tt.py edit
else
	./tt.py "$@"
fi
