#!/bin/bash
cd "$(dirname "$0")"
git pull
python3 rps_gui.py