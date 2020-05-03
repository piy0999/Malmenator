#!/bin/bash

while inotifywait -q -e modify /home/ubuntu/Malmenator/new_model/packets-record.pcap >/dev/null;
do
	sudo /home/ubuntu/CICFlowMeter-4.0/bin/cfm /home/ubuntu/Malmenator/new_model/packets-record.pcap /home/ubuntu/Malmenator/new_model/	
	python /home/ubuntu/Malmenator/new_model/CICFlowmeter_Converter.py
done
