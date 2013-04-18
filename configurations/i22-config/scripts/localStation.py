#localStation.py
#For beamline specific initialisation code.
#
print "===================================================================";
print "Performing beamline specific initialisation code (i22).";
print

print "Importing generic features...";
import java
from gda.configuration.properties import LocalProperties
from gda.device.scannable.scannablegroup import ScannableGroup
from time import sleep
from gda.jython.commands.GeneralCommands import alias


# Get the locatation of the GDA beamline script directory
gdaScriptDir = "/dls/i22/software/gda/config/scripts/"
gdascripts = "/dls/i22/software/gda/workspace_git/gda-core.git/uk.ac.gda.core/scripts/gdascripts/"

execfile(gdascripts + "/pd/epics_pds.py");
execfile(gdascripts + "/pd/time_pds.py");
execfile(gdascripts + "/pd/dummy_pds.py");
execfile(gdascripts + "/utils.py");

#execfile(gdaScriptDir + "i22.py")

print "Creating beamline specific devices...";
execfile(gdaScriptDir + "energy.py")
execfile(gdaScriptDir + "ExafsScannable.py")

#Set up the Bimorph Mirror 
#print "Setting up access to Bimorph Mirror Channels...";
execfile(gdaScriptDir + "fastshuttershutter.py");
execfile(gdaScriptDir + "bimorph.py");
execfile(gdaScriptDir + "d10XYMaxPosition.py");

execfile(gdaScriptDir + "LookupTables.py");
#execfile(gdaScriptDir + "CheckShutter.py");

bsdiode=DisplayEpicsPVClass('bsdiode', 'BL22I-RS-ABSB-02:DIODE:I', '', '%5.5g')
d10d1=DisplayEpicsPVClass('d10d1', 'BL22I-DI-PHDGN-10:DIODE1:I', '', '%5.5g')
d10d2=DisplayEpicsPVClass('d10d2', 'BL22I-DI-PHDGN-10:DIODE2:I', '', '%5.5g')

i0xplus=DisplayEpicsPVClass("i0xplus","BL22I-DI-IAMP-06:PHD1:I_C","ua","%.3e")
i0xminus=DisplayEpicsPVClass("i0xplus","BL22I-DI-IAMP-06:PHD2:I_C","ua","%.3e")
i0yplus=DisplayEpicsPVClass("i0xplus","BL22I-DI-IAMP-06:PHD3:I_C","ua","%.3e")
i0yminus=DisplayEpicsPVClass("i0xplus","BL22I-DI-IAMP-06:PHD4:I_C","ua","%.3e")
i0=DisplayEpicsPVClass("i0","BL22I-DI-IAMP-06:INTEN_C","ua","%.3e")

s2xplusi=DisplayEpicsPVClass("s2xplusi","BL22I-AL-SLITS-02:X:PLUS:I:FFB","","%.3e")
s2yplusi=DisplayEpicsPVClass("s2yplusi","BL22I-AL-SLITS-02:Y:PLUS:I:FFB","","%.3e")
s2xminusi=DisplayEpicsPVClass("s2xminusi","BL22I-AL-SLITS-02:X:MINUS:I:FFB","","%.3e")
s2yminusi=DisplayEpicsPVClass("s2yminusi","BL22I-AL-SLITS-02:Y:MINUS:I:FFB","","%.3e")

execfile(gdaScriptDir + "TopupCountdown.py")
execfile(gdaScriptDir + "gainpds.py")
execfile(gdaScriptDir + "feedback.py")
execfile(gdaScriptDir + "microfocus.py")

from linkam import Linkam
linkam=Linkam("linkam","BL22I-EA-TEMPC-01")
from linkamrampmaster4000 import LinkamRampMaster4000
lrm4k=LinkamRampMaster4000("lrm4k",linkam)

from installStandardScansWithProcessing import *
scan_processor.rootNamespaceDict=globals()

from redux import NcdRedux
ncdredux = NcdRedux(ncddetectors)

# preseed listener dispatcher
finder.find("ncdlistener").monitorLive("Saxs Plot", "SAXS")
finder.find("ncdlistener").monitorLive("Waxs Plot", "WAXS")

execfile(gdaScriptDir + "atten.py")
execfile(gdaScriptDir + "rate.py")
execfile(gdaScriptDir + "DiodeAverage.py")

#hexapod pivot
#execfile(gdaScriptDir + "hexapod.py")

#create cam1, peak2d
#scan slit start end step cam1 620 peak2d
#run "setupBimorphOptimisation"

import gridscan

print "Create ncdgridscan"
try:
       del(gridxy)
except:
       pass

gridxy=ScannableGroup()
gridxy.setName("gridxy")
gridxy.setGroupMembers([mfstage_x, mfstage_y])
gridxy.configure()
ncdgridscan=gridscan.Grid("Camera View", "Mapping Grid", mfgige, gridxy, ncddetectors)
ncdgridscan.snap()

import metadatatweaks
getTitle = metadatatweaks.getTitle
alias("getTitle")
setTitle = metadatatweaks.setTitle
alias("setTitle")
getVisit = metadatatweaks.getVisit
alias("getVisit")
setVisit = metadatatweaks.setVisit
alias("setVisit")
print "\n adding hotwaxs device"
# has GDA pos etc in it, so we need to "run"
#execfile("/dls/i22/scripts/commissioning/Marc/shutdown/hotwaxs.py")
run("/commissioning/Marc/shutdown/hotwaxs.py")
print "==================================================================="
