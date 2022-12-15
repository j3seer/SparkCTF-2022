#!/usr/bin/env bash

socat tcp-l:7894,reuseaddr,fork EXEC:/home/ctf/margot
