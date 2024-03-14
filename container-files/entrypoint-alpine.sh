#!/bin/sh
set -e
/usr/sbin/sshd
exec python3 -u /home/server.py
