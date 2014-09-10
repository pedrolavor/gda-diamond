#bash file used to easily create External Program launch configurations in Eclipse to start servers from the IDE
#The arguments give the location of the gda command, config , the mode and the command (start or stop)
#${project_loc:uk.ac.gda.core} ${project_loc:i11-config} dummy --restart
echo $1 $2 $3 $4
$1/bin/gda --smart --verbose --config $2 --mode $3 $4 logserver
$1/bin/gda --smart --verbose --config $2 --mode $3 $4 nameserver 
$1/bin/gda --smart --verbose --config $2 --mode $3 $4 eventserver
$1/bin/gda --smart --verbose --config $2 --mode $3 $4 --debug objectserver
