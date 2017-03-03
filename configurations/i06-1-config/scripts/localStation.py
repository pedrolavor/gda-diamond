#localStation.py
#For beamline specific initialisation code.

print "===================================================================";
print "Performing Beamline I06-1 specific initialisation code (localStation.py).";
print

print "-"*100
print "Set scan returns to the start positions on completion"
print "   To set scan returns to its start positions on completion please do:"
print "      >>>scansReturnToOriginalPositions=1"
scansReturnToOriginalPositions=0;
print

from i06shared.localStation import *  # @UnusedWildImport

from Beamline.beamline import getTitle,gettitle,getvisit,getVisit,lastscan,setDir,setdir,setTitle,settitle,setVisit,setvisit  # @UnusedImport
from Beamline.createAlias import closebeam, openbeam  # @UnusedImport
from Beamline.U2Scaler8513 import ca61sr,ca62sr,ca63sr,ca64sr,ca65sr,ca66sr,ca67sr,ca68sr,scaler2  # @UnusedImport

#To eLog the scan
from Beamline.beamline import branchline
fileHeader.setScanLogger(branchline);

from i06shared.lasers.useSlap2 import laser2, laser2phase,laser2delay,laser2locking  # @UnusedImport
#End Station Section

##Magnet
from magnet.useMagnet import scm,magmode,magcartesian,magspherical,magx,magy,magz,magrho,magth,magphi,magdelay,magtolerance,hyst2,dhyst,logValues,negLogValues,negPosLogValues,cw  # @UnusedImport
##Pixis - there is a java object replement
#from cameras.usePixis import pixis
##Exit Slit
from slits.useS6 import s6ygap, s6xgap  # @UnusedImport
#Group the hexapod legs into list
m7legs = [m7leg1, m7leg2, m7leg3, m7leg4, m7leg5, m7leg6];  # @UndefinedVariable
#To add branchline device position to the SRS file header
branchMirrorList = [m7x, m7pitch, m7qg]; fileHeader.add(branchMirrorList);  # @UndefinedVariable
branchDiodeList = [d9y, d10y, d11y]; fileHeader.add(branchDiodeList);  # @UndefinedVariable
branchExitSlitList = [s6x, s6xgap, s6y, s6ygap]; fileHeader.add(branchExitSlitList);  # @UndefinedVariable
from functionDevices.idivio import idio,ifio  # @UnusedImport
from Beamline.waveplate3 import wp32  # @UnusedImport

print "===================================================================";
print " end of localStation.py"



