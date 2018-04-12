#!/bin/bash

## A script for installing SRIM on Linux machine

## wine needs to already be installed
# sudo apt install wine-stable

SRIMDIR=/tmp/srim

mkdir -p $SRIMDIR
wget --output-document=$SRIMDIR/SRIM_INSTALL.exe http://www.srim.org/SRIM/SRIM-2013-Std.e
wine $SRIMDIR/SRIM_INSTALL.exe
