#!/bin/bash

usage()
{
	echo "To start a GDA RCP Client of local server or beamline remote server"
	echo "Usage:"
	echo "       gdaclient local"
	echo "   or:"
	echo "       gdaclient remote"
}


if [ $# -ne 1 ]; then
	usage
	exit 1
fi


Properties=$configDir/properties/java.properties_mobilerack


if [ ! -n "$BEAMLINE" ];
then
  echo "Please set BEAMLINE environment variable."
  exit 1
fi

if [ ! -n "$GDA_HOME" ]; then
	GDA_HOME=/dls_sw/$BEAMLINE/software/gda
	echo "No GDA_HOME setup, use the default $GDA_HOME."
fi

if [ ! -n "$GDA_CONFIG" ]; then
	GDA_CONFIG=$GDA_HOME/config
	echo "No GDA_CONFIG setup, use the default $GDA_CONFIG."
fi


gdaLauncher=$GDA_HOME/plugins/uk.ac.gda.core/bin/gda 

case $1 in
   "local")
		echo "To start a Client of local GDA."
		JacorbDir=$GDA_CONFIG/properties/jacorb_i06_local
		varDir=/tmp/gda/var
		dataDir=/tmp/gda
		logDir=/tmp/gda/logs
		;;
   "remote") 
		echo "To start a Client of Beamline GDA."
		$GDA_CONFIG/bin/GDA_StartClient
		exit 0;
		;;
   *)
		usage
		exit 1
		;;
esac
	 
#JAVA_OPTS="-Xms512m -Xmx2048m -XX:PermSize=182m -XX:MaxPermSize=786m" $gdaLauncher --properties=$Properties --jacorb=$JacorbDir --rcp_image=$GDA_HOME/client/gda-${BEAMLINE} --start rcpclient &
JAVA_OPTS="-Xms512m -Xmx1024m -XX:PermSize=182m -XX:MaxPermSize=786m -XX:+DisableExplicitGC" $gdaLauncher --properties=$Properties  --jacorb=$JacorbDir --vardir=$varDir --datadir=$dataDir --logsdir=$logDir --rcp_image=/dls_sw/$BEAMLINE/software/gda/client/gda-${BEAMLINE} --start rcpclient &


