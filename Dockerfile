FROM debian:stretch
MAINTAINER Chris Ostrouchov <chris.ostrouchov@gmail.com>

ARG SRIM_DIR="/tmp/srim"

RUN dpkg --add-architecture i386

RUN apt update && \
    apt install wget xvfb wine32 -y && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir -p $SRIMDIR
wget --output-document=$SRIMDIR/SRIM_INSTALL.exe http://www.srim.org/SRIM/SRIM-2013-Std.e
wine $SRIMDIR/SRIM_INSTALL.exe
