#!/usr/bin/env bash

socat tcp-l:6542,reuseaddr,fork EXEC:/home/ctf/x-bof
