#!/bin/bash

while true
do
   sudo tcpdump -i eth0 -v -w packets-record.pcap -c 100
   scp -i DLAMI.pem packets-record.pcap ubuntu@ec2-18-206-94-40.compute-1.amazonaws.com:/home/ubuntu/Malmenator/new_model
done
