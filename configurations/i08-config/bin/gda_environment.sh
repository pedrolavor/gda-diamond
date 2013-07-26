#!/bin/sh
# This script assumes that $BEAMLINE is set (e.g. i02, i08, b16) if not exit...

# **** DO NOT EDIT THIS SCRIPT AS IT MAY BE AUTOMATICALLY OVERWRITTEN *****

if [ ! -n "$BEAMLINE" ]; 
then
  echo "Please set BEAMLINE environment variable."
  exit 1
fi
if [ ! -n "$SOFTWAREFOLDER" ]; 
then
  echo "Please set SOFTWAREFOLDER environment variable."
  exit 1
fi
unset ANT_HOME
unset JAVA_HOME
unset JYTHON_HOME
unset SVN_HOME

export PATH=/$SOFTWAREFOLDER/$BEAMLINE/software/gda/bin:/$SOFTWAREFOLDER/$BEAMLINE/bin:${PATH}
