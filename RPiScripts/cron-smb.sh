#!/bin/sh
#
#root@raspberrypi:~/RPiRFID# cat /usr/local/bin/cron-smb.sh
#
# cron-smb.sh	1.00	2013-02-04	S. Kittelson
#
# Script driven by cron to get a file from a Samba server and
# post process the file for use by an nfc app.
#
# All variable names are in CAPS for ease of ident.  See:
#   RAMFSSIZE
#   RAMFSDEV
#   RAMFSNAME
#   LOGFNAME
#   SMBUSER
#   SMBPASS
#   SMBWORKGROUP
#   SMBSRCFILE
#   SRCFILE
#   CMPFILE
#   DSTPATH
#   DSTFILE
#

#
# This simple function is used for debugging. Uncomment the
# "echo" command inside it to see output.  Otherwise this
# script is mostly self logging.  You could change the echo
# to a logger command to use syslog (or another system syslog).
#
elog(){
# echo "$1"
:
}

#
# This is a file logger which always appends.
# It is only useful if the log file can be created.
#
flog(){
  echo "$1" >> $LOGFNAME
}

#
# To save wear and tear on the SD card we do nearly all of the
# work in a ramdisk filesystem.  Change the RAMFS SIZE param
# below to adjust size of the ramdisk fs. Change the DEV and
# NAME params if needed.
#
RAMFSSIZE='1024'
RAMFSDEV='/dev/ram1'
RAMFSNAME='/ramfs1'
LOGFNAME="$RAMFSNAME/cron-smb.log"

#
# These are the params needed to use/get from SMB.
#
SMBUSER='amosk'
SMBPASS='LOok56%^'
SMBWORKGROUP='workgroup'
SMBSRCFILE='smb://SatM45.local/sambashared/dlserials.txt'

#
# These params specify the location and name of the
# ultimate destination.
#
DSTPATH="/root/RPiRFID"
DSTFILE="dlserials.txt"
DSTPATHFILE=$DSTPATH/$DSTFILE

#
# These params are internals.
#
SRCFILE="$RAMFSNAME/dlserials.src"
CMPFILE="$RAMFSNAME/dlserials.prv"

#
# We've got all we need.  Get going.
#

#
# Tell logger where this is coming from and the params.
#
elog "$0"
elog "RAMFSSIZE=$RAMFSSIZE"
elog "RAMFSDEV=$RAMFSDEV"
elog "RAMFSNAME=$RAMFSNAME"
elog "LOGFNAME=$LOGFNAME"
elog "SMBUSER=$SMBUSER"
elog "SMBPASS=$SMBPASS"
elog "SMBWORKGROUP=$SMBWORKGROUP"
elog "SMBSRCFILE=$SMBSRCFILE"
elog "SRCFILE=$SRCFILE"
elog "CMPFILE=$CMPFILE"
elog "DSTPATH=$DSTPATH"
elog "DSTFILE=$DSTFILE"
elog "DSTPATHFILE=$DSTPATHFILE"

#
# Check for the ramdisk fs and create it if needed.  Seed it with
# a file to simplify checking for viability.  We always simply
# create the ramdisk with mkfs since we don't care what is in 
# it from previous runs.
#

#
# Extract the name of mounted filesystem we are looking for.
# Use both the name and device to be sure we've got what we need.
#
fsexists=`mount | grep "$RAMFSNAME" | grep "$RAMFSDEV" | awk '{print $1}'`

#
# If we need to create a ramdisk and mount point we do
# it all at once since we don't care what's in it.
#
if test $fsexists
then

  elog "$RAMFSNAME DOES exist mounted on $RAMFSDEV"

else

  elog "$RAMFSNAME NOT exists - Creating and mounting"

  mkdir -p $RAMFSNAME	# -p won't error if already existing.
  chmod 777 $RAMFSNAME

  elog "Creating ramdisk $RAMFSDEV $RAMFSSIZE"
  cmdsts=`mkfs -q $RAMFSDEV $RAMFSSIZE`
  if test $cmdsts
  then
    elog "Create ramdisk FAILURE - Exiting!"
    exit 1
  else
    elog "Create ramdisk SUCCESS"
  fi

  elog "Mounting ramdisk $RAMFSDEV on $RAMFSNAME"
  cmdsts=`mount $RAMFSDEV $RAMFSNAME`
  if test $cmdsts
  then
    elog "Mounting ramdisk FAILURE - Exiting!"
    exit 1
  else
    elog "Mounting ramdisk SUCCESS"
  fi

fi	# test $fsexists

#
# Check again to be SURE we are using a ramdisk FS.
# Give up if no go.
#
fsexists=`mount | grep "$RAMFSNAME" | grep "$RAMFSDEV" | awk '{print $1}'`
if test $fsexists
then
  :
else
  elog "Cannot create or mount ramdisk filesystem - Exiting!"
fi

#
# Use the seed file to see if it is functional.
# Create the seed file again if needed.
#
elog "$RAMFSNAME DOES exist - Checking if seeded"
if test -f "$RAMFSNAME/-MOUNTED-"
then
  elog "$RAMFSNAME is seeded"
else
  elog "Seeding $RAMFSNAME"
  touch "$RAMFSNAME/-MOUNTED-"
  if test -f $DSTPATHFILE
  then
    elog "Copying any existing destination back for comparison"
    cp $DSTPATHFILE $SRCFILE
  fi
fi

#
# From here on we use the file logger.
#

#
# Always create a fresh status entry of this script being run.
# We log anything we need for debugging here.
#
rm -f $LOGFNAME
flog "$0"
flog "`date`"

#
# SMB is stupid enough that it won't get a file if the destination
# already exists.  That's ok as we need a compare file anyway.
#
if test -f $SRCFILE
then
  flog "Deleting/copying $SRCFILE to $CMPFILE"
  rm -f $CMPFILE
  mv $SRCFILE $CMPFILE
fi

#
# Get the file we are looking for.  Be verbose about it and 
# send the verbosity to the log file.  Trap any issues
# that crop up.
#
# NOTE: Do NOT leave any blank lines in this command string!
#
smbget \
--username=$SMBUSER \
--password=$SMBPASS \
--workgroup=$SMBWORKGROUP \
-v \
$SMBSRCFILE \
-o $SRCFILE >> $LOGFNAME 2>&1

cmdsts=$?
if test $cmdsts -eq 0
then
  flog "smbget appears to succeed"
else
  flog "Severe error $cmdsts in smbget command - Exiting!"
  exit 1
fi

#
# If both files exist (not the first time run) then
# compare them.
#
if test -f $SRCFILE && test -f $CMPFILE
then

  flog "Diffing $SRCFILE against $CMPFILE"
  diff $SRCFILE $CMPFILE >> $LOGFNAME
  cmdsts=$?
  if test $cmdsts -eq 0
  then
    flog "No differences found"
  else
    flog "Differences found - Updating reference copy for other apps"
    flog "Creating .lck and copying to $DSTPATHFILE"
    touch $DSTPATHFILE.lck
    sleep 1
    cp -f $SRCFILE $DSTPATHFILE
    rm -f $DSTPATHFILE.lck
    sync
  fi

else

#
# If we don't yet have BOTH files (this else clause)
# we want to be SURE to send any initial found file.
#
  if test -f $SRCFILE
  then
    if test -f $DSTPATHFILE
    then
      :
    else
      flog "Copying initial $SRCFILE to $DSTPATHFILE"
      cp -f $SRCFILE $DSTPATHFILE
      sync
    fi
  fi

fi	 # test -f DST/CMP files

