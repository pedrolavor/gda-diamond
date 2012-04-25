#!/bin/bash  
#$Id: do_all_sinograms.sh 219 2012-02-17 18:44:10Z kny48981 $
timestamp=`date +%y%m%d%H%M%S%N`
#set up some version tracking
svnid='$Id: do_all_sinograms.sh 219 2012-02-17 18:44:10Z kny48981 $ '
svnurl='$URL: file:///home/kny48981/SVN/progs/scripts/trunk/do_all_sinograms.sh $ '

#modules don't work for gda user
source /dls_sw/i12/modulefiles/modules.sh

#add the modules required 
module add i12
module add global/cluster


visit="cm5706-1"
year=2012
nflat=24
cstart=1995
cstep=1 
cslice=1300
cnsteps=32 Iflag=0
Iflag=0
iflag=0
nproj=6000

rawfolder="processing/rawdata/"
sinofolder="processing/sino/"

usage(){
echo "version information:"
echo $svnid 
echo $svnurl

echo ""
echo "Usage:"
echo "$0 [-y year($year) ] -V visit($visit)  -s start-centre($cstart) -n nsteps-centre($cnsteps) -t centre-step($cstep)"
echo " -S testslice($cslice) -I list-file  -i input-folder -f flat-folder -d dark-folder  [ one of I or i,f,d is REQUIRED]"
echo " -R [raw data folder after 'visit'] (currently $rawfolder)"
echo " -O [sinogram output folder after 'visit'] (currently $sinofolder) "
#echo " -p number of projections (currently $nproj) "
echo " "
echo "Generate sinograms and run first centreing routine on a range of samples"
echo "This script submits the jobs to the queue with queue-hold instructions. If the sinograms already exist, their generation is skipped"
echo "the 'list-file' contains the sample names, the flat field should be in a folder of the same name prefixed with 'ff1' "
}

if [[ $# -lt 1 ]]
then
   echo "No command line options specified"
   usage
   exit
fi
Rflag=0
dflag=0
fflag=0
iflag=0


#parse the options
while getopts "V:y:f:d:s:S:n:t:hI:R:O:p:i:" flag
do
  case $flag in
  "p")
    nproj=$OPTARG
  ;;
  "R")
    rawfolder="$OPTARG"
    Rflag=1
  ;;
  "O")
    sinofolder="$OPTARG"
    Oflag=1
  ;;
  "I")
    listfile="$OPTARG"
    Iflag=1
  ;;
  "i")
    expname="$OPTARG"
    iflag=1
  ;;
  "y")
    year=$OPTARG
  ;;
  "V")
    visit=$OPTARG
  ;;
  "f")
    flatfolder=$OPTARG
    fflag=1
  ;;
  "d")
    darkfolder=$OPTARG
    dflag=1
  ;;
  "s")
   cstart=$OPTARG
  ;;
  "n")
     cnsteps=$OPTARG
  ;;
  "S")
     cslice=$OPTARG
  ;;
  "t")
     cstep=$OPTARG
  ;;
  "h")
     usage
     exit
  ;;
  esac

done
if [[ $Iflag  || ( $iflag && $fflag && $dflag ) ]]
then
   goflag=1
else
   goflag=0
fi

if [[ $goflag -eq 0 ]] 
then
      echo "*************************"
      echo "ERROR Cannot proceed without input specification (-I  or -i flag)"
      echo "*************************"
      usage
      exit
fi


if [[ $Iflag -ne 1 ]]
then

   if [[ $iflag -ne 1 ]]
   then
      echo "*************************"
      echo "ERROR Cannot proceed without input specification (-I  or -i flag)"
      echo "*************************"
      usage
      exit
   fi

fi

if [[ $iflag -eq 1 ]]
then
   echo "expname $expname flatfolder $flatfolder darkfolder $darkfolder"
   listfile="/tmp/${$}autolist.txt"
   echo $expname $flatfolder $darkfolder  > $listfile
fi

echo "Inputs and  defaults:"
echo "listfile $listfile"
echo "year $year"
echo "visit $visit"
echo "cstart $cstart"
echo "cnsteps $cnsteps"
echo "cslice $cslice"
echo "cstep $cstep"

#set up the data folder paths
## arranging to have sinograms in a seperate folder

