#!/dls_sw/prod/tools/RHEL5/bin/dls-python2.6
#
#this is a stand-alone python/epics script-- run without GDA
#
# written by Robert Atwood 
# $Id: tomo_tfg.py 214 2012-02-13 15:46:36Z kny48981 $
### required libraries and modules
import sys
import os
import commands
import time
import math
import subprocess
from pkg_resources import require
require("numpy")
require("cothread")
import cothread
from cothread.catools import *
####end of module section 

tomopos=0    # tomography position centre of rotation (corrected from 1002.358)
flatpos=-100        # ss1.x position for flatfields
exp=.05             # exposure time
anglestep=.25     #angle(360/1440) 
trigpv="BL12I-EA-DIO-01:OUT:02"
hightime=0.15
tfgscript="tfgscript.cmd"


def setup_tfg(exposure,nsteps,myfolder):
   global tfgscript
   tfgscript="%s/tfgscript.cmd" % myfolder
   print "setting up for %i steps" % (nsteps+1)
   sys.stdout=open(tfgscript,"w")
#   print("""\
#tfg config "etfg0" tfg2
#tfg setup-groups sequence "seq0"
#1 0 %f    0 1 0 8 0 0
#1 0 10e-9  0 0 0 40 0 0
#1 0 10e-3 0 2 0 10 0 0
#1 0 10e-9  0 0  0 42 0 0
#-1
#tfg setup-groups cycles %i 
#1 seq0
#-1
#tfg start
#tfg wait ignore-pause
#""") % (exposure,nsteps+1)
#
   if (exposure < 0.125):
      pausetime=0.125-exposure
   else:
      pausetime=0

   print("""\
tfg config "etfg0" tfg2
tfg setup-groups sequence "seq0"
1 0 %f    0 257 0 9 0 0
1 0 10e-9  0 0 0 41 0 0
1 %f 10e-3 0 2 0 10 0 0
1 0 10e-9  0 2048  0 42 0 0
-1
tfg setup-groups sequence "seq1"
1 0 10e-9  0 0  0 42 0 0
-1
tfg setup-groups cycles %i 
1 seq0
-1
tfg setup-cc-mode scaler64
tfg setup-cc-chan 0 vetoed-edge
tfg setup-cc-chan 3 time-veto
tfg setup-cc-chan 4 time-veto
tfg setup-cc-chan 5 time-veto
set-func "path" "tfg open-cc"
clear %%path
enable %%path
tfg start
tfg wait ignore-pause
""") % (exposure,pausetime,nsteps+1)
#tfg wait ignore-pause
#read 0 0 0 6 1 9 from %%path to-local-file "out.txt"
#end of the  script text
   sys.stdout.flush()
   sys.stdout=sys.__stdout__

  

def doflat(nflat=5):
   global flatpos
   global tomopos
   global trigpv
   print("moving to flat position")
   caput ("BL12I-MO-TAB-02:X.VAL", flatpos, wait=True,timeout=300);

   print ("Setting CAM:NumImages")
   caput("BL12I-EA-DET-02:CAM:NumImages",1,wait=False)
   caput("BL12I-EA-DET-02:CAM:ImageMode",0,wait=True)
   caput("BL12I-EA-DET-02:CAM:TriggerMode",1,wait=True)

   print ("Setting TIF:NumCapture")
   caput("BL12I-EA-DET-02:TIF:NumCapture",nflat)
   print ("Setting capture on TIF:Capture=1")
   caput ("BL12I-EA-DET-02:TIF:Capture",1,wait=False)
   print ("TIF:Capture: set to 1 ")
   cothread.Sleep(2)
   print("Arming the camera")
   caput("BL12I-EA-DET-02:CAM:ARM_MODE",1,wait=True,timeout=300)

   for idx in range(0,nflat,1):
      print ("Acquiring CAM:Acquire")
      caput("BL12I-EA-DET-02:CAM:Acquire",1,wait=True, timeout=300)

   print ("TIF:Capture: 0 ")
   caput ("BL12I-EA-DET-02:TIF:Capture",0)
   caput("BL12I-EA-DET-02:CAM:Acquire",0,wait=True,timeout=60)

   print("moving to tomography position")
   caput ("BL12I-MO-TAB-02:X.VAL", tomopos, wait=True,timeout=300);

