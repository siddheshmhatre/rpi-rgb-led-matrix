#!/bin/bash
cd /home/pi/ngrok
./ngrok tcp --region=in --remote-addr=remote_addr --config=/home/pi/.ngrok2/ngrok.yml 22
