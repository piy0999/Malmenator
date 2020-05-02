#!/bin/bash

while inotifywait -q -e modify /home/ubuntu/Malmenator/new_model/packets-record.pcap >/dev/null;
do
	python /home/ubuntu/Malmenator/new_model/CICFlowmeter_Converter.py
done
