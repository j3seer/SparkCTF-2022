#!/usr/bin/env bash

socat tcp-l:1337,reuseaddr,fork EXEC:/home/ctf/f-xit
