#!/bin/bash
mosquitto_pub -h localhost -m "connct" -t "helmet/netwrk"
ip=`ifconfig wlan0 |grep "inet"|grep -v inet6| awk '{print $2}'`
mosquitto_pub -h localhost -m $ip -t "helmet/IP"
su -c "cd /home/pi/spacezoot;git pull" pi
#mosquitto_pub -h localhost -m $ip -t "helmet/IP"
aptitude install sshpass
user=$(/bin/hostname|awk '{ print tolower($0) }')
SSHPASS=`grep spacesuit -A 1 /etc/wpa_supplicant/wpa_supplicant.conf|tail -1 |awk -F\" '{ print $2}'`
sshpass -e ssh -l $user -R 42523:localhost:22 lab.tinkering.ninja
