#!/bin/bash

cd ~/pypboy && git stash && git fetch --all && git checkout --force "origin/master" && chmod 777 main.py && chmod 777 scripts/installsdl.sh && chmod 777 scripts/updatepypboy.sh && sudo chmod 777 scripts/installsdl.sh && sudo chmod 777 scripts/updatepypboy.sh
