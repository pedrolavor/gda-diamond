# localStation.py
# For beamline specific initialisation code.
#
print "===================================================================";
print "Performing beamline specific initialisation code (i05-1).";
print

print "Importing generic features...";
import java
from gda.configuration.properties import LocalProperties
from gda.device.scannable.scannablegroup import ScannableGroup
from time import sleep, localtime
from gda.jython.commands.GeneralCommands import alias
from gdascripts.pd.time_pds import actualTimeClass

# Get the location of the GDA beamline script directory
gdaScriptDir = LocalProperties.get("gda.config") + "/scripts/"
gdascripts = LocalProperties.get("gda.install.git.loc") + "/gda-core.git/uk.ac.gda.core/scripts/gdascripts/"

execfile(gdaScriptDir + "/installStandardScansWithProcessing.py");

execfile(gdascripts + "/pd/epics_pds.py");
execfile(gdascripts + "/pd/dummy_pds.py");
execfile(gdascripts + "/pd/time_pds.py");

execfile(gdascripts + "/utils.py");

print "Creating beamline specific devices...";

import metadatatweaks
getSubdirectory = metadatatweaks.getSubdirectory
alias("getSubdirectory")
setSubdirectory = metadatatweaks.setSubdirectory
alias("setSubdirectory")
getVisit = metadatatweaks.getVisit
alias("getVisit")
setVisit = metadatatweaks.setVisit
alias("setVisit")
sample_name = metadatatweaks.SampleNameScannable("sample_name", "samplename")

from arpesmonitor import ARPESMonitor
am = ARPESMonitor()
centre_energy = analyser.getCentreEnergyScannable()
centre_energy.setName("centre_energy")
centre_energy.setInputNames(["centre_energy"])

# Enable callbacks on ARR1 to allow updating of detector plot
caput("BL05J-EA-DET-01:ARR:EnableCallbacks",1)

import arpes

# Sample stage script for easy and safe movement of the stage to predefined positions
execfile(gdaScriptDir + "/sampleStage.py")

print "==================================================================="
if LocalProperties.get("gda.mode") == "live":  # don't execute in squish tests
   print "Running i05-1 scripts."
   run "beamline/masterj.py"
print "==================================================================="
