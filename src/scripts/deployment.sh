#!/bin/bash

## Installation - CentOS
wget https://dl.influxdata.com/telegraf/releases/telegraf-0.13.1.x86_64.rpm && yum localinstall telegraf-0.13.1.x86_64.rpm
wget https://dl.influxdata.com/influxdb/releases/influxdb-0.13.0.x86_64.rpm && yum localinstall influxdb-0.13.0.x86_64.rpm

# Clone: make sure you have deploy key
cd /usr/local/src
git clone git@github.com:Jamesits/hz-traffic-analysis.git

# Install Python 3 dependencies
pip3 install -r hz-traffic-analysis/src/crawler/requirements.txt

# Configuration: assume /dev/sdb mounted on /data
systemctl stop telegraf
systemctl stop influxdb
rm -r /var/lib/influxdb
mkdir -p /data/influxdb
ln -s /var/lib/influxdb /data/influxdb
rm /etc/telegraf/telegraf.conf
ln -s /usr/local/src/hz-traffic/hz-traffic-analysis/src/config/influx/telegraf.conf /etc/telegraf/telegraf.conf
systemctl start influxdb
systemctl start telegraf

# Add InfluxDB user: make sure you have admin set
influx -database=telegraf -execute "CREATE USER telegraf WITH PASSWORD '8ufnGvYkc8bvqH'; GRANT READ ON telegraf TO telegraf;"
