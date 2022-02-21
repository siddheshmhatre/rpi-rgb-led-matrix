#!/bin/bash
cd /home/pi/ngrok
./ngrok http -subdomain=subdmn --log=stdout --config=/home/pi/.ngrok2/ngrok.yml 3000