rootfolder="/dls/i12/data/$year/"
rawfolder="default"
sinofolder="processing/sino"

qfolder="q_output"
qpath=$rootfolder/$visit/$sinofolder/$qfolder
mywd=`pwd`

echo "raw data in $rootfolder/$visit/$rawfolder/"
echo "sinograms into $rootfolder/$visit/$sinofolder/"
echo "misc queue output into $qpath"

#check and/or create the folders

if [[ ! -d $rootfolder/$visit/$sinofolder/ ]]
then
   echo "sinogram folder not found"
   echo "$rootfolder/$visit/$sinofolder"
   echo "attempting to create..."
   mkdir $rootfolder/$visit/$sinofolder
fi

if [[ ! -d $qpath/ ]]
then
   echo "queue output folder not found"
   echo "$qpath"
   echo "attempting to create..."
   mkdir $qpath
fi

if [[ ! -d $rootfolder/$visit/$sinofolder/ ]]
then
   echo "sinogram folder STILL not found"
   echo "sinogram folder STILL not found, or the file of that name is not a folder"
   ls -ld $rootfolder/$visit/$sinofolder
   echo "There must be some permission problem on the parent folder"
   echo "exiting .. "
   exit
fi

declare -a sname
while read sline
do
   sname=($sline)
   pfolder=$rootfolder/$visit/$rawfolder/${sname[0]}/projections
   ffolder=$rootfolder/$visit/$rawfolder/${sname[1]}/projections
   dfolder=$rootfolder/$visit/$rawfolder/${sname[2]}/projections
   rfolder=$rootfolder/$visit/$sinofolder/$sname
   echo "projections folder: $pfolder"
   echo "flat folder: $ffolder"
   echo "dark folder: $dfolder"
   echo "sinograms folder $rfolder"

   nflat=`ls $ffolder | wc -w`
   (( nflat = $nflat - 1 ))
   nproj=`ls $pfolder | grep 'p.*tif'  | wc -w`
   (( nproj = $nproj - 1 ))
   echo "Calculated: "
   echo "sname: " $sname "nflat: " $nflat "nproj: " $nproj


   mkdir  $rfolder
   # average the flat field file
   cd $rfolder

   holdflag=0
   #get output of qsub and split the line into array variable
     qjobline=(`echo "/dls_sw/i12/software/tomography_scripts/flat_capav  -i $ffolder -o flat -a $nflat" | qsub -N flat -e $qpath -o $qpath`)
     qflatid=${qjobline[2]}
     echo "flat queue job is $qflatid"
     fholdflag=1
     holdflag=1

   #get output of qsub and split the line into array variable
     qjobline=(`echo "/dls_sw/i12/software/tomography_scripts/flat_capav  -i $dfolder -o dark -f dark -a $nflat" | qsub  -hold_jid $qflatid -N dark -e $qpath -o $qpath`)
     qdarkid=${qjobline[2]}
     echo "dark queue job is $qdarkid"
     dholdflag=1
     holdflag=1

   #copy the local settings file
   #if available
   if [[ -e $mywd/settings.xml ]]
   then
      echo "Using local reconstruction settings file"
      cp $mywd/settings.xml $rfolder
   else
      echo "Default reconstruction settings file will be used"
   fi

   if [[ -d $rfolder/sinograms ]]
   then

      # do a centering with existing sinograms
      set -x
      qcentrexml.py $cstart $cnsteps $cstep  $cslice 1 1 
      set +x

   else

      #generate sinograms and wait for the job to finish
      #then do the centereing

      datestring=`date +"%m%d%H%M%S"`

         jstring=`/dls_sw/i12/software/tomography_scripts/sino_listener.py  -W ${qdarkid} -J S$sname -U $datestring -i $pfolder -p $nproj -n 16 -Q low.q | tee out$datestring.txt |  grep "JOB NAME IS"`

      rv=$?
      echo "return value" $rv
      declare -a jobline
      echo "JSTRING:" $jstring
      jobline=($jstring)
      nm=${jobline[3]}
      echo "HOLDNAME: " $nm

      set -x
      qcentrexml.py $cstart $cnsteps $cstep  $cslice 1 1  $nm
      set +x

   fi

done < $listfile

if [[ $iflag -eq 1 ]]
then
   rm  $listfile
fi