def doscan(nsteps=1800,exposure=0.3,readout=0.4):
   global trigpv
   global hightime
   print "Entering doscan routine"
   nplus=nsteps + 1
   print ("Setting CAM:NumImages")
   caput("BL12I-EA-DET-02:CAM:NumImages",1,wait=False)
   caput("BL12I-EA-DET-02:CAM:ImageMode",0,wait=True)
   caput("BL12I-EA-DET-02:CAM:TriggerMode",3,wait=True)

   print ("Setting TIF:NumCapture",nplus)
   caput("BL12I-EA-DET-02:TIF:NumCapture",nplus)
   print ("setting TIF:Capture: 1 ")
   caput ("BL12I-EA-DET-02:TIF:EnableCallbacks",1,wait=True,timeout=10)
   caput ("BL12I-EA-DET-02:TIF:FileNumber",0,wait=False)
   caput ("BL12I-EA-DET-02:TIF:Capture",1,wait=False)


   caput("BL12I-EA-DET-02:CAM:ArrayCounter",0)

   print("Arming the camera")
   caput("BL12I-EA-DET-02:CAM:ARM_MODE",1,wait=True,timeout=300)

   print "Allowing time for camera to arm"
   cothread.Sleep(3.5)
   camstat=caget("BL12I-EA-DET-02:CAM:ARM_MODE_RBV")
   while (camstat != 1 ):
      cothread.Sleep(1)
      camstat=caget("BL12I-EA-DET-02:CAM:ARM_MODE_RBV")
      print "camstat: ", camstat
   print "continuing..."



   #call the TFG
   print "cat %s | nc i12-tfg2-10ge 1972" % tfgscript 
   print "Allowing time for tfg to arm"
   cothread.Sleep(2)
   print "continuing..."
   subprocess.call("cat %s | nc i12-tfg2-10ge 1972" % tfgscript ,shell=True)

   #while [[ 1 == 1 ]]:
   #    ostring=subprocess.call("echo 'tfg read progress' | nc i12-tfg2-10ge 1972" ,shell=True)
   #    print "ostring: ", ostring
   #    cothread.Sleep(1)


   camstat=caget("BL12I-EA-DET-02:TIF:WriteFile_RBV")
   print "camstat: ", camstat
   cothread.Sleep(exposure)
   camstat=caget("BL12I-EA-DET-02:TIF:WriteFile_RBV")
   print "camstat: ", camstat
   while (int(camstat) == 1):
      print "WARNING: camera not finished!"
      print "Pushing the Snooze alarm..."
      cothread.Sleep(5)
      camstat=caget("BL12I-EA-DET-02:TIF:WriteFile_RBV")
      print "camstat: ", camstat
   print "camstat: ", camstat
   print "continuing..."
   print ("TIF:Capture: 0 ")
   caput("BL12I-EA-DET-02:CAM:ARM_MODE",0,wait=True,timeout=60)
   caput ("BL12I-EA-DET-02:TIF:Capture",0)
   caput ("BL12I-EA-DET-02:TIF:EnableCallbacks",0,wait=True,timeout=10)
   caput("BL12I-EA-DET-02:CAM:TriggerMode",2,wait=True)

#MAIN part

#caput("BL12I-EA-DET-02:CAM:ADC_MODE", 1,wait=True,timeout=60)
if (len(sys.argv) < 4):
   print " Usage: %s <scan-name> <num-projections> <exposure-time-s> " % sys.argv[0]
   print "CAUTION: bad scan name can crash the server"
   sys.exit(0)

scanname=sys.argv[1]
nproj=int(sys.argv[2])
exposure=float(sys.argv[3])

