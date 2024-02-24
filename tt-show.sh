#!/bin/bash
PRJFOLDER=/Users/charleslobo/Desktop/chaRcoal/me/tt
cd $PRJFOLDER

if [ -z "$1" ]
then
	./tt.py show | less
	./tt.py edit
else
	./tt.py "$@"
fi
