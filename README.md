# Malmenator
Network Based Intelligent Malware Detection

## System setup manual
1. On the raspberry pi install september 2019 release of raspbian OS. This was done following the guidance from https://www.raspberrypi.org/documentation/installation/installing-images/

2. Then tcpdump tools were setup on the Pi using `sudo apt-get install -y tcpdump`

3. Some dependencies were installed before installing snort by `sudo apt install -y gcc libpcre3-dev zlib1g-dev libluajit-5.1-dev libpcap-dev openssl libssl-dev libnghttp2-dev libdumbnet-dev bison flex libdnet`

4. Then Snort IDS was installed following the snort official website by 
```
wget https://www.snort.org/downloads/snort/daq-2.0.6.tar.gz

wget https://www.snort.org/downloads/snort/snort-2.9.9.0.tar.gz
 
 tar xvzf daq-2.0.6.tar.gz
 
 cd daq-2.0.6
 
 sudo ./configure && make && sudo make install
 
 tar xvzf snort-2.9.9.0.tar.gz    
 
 cd snort-2.9.9.0

 sudo ./configure --enable-sourcefire && make && sudo make install
 ```
 
 5. Snort was configured to work with registered user rules as a NIDS which were obtained after getting the oinkcode on registration with the Snort website. The configuration was done using the following changes in the snort.conf file in /etc/snort/ directory. 
```
wget https://www.snort.org/rules/snortrules-snapshot-29120.tar.gz?oinkcode=oinkcode -O ~/registered.tar.gz 

sudo tar -xvf ~/registered.tar.gz -C /etc/snort

sudo nano /etc/snort/snort.conf
```
Make sure that the configuration files have the rule specified correctly as follows

```
# Path to your rules files (this can be a relative path)
var RULE_PATH /etc/snort/rules
var SO_RULE_PATH /etc/snort/so_rules
var PREPROC_RULE_PATH /etc/snort/preproc_rules
# Set the absolute path appropriately
var WHITE_LIST_PATH /etc/snort/rules
var BLACK_LIST_PATH /etc/snort/rules
```
Check if Snort is functioning by running ` Snort -V ` , the output should return as follows on the command line. 

```
   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.9.0 GRE (Build 56) 
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014-2016 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.8.1
           Using PCRE version: 8.39 2016-06-14
           Using ZLIB version: 1.2.11
```
Run snort by using the command `sudo snort -dev -l /var/log/snort -A full -c /etc/snort/etc/snort.conf`
To run snort as a daemon in background we need to create a file for starting it up as
`sudo nano /lib/systemd/system/snort.service`
Add the following contents into this file
```
[Unit]
Description=Snort NIDS Daemon
After=syslog.target network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/snort -dev -l /var/log/snort -A full -c /etc/snort/etc/snort.conf

[Install]
WantedBy=multi-user.target
```
Save the files and then run the following commands
```
sudo systemctl daemon-reload
sudo systemctl start snort
```
This will initiate Snort in background.

Now add screen interface to the Rasberry Pi by running `sudo apt-get install -y screen` this will help run the shell automation script in background

Now go Malmenator/shell_automation and run the following 
```
screen
./transfer_to_ec2.sh
ctrl+A+D
```
This will run the script to export network packet data from Raspberry Pi to AWS EC2 in background

On the AWS EC2, CICFlowmeter was installed by following the instructions on the github repository from canadian institute for cybersecurity at https://github.com/ahlashkari/CICFlowMeter

After installing CICFlowmeter successfully on the AWS server, in the Malmenator/shell_automation folder type the following
```
screen
./predicted_to_es.sh
ctrl+A+D
```
This script gets the data coming from the Pi, processes it by using CICFlowmeter and then feeds the processed data to the network anomaly detection model, receives the predictions from the model and sends the predictions along with this processed data to elasticsearch on AWS. 

For more details on using AWS for elasticsearch service and elastic compute virtual machine service please refer to
https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/what-is-amazon-elasticsearch-service.html
and 
https://docs.aws.amazon.com/ec2/index.html

For this setup we used AWS elasticsearch service with a single data node (50 GB) and open permissions without a VPC subnet.
The Ec2 service used was a deep learning AMI virutal machine ideal for training the network anomaly detection model along with most libraries like Tensorflow, pandas and anaconda pre-installed. More details can be found at https://docs.aws.amazon.com/dlami/latest/devguide/what-is-dlami.html

### Note
**For the python notebooks relevant to the anomaly detection portion of the report, please look at the `new_model` folder, as the `old_models` is obsolete and only used in the early experimental stages of our project**
