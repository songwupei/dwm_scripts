#!/bin/bash
read -p "Input file name: " FILENAME
if [ -c "$FILENAME" ] ;then
		cp $FILENAME /dev
fi