folderstr="/data/2012/cm5706-1/tmp/"

linfolder="/dls/i12/%s" % folderstr
winfolder="Z:/%s" % folderstr

linbasefolder = "%s/%s" % (linfolder,scanname)
linprojfolder = "%s/projections" % linbasefolder

winbasefolder = "%s/%s" % (winfolder,scanname)
winprojfolder = "%s/projections" % winbasefolder



if not (os.access (linbasefolder, os.F_OK)):
   os.mkdir(linbasefolder)
else:
   print("Directory %s already exists!" % linbasefolder)
   print("Please use a different folder or move the folder away")
   sys.exit(0)

if not (os.access (linbasefolder, os.F_OK)):
   print ("COULD NOT CREATE %s",linbasefolder)
   sys.exit(0)

if not (os.access (linprojfolder, os.F_OK)):
   os.mkdir(linprojfolder)

if not (os.access (linprojfolder, os.F_OK)):
   print ("COULD NOT CREATE %s",linprojfolder)
   sys.exit(0)


#stop the camera
caput("BL12I-EA-DET-02:CAM:Acquire",0,wait=True)

# save the state of callback tabs
#procstate=caget("BL12I-EA-DET-02:PRC1:EnableCallbacks")
statstate=caget("BL12I-EA-DET-02:STAT:EnableCallbacks")
roistate=caget("BL12I-EA-DET-02:ROI1:EnableCallbacks")
modestate=caget("BL12I-EA-DET-02:CAM:ImageMode")
expstate=caget("BL12I-EA-DET-02:CAM:AcquireTime_RBV")

#disable the callbacks
#caput("BL12I-EA-DET-02:PROC:EnableCallbacks",0,wait=True)
caput("BL12I-EA-DET-02:STAT:EnableCallbacks",0,wait=True)
caput("BL12I-EA-DET-02:ROI1:EnableCallbacks",0,wait=True)


caput("BL12I-EA-DET-02:TIF:FilePath",winprojfolder,datatype=DBR_CHAR_STR)
caput("BL12I-EA-DET-02:TIF:FileName","p_",datatype=DBR_CHAR_STR)
caput("BL12I-EA-DET-02:TIF:FileTemplate","%s%s%05d.tif",datatype=DBR_CHAR_STR)



print ("Setting CAM:NumImages")
caput("BL12I-EA-DET-02:TIF:EnableCallbacks",1,wait=True,timeout=60)
caput("BL12I-EA-DET-02:CAM:Acquire",0,wait=True,timeout=60)
caput("BL12I-EA-DET-02:CAM:NumImages",1,wait=False)
caput("BL12I-EA-DET-02:CAM:ImageMode",0,wait=True)
caput("BL12I-EA-DET-02:CAM:TriggerMode",1,wait=True)
caput("BL12I-EA-DET-02:TIF:FileNumber",0,wait=True)
caput("BL12I-EA-DET-02:CAM:AcquireTime",exposure,wait=True)

testexp = caget("BL12I-EA-DET-02:CAM:AcquireTime_RBV")

if not (testexp == exposure):
   print("Exposure time didn't get set properly! requested %f got %f " % (exposure,testexp) )
   sys.exit(0)




#setup the TFG with the number of steps and exposure time

setup_tfg(exposure,nproj,linbasefolder)

print("calling doscan")
doscan(nproj,exposure)
#restore the callbacks
sys.exit(0)



print "restoring the image mode"
caput("BL12I-EA-DET-02:CAM:ImageMode",modestate,wait=True)
print "restoring the exposure"
caput("BL12I-EA-DET-02:CAM:AcquireTime",expstate,wait=True)
print "restoring the tab callbacks"
caput("BL12I-EA-DET-02:PRC1:EnableCallbacks",procstate,wait=True)
caput("BL12I-EA-DET-02:STAT:EnableCallbacks",statstate,wait=True)
caput("BL12I-EA-DET-02:ROI1:EnableCallbacks",roistate,wait=True)

