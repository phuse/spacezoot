#!/bin/bash
mosquitto_pub -h localhost -m "connct" -t "helmet/netwrk"
ip=`ifconfig wlan0 |grep "inet"|grep -v inet6| awk '{print $2}'`
mosquitto_pub -h localhost -m $ip -t "helmet/IP"
su -c "cd /home/pi/spacezoot;git pull" pi
mosquitto_pub -h localhost -m $ip -t "helmet/IP"
