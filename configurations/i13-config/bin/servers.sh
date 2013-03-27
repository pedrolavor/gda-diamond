# runs the servers locally

#identify install folder and JAVA_HOME
source /dls_sw/i13/etc/i13_profile.sh

. /usr/share/Modules/init/bash
module load java/gda830-64

#this is needed to ensure the acls work properly
umask 0002

export LOGFILE=$GDALOGS/gda_output_`date +%F-%T`.txt
touch $LOGFILE
rm $GDALOGS/gda_output.txt
ln -s $LOGFILE $GDALOGS/gda_output.txt

echo GDAFOLDER=$GDAFOLDER
echo BEAMLINE=$BEAMLINE
SERVER_STARTUP_FILE=$GDAVAR/object_server_startup_server_main; export SERVER_STARTUP_FILE
rm -f $SERVER_STARTUP_FILE

echo "Starting GDA. Output is being logged to $LOGFILE"

export JAVA_OPTS="-Xms128m -Xmx1024m -XX:MaxPermSize=128m -XX:+DisableExplicitGC"

nohup python ${GDAFOLDER}/workspace_git/gda-core.git/uk.ac.gda.core/bin/gda  --smart --trace --config=$GDAFOLDER/config --restart -v --mode=$GDAMODE nameserver > $LOGFILE 2>&1 &


nohup python ${GDAFOLDER}/workspace_git/gda-core.git/uk.ac.gda.core/bin/gda  --smart --trace --config=$GDAFOLDER/config --restart -v --mode=$GDAMODE logserver > $LOGFILE 2>&1 &


nohup python ${GDAFOLDER}/workspace_git/gda-core.git/uk.ac.gda.core/bin/gda --smart --trace --config=$GDAFOLDER/config --debug -p 8002 --restart -v --mode=$GDAMODE eventserver > $LOGFILE 2>&1 &

export JAVA_OPTS="-Xms128m -Xmx4096m -XX:MaxPermSize=128m -XX:+DisableExplicitGC"
#export JAVA_OPTS="$JAVA_OPTS -javaagent:/home/tjs15132/.eclipse/org.eclipse.platform_4.2.0_1709057204/plugins/org.zeroturnaround.eclipse.embedder_5.2.0.SR1-201303112135/jrebel/jrebel.jar -Drebel.workspace.path=/dls_sw/i13/software/gda_versions/gda_8_30/workspace -Drebel.log.file=/ldls_sw/i13/software/logs/jrebel.log -Drebel.properties=/dls_sw/i13/software/gda_versions/gda_8_30/workspace/jrebel.properties -Drebel.notification.url=http://127.0.0.1:46416/jrebel/notifications -Dhttp.proxyHost=wwwcache.rl.ac.uk -Dhttp.proxyPort=8080 -Dhttp.nonProxyHosts=dasc-git.diamond.ac.uk|localhost|127.0.0.1"
nohup python ${GDAFOLDER}/workspace_git/gda-core.git/uk.ac.gda.core/bin/gda --smart --trace --config=$GDAFOLDER/config --debug -p 8001 --restart -v --mode=$GDAMODE objectserver > $LOGFILE 2>&1 &
echo "Looking for file $SERVER_STARTUP_FILE"
$GDAFOLDER/config/bin/lookForFile $SERVER_STARTUP_FILE
