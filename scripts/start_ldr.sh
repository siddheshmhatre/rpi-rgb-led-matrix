#!/bin/bash
cd /home/pi/rpi-rgb-led-matrix/bindings/python/samples
sudo SLACK_BOT_TOKEN=slack_bot_token SLACK_SIGNING_SECRET=slack_signin_secret python3 slack_notifications_run_text.py
