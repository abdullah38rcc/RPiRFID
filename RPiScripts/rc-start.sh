#!/bin/sh
#
#root@raspberrypi:~/RPiRFID# cat /usr/local/bin/rc-start.sh 
#
# rc-start.sh	1.00	2013-02-04	S. Kittelson
#
# Script used upon system startup.

#
# Create a temp dir in the /dev space as it is 
# using a mem filesystem.
#
echo `date` > /tmp/rc-start.log
echo `pwd` >> /tmp/rc-start.log
echo  >> /tmp/rc-start.log

mkdir -p /dev/tmp
chmod 777 /dev/tmp

#
# Run the python app and restart it if it dies.
#
cd /root/RPiRFID

while true
do
  
  echo `date` >> /tmp/rc-start.log
  echo "Starting python app with logging to /dev/tmp/ATS.log"  \
    >> /tmp/rc-start.log
  ./ATS_Machine_Control.py > /dev/tmp/ATS.log 2>&1
  es=$?
  echo "python app exited with status $es - restarting in 5 seconds" \
    >> /tmp/rc-start.log
  sleep 5

done



