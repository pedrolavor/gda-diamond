#! /bin/bash

. /usr/share/Modules/init/bash

module load global/cluster

# those two need to be in sync
#DAWN=/dls_sw/apps/DawnDiamond/1.4.1/builds-stable/stable-linux64/dawn
#DAWN=/dls/b21/data/2014/cm4976-1/tmp/DawnDiamond-1.5.0.v20140314-1320-linux64/dawn
#MOML=${GDA_CONFIG}/processing/ncd_model.moml
# those would be found in the environment
# beamline staff specified
#PERSISTENCEFILE=/home/zjt21856/persistence_file.nxs
#NCDREDXML=/home/zjt21856/ncd_configuration.xml
# these should be on the command line
#DATAFILE=/home/zjt21856/i22-34820.nxs
#BACKGROUNDFILE=/home/zjt21856/i22-34820.nxs
#ISPYBUPDATE=$(dirname $0)/updateispyb.py

DATAFILE="$1"
BACKGROUNDFILE="$2"
DATACOLLID="$3"

# avoid messages popping up in testing
export DISPLAY=
REDUCTIONOUTPUTFILE=

echo edited file
#is file in visit
read VISIT RESTOFPATH <<<$( echo $DATAFILE | sed 's,\(/dls/.../data/20../[-a-z0-9]*\)/\(.*\),\1 \2,')
RESTOFPATH=${RESTOFPATH%.*}
echo $RESTOFPATH
if test -d $VISIT ; then
	echo running reduction in visit based directory under $VISIT
	if test -w $VISIT ; then
		REDUCTIONOUTPUTFILE=${VISIT}/processed/${RESTOFPATH}.reduced.nxs
		mkdir -p $(dirname $REDUCTIONOUTPUTFILE)
	else 
		REDUCTIONOUTPUTFILE=${VISIT}/processing/${RESTOFPATH}.reduced.nxs
		mkdir -p $(dirname $REDUCTIONOUTPUTFILE)
		REDUCTIONOUTPUTFILE=
	fi
	TMPDIR=${VISIT}/tmp/${RESTOFPATH}.$$
else
	echo running reduction outside of a visit
	TMPDIR=${DATAFILE}.$$.reduction
fi

mkdir -p $TMPDIR
cd $TMPDIR
echo now in $TMPDIR

WORKSPACE=$TMPDIR/workspace
mkdir $WORKSPACE
OUTPUTDIR=$TMPDIR/output
mkdir $OUTPUTDIR

sed "s,bgFile>.*</bgFile,bgFile>${BACKGROUNDFILE}</bgFile," < $NCDREDXML > ncd_reduction.xml
NCDREDXML=${TMPDIR}/ncd_reduction.xml

mkdir ${WORKSPACE}/workflows/
WORKSPACEMOML=${WORKSPACE}/workflows/reduction.moml
ln -s $MOML $WORKSPACEMOML

SCRIPT=$TMPDIR/biosaxsqsub.script
cat >> $SCRIPT <<EOF
#! /bin/sh

. /usr/share/Modules/init/sh

module load java/7-64
module load python/ana
module load cothread

## set data reduction to started
$ISPYBUPDATE reduction $DATACOLLID STARTED \"\"

export MALLOC_ARENA_MAX=4

$DAWN -noSplash -application com.isencia.passerelle.workbench.model.launch \
-data $WORKSPACE \
-consolelog -os linux -ws gtk -arch $(arch) -vmargs \
-Dorg.dawb.workbench.jmx.headless=true \
-Dcom.isencia.jmx.service.terminate=false \
-Dmodel=$WORKSPACEMOML \
-Dlog.folder=$TMPDIR \
-Dxml.path=$NCDREDXML \
-Draw.path=$DATAFILE \
-Declipse.pluginCustomization=/dls_sw/b21/software/gda/config/processing/plugin_customisation.ini \
-Dpersistence.path=$PERSISTENCEFILE \
-Doutput.path=$OUTPUTDIR

for i in $OUTPUTDIR/results*.nxs ; do
	GENERATEDFILE=\$i
	break;
done

if test -n "\$GENERATEDFILE" && test -r \$GENERATEDFILE ; then
 : # all fine, but tell ISPyB later
else 
	# raise ISPyB error and exit
	MESSAGE="ERROR cannot find generated reduction file for collection $DATACOLLID in $OUTPUTDIR"
	$ISPYBUPDATE reduction $DATACOLLID FAILED \$MESSAGE 
	echo \$MESSAGE  >&2
	echo ABORTING. >&2
	exit 1
fi

if test -n "$REDUCTIONOUTPUTFILE" ; then 
	ln \$GENERATEDFILE $REDUCTIONOUTPUTFILE
	REDUCEDFILE="$REDUCTIONOUTPUTFILE"
else
	REDUCEDFILE=\$GENERATEDFILE
fi

# tell ispyb reduction worked and result is in \$REDUCEDFILE
$ISPYBUPDATE reduction $DATACOLLID COMPLETE \$REDUCEDFILE

EOF

#bash $SCRIPT > ${SCRIPT}.stdout 2> ${SCRIPT}.errout
qsub -pe smp 8-16 -q medium.q -l h_rt=01:30:00 -N ${BEAMLINE}BIOSAXS $SCRIPT
