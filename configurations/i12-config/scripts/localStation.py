#    file: localStation.py
#
#    For beamline specific initialisation code
import sys	
from gdascripts.messages import handle_messages
from gda.jython.commands import GeneralCommands

print "Performing I12 specific initialisation code"
print "=============================================="

from gda.jython.commands.GeneralCommands import alias

print "add EPICS scripts to system path"
print "------------------------------------------------"
### add epics plugin scripts library path
from gda.util import PropertyUtils
from java.lang import System
_epicsScriptLibraryDir = PropertyUtils.getExistingDirFromLocalProperties("gda.install.git.loc") + "/gda-epics.git/uk.ac.gda.epics/scripts" + System.getProperty("file.separator");
sys.path.append(_epicsScriptLibraryDir)

import i12utilities
from i12utilities import DocumentationScannable
import lookupTables


print "create commands for folder operations: wd, pwd, nwd, nfn, cfn, setSubdirectory('subdir-name')"
print "-------------------------------------------------"
# function to find the last file path

from i12utilities import wd, pwd, nwd, nfn, cfn, setDataWriterToNexus, setDataWriterToSrs, getDataWriter, ls_scannables
alias("wd")
alias("pwd")
alias("nwd")
alias("nfn")
alias("cfn")
alias("setSubdirectory")


print "create commands for Data Writer operations: setDataWriterToNexus, setDataWriterToSrs, getDataWriter"
print "-------------------------------------------------"

alias("setDataWriterToNexus")
alias("setDataWriterToSrs")
alias("getDataWriter")

print "Command to find list all the scannables: ls_scannables"
print "-------------------------------------------------"
alias("ls_scannables")

print "Commands to reload lookup tables: reloadModuleLookup, reloadCameraMotionLookup, reloadTiltBallPositionLookup, reloadScanResolutionLookup"
from lookupTables import reloadModuleLookup, reloadCameraMotionLookup, reloadTiltBallPositionLookup, reloadScanResolutionLookup
alias("reloadModuleLookup")
alias("reloadCameraMotionLookup")
alias("reloadTiltBallPositionLookup")
alias("reloadScanResolutionLookup")


msg = "i12 Help\n======="
msg += "\nPCO Help - type 'help i12pco'"
msg += "\nPixium Help - type 'help i12pixium'"
msg += "\nEDXD Help - type 'help i12edxd'"
msg += "\n====="
i12 = DocumentationScannable("i12Help", msg, "http://confluence.diamond.ac.uk/display/I12Tech/I12+GDA+Help")
i12pco = DocumentationScannable("i12HelpPco", "Documentation for i12pco", "http://confluence.diamond.ac.uk/display/I12Tech/PCO+detector")
i12pixium = DocumentationScannable("i12HelpPixium", "Documentation for i12pixium", "http://confluence.diamond.ac.uk/display/I12Tech/Pixium+in+GDA")
i12edxd = DocumentationScannable("i12HelpEdxd", "Documentation for i12edxd", "http://confluence.diamond.ac.uk/display/I12Tech/EDXD%3A+Use+in+GDA")

# Do this last
#setSubdirectory("default")
print
print "-----------------------------------------------------------------------------------------------------------------"
print "Create an 'interruptable()' function which can be used to make for-loop interruptable in GDA."
print "    To use this, you must place 'interruptable()' call as the 1st or last line in your for-loop."
def interruptable():
    GeneralCommands.pause()
print
print "-----------------------------------------------------------------------------------------------------------------"
print "load EPICS Pseudo Device utilities for creating scannable object from a PV name."
from gdascripts.pd.epics_pds import * #@UnusedWildImport
print
print "-----------------------------------------------------------------------------------------------------------------"
print "load time utilities for creating timer objects."
from gdascripts.pd.time_pds import * #@UnusedWildImport
print
print "-----------------------------------------------------------------------------------------------------------------"
print "Load utilities: printJythonEnvironment(), caget(pv), caput(pv,value), attributes(object), "
print "    iterableprint(iterable), listprint(list), frange(start,end,step)"
from gdascripts.utils import * #@UnusedWildImport
print
print "-----------------------------------------------------------------------------------------------------------------"
print "load common physical constants"
from gdascripts.constants import * #@UnusedWildImport

from gda.configuration.properties import LocalProperties


# set up the reconmanager, however this should be moved into the Spring
#from uk.ac.gda.client.tomo import ReconManager
#rm = ReconManager()

# set up the extra scans
from init_scan_commands_and_processing import * #@UnusedWildImport
#scan_processor.rootNamespaceDict=globals()


from gda.scan.RepeatScan import create_repscan, repscan
vararg_alias("repscan")

from gdascripts.metadata.metadata_commands import setTitle
alias("setTitle")

if LocalProperties.check("gda.dummy.mode"):
    print "Running in dummy mode"

from gdascripts.pd.time_pds import waittimeClass2, showtimeClass, showincrementaltimeClass, actualTimeClass
waittime = waittimeClass2('waittime')
showtime = showtimeClass('showtime')
inctime = showincrementaltimeClass('inctime')
actualTime = actualTimeClass("actualTime")



try :
    print "setup edxd detector: edxd_counter, edxdout, edxd_binned"
    print "-------------------------------------------------"
    from edxd_count import edxd_count
    edxd_counter = edxd_count("edxd_counter", edxd) #@UndefinedVariable
    # set up the edxd to monitor to begin with
    edxd.monitorAllSpectra() #@UndefinedVariable
    print("After monitorAllSpectra")
    from EDXDDataExtractor import EDXDDataExtractor #@UnusedImport
    from EDXDDataExtractor import edxd2ascii
    from EDXDDataExtractor import postExtractor #@UnusedImport
    edxdout = edxd2ascii("edxdout")
    ## removing binned for the moment
    from edxd_binned_counter import EdxdBinned
    edxd_binned = EdxdBinned("edxd_binned", edxd) #@UndefinedVariable

    from edxd_q_calibration_reader import set_edxd_q_calibration
    print("After set_edxd_q_calibration")
    #epg 8 March 2011 Force changes to allow edxd to work on the trunk
    LocalProperties.set("gda.data.scan.datawriter.dataFormat", "NexusDataWriter")
    if LocalProperties.get("gda.data.scan.datawriter.dataFormat") != "NexusDataWriter":
        raise "Format not set to Nexus"
    edxd.setOutputFormat(["%5.5g", "%5.5g", "%5.5g", "%5.5g", "%5.5g"])
    
except :
	exceptionType, exception, traceback = sys.exc_info()
	handle_messages.log(None, "EDXD detector not available!", exceptionType, exception, traceback, False)

print "setup scan manager to control scan queue and their running"
print "-------------------------------------------------"
from manager_scan_functions import * #@UnusedWildImport

print "create 'topup' object"
print "-------------------------------------------------"
from topup_pause import TopupPause
topup = TopupPause("topup")

print "I12 specific commands: view <scannable>"
print "-------------------------------------------------"
def view(scannable): 
    for member in scannable.getGroupMembers() :
        print member.toFormattedString().replace('_', '.')

alias("view")

print "setup 'fastscan' object"
print "--------------------------------------------------"
from fast_scan import FastScan
fastscan = FastScan("fastscan");

print "setup 'sleeperWhileScan' object"
print "--------------------------------------------------"
from sleeperWhileScan import SleeperWhileScan
sleeper = SleeperWhileScan("sleeper");


print "Defines 'timer':"
print "--------------------------------------------------"
import timerelated 
timer = timerelated.TimeSinceScanStart("timer")

# tobias did this for the users at the end of run 3
from WaitLineDummy import WaitLineDummy
wld = WaitLineDummy("wld")

try :
    #create the PCO external object
    from pcoexternal import PCOext
    pcoext = PCOext(pco) #@UndefinedVariable
except :
    print "PCO external trigger not available"

from gdascripts.pd.time_pds import * #@UnusedWildImport
from gdascripts.pd.epics_pds import * #@UnusedWildImport
try:
    pixtimestamp = DisplayEpicsPVClass('pixtimestamp', 'BL12I-EA-DET-05:TIFF:TimeStamp_RBV', 's', '%.3f')
    pixtemperature = DisplayEpicsPVClass('pixtemperature', 'BL12I-EA-DET-05:TIFF:Temperature_RBV', 'degree', '%.3f') 
    pixtotalcount = DisplayEpicsPVClass('pixtotalcount', 'BL12I-EA-DET-05:STAT:Total_RBV', 'degree', '%d') 
    pixexposure = DisplayEpicsPVClass('pixexposure', 'BL12I-EA-DET-05:PIX:AcquireTime_RBV', 's', '%.3f') 
except:
    print "cannot create pixium timestamp and temperature scannables"
     
try:
    pcotimestamp = DisplayEpicsPVClass('pcotimestamp', 'TEST:TIFF0:TimeStamp_RBV', 's', '%.3f')    
except:
    print "cannot create PCO timestamp scannable"
try:
    loadcell = DisplayEpicsPVClass('loadcell', 'BL12I-EA-ADC-01:CH0', 's', '%.3g')
    adc01 = DisplayEpicsPVClass('adc01', 'BL12I-EA-ADC-01:CH1', 'V', '%.3g')
    adc02 = DisplayEpicsPVClass('adc02', 'BL12I-EA-ADC-01:CH2', 'V', '%.3g')
    adc03 = DisplayEpicsPVClass('adc03', 'BL12I-EA-ADC-01:CH3', 'V', '%.3g')
    adc04 = DisplayEpicsPVClass('adc04', 'BL12I-EA-ADC-01:CH4', 'V', '%.3g')
    adc05 = DisplayEpicsPVClass('adc05', 'BL12I-EA-ADC-01:CH5', 'V', '%.3g')
    adc06 = DisplayEpicsPVClass('adc06', 'BL12I-EA-ADC-01:CH6', 'V', '%.3g')
    adc07 = DisplayEpicsPVClass('adc07', 'BL12I-EA-ADC-01:CH7', 'V', '%.3g')

    HV_amp = EpicsReadWritePVClass('HV_amp', 'BL12I-EA-DAC-01:00', 'V', '%.3g')
    dac01 = EpicsReadWritePVClass('dac01', 'BL12I-EA-DAC-01:01', 'V', '%.3g')
    dac02 = EpicsReadWritePVClass('dac02', 'BL12I-EA-DAC-01:02', 'V', '%.3g')
    dac03 = EpicsReadWritePVClass('dac03', 'BL12I-EA-DAC-01:03', 'V', '%.3g')
    dac04 = EpicsReadWritePVClass('dac04', 'BL12I-EA-DAC-01:04', 'V', '%.3g')
    dac05 = EpicsReadWritePVClass('dac05', 'BL12I-EA-DAC-01:05', 'V', '%.3g')
    dac06 = EpicsReadWritePVClass('dac06', 'BL12I-EA-DAC-01:06', 'V', '%.3g')
    dac07 = EpicsReadWritePVClass('dac07', 'BL12I-EA-DAC-01:07', 'V', '%.3g')
    
    ttlout00 = EpicsReadWritePVClass('ttlout08','BL12I-EA-DIO-01:OUT:00','bool','%i')
    ttlout01 = EpicsReadWritePVClass('ttlout01','BL12I-EA-DIO-01:OUT:01','bool','%i')
    ttlout02 = EpicsReadWritePVClass('ttlout02','BL12I-EA-DIO-01:OUT:02','bool','%i')
    ttlout03 = EpicsReadWritePVClass('ttlout03','BL12I-EA-DIO-01:OUT:03','bool','%i')
    ttlout04 = EpicsReadWritePVClass('ttlout04','BL12I-EA-DIO-01:OUT:04','bool','%i')
    ttlout05 = EpicsReadWritePVClass('ttlout05','BL12I-EA-DIO-01:OUT:05','bool','%i')
    ttlout06 = EpicsReadWritePVClass('ttlout06','BL12I-EA-DIO-01:OUT:06','bool','%i')
    ttlout07 = EpicsReadWritePVClass('ttlout07','BL12I-EA-DIO-01:OUT:07','bool','%i')

    ttlin00 = DisplayEpicsPVClass('ttlin08','BL12I-EA-DIO-01:IN:00','bool','%i')
    ttlin01 = DisplayEpicsPVClass('ttlin01','BL12I-EA-DIO-01:IN:01','bool','%i')
    ttlin02 = DisplayEpicsPVClass('ttlin02','BL12I-EA-DIO-01:IN:02','bool','%i')
    ttlin03 = DisplayEpicsPVClass('ttlin03','BL12I-EA-DIO-01:IN:03','bool','%i')
    ttlin04 = DisplayEpicsPVClass('ttlin04','BL12I-EA-DIO-01:IN:04','bool','%i')  
    ttlin05 = DisplayEpicsPVClass('ttlin05','BL12I-EA-DIO-01:IN:05','bool','%i')
    ttlin06 = DisplayEpicsPVClass('ttlin06','BL12I-EA-DIO-01:IN:06','bool','%i')
    ttlin07 = DisplayEpicsPVClass('ttlin07','BL12I-EA-DIO-01:IN:07','bool','%i')  
    
except:
    print "cannot create loadcell or HV_amp scannables"
    
print
print "create ETL detector objects"
try:
    eh1therm1 = DisplayEpicsPVClass('eh1therm1', 'BL12I-OP-THERM-01:TEMP:T1', 'degree', '%.3f')
    eh1therm2 = DisplayEpicsPVClass('eh1therm2', 'BL12I-OP-THERM-01:TEMP:T2', 'degree', '%.3f')
    eh1therm3 = DisplayEpicsPVClass('eh1therm3', 'BL12I-OP-THERM-01:TEMP:T3', 'degree', '%.3f')
    eh1therm4 = DisplayEpicsPVClass('eh1therm4', 'BL12I-OP-THERM-01:TEMP:T4', 'degree', '%.3f')
    eh1therm5 = DisplayEpicsPVClass('eh1therm5', 'BL12I-OP-THERM-01:TEMP:T5', 'degree', '%.3f')
    eh1therm6 = DisplayEpicsPVClass('eh1therm6', 'BL12I-OP-THERM-01:TEMP:T6', 'degree', '%.3f')
except:
    print "cannot create thermocouple scannables"
try:
    eh2therm1 = DisplayEpicsPVClass('eh2therm1', 'BL12I-OP-THERM-02:TEMP:T1', 'degree', '%.3f')
    eh2therm2 = DisplayEpicsPVClass('eh2therm2', 'BL12I-OP-THERM-02:TEMP:T2', 'degree', '%.3f')
    eh2therm3 = DisplayEpicsPVClass('eh2therm3', 'BL12I-OP-THERM-02:TEMP:T3', 'degree', '%.3f')
    eh2therm4 = DisplayEpicsPVClass('eh2therm4', 'BL12I-OP-THERM-02:TEMP:T4', 'degree', '%.3f')
    eh2therm5 = DisplayEpicsPVClass('eh2therm5', 'BL12I-OP-THERM-02:TEMP:T5', 'degree', '%.3f')
    eh2therm6 = DisplayEpicsPVClass('eh2therm6', 'BL12I-OP-THERM-02:TEMP:T6', 'degree', '%.3f')
except:
    print "cannot create thermocouple scannables"
try:
    dac01_0 = EpicsReadWritePVClass('dac01_0', 'BL12I-EA-DAC-01:00', 'volt', '%.3f')
    dac01_1 = EpicsReadWritePVClass('dac01_1', 'BL12I-EA-DAC-01:01', 'volt', '%.3f')
    dac01_2 = EpicsReadWritePVClass('dac01_2', 'BL12I-EA-DAC-01:02', 'volt', '%.3f')
    dac01_3 = EpicsReadWritePVClass('dac01_3', 'BL12I-EA-DAC-01:03', 'volt', '%.3f')
    dac01_4 = EpicsReadWritePVClass('dac01_4', 'BL12I-EA-DAC-01:04', 'volt', '%.3f')
    dac01_5 = EpicsReadWritePVClass('dac01_5', 'BL12I-EA-DAC-01:05', 'volt', '%.3f')
    dac01_6 = EpicsReadWritePVClass('dac01_6', 'BL12I-EA-DAC-01:06', 'volt', '%.3f')
    dac01_7 = EpicsReadWritePVClass('dac01_7', 'BL12I-EA-DAC-01:07', 'volt', '%.3f')
except:
    print "cannot create DAC scannables"
try:
    dac03_0 = EpicsReadWritePVClass('dac03_0', 'BL12I-EA-DAC-03:00', 'volt', '%.3f')
    dac03_1 = EpicsReadWritePVClass('dac03_1', 'BL12I-EA-DAC-03:01', 'volt', '%.3f')
    dac03_2 = EpicsReadWritePVClass('dac03_2', 'BL12I-EA-DAC-03:02', 'volt', '%.3f')
    dac03_3 = EpicsReadWritePVClass('dac03_3', 'BL12I-EA-DAC-03:03', 'volt', '%.3f')
    dac03_4 = EpicsReadWritePVClass('dac03_4', 'BL12I-EA-DAC-03:04', 'volt', '%.3f')
    dac03_5 = EpicsReadWritePVClass('dac03_5', 'BL12I-EA-DAC-03:05', 'volt', '%.3f')
    dac03_6 = EpicsReadWritePVClass('dac03_6', 'BL12I-EA-DAC-03:06', 'volt', '%.3f')
    dac03_7 = EpicsReadWritePVClass('dac03_7', 'BL12I-EA-DAC-03:07', 'volt', '%.3f')
except:
    print "cannot create DAC scannables"
print "--------------------------------------------------"
pdnames = []
from detector_control_pds import * #@UnusedWildImport

for pd in pds:
    pdnames.append(str(pd.getName()))
    
print "available Detector objects are:"
print pdnames
print [(str(pd.getName()), pd.getTargetPosition(), pd.getPosition()) for pd in pds]
print
print "create Long Count Time Scaler objects:"
print "---------------------------------------------------"
from long_count_time_scaler_pds import I0oh2l, I0eh1l, I0eh2l
print I0oh2l.getName(), I0eh1l.getName(), I0eh2l.getName()
print
print "create rocking motion objects:"
print "---------------------------------------------------"
from rockingMotion_class import RockingMotion #@UnresolvedImport
rocktheta = RockingMotion("rocktheta", ss1.theta, -1, 1) #@UndefinedVariable
print rocktheta.getName()

from positionCompareMotorClass import PositionCompareMotorClass
ss2x = PositionCompareMotorClass("ss2x", "BL12I-MO-TAB-06:X.VAL", "BL12I-MO-TAB-06:X.RBV", "BL12I-MO-TAB-06:X.STOP", 0.002, "mm", "%.3f")
ss2y = PositionCompareMotorClass("ss2y", "BL12I-MO-TAB-06:Y.VAL", "BL12I-MO-TAB-06:Y.RBV", "BL12I-MO-TAB-06:Y.STOP", 0.002, "mm", "%.3f")
ss2z = PositionCompareMotorClass("ss2z", "BL12I-MO-TAB-06:Z.VAL", "BL12I-MO-TAB-06:Z.RBV", "BL12I-MO-TAB-06:Z.STOP", 0.002, "mm", "%.3f")
ss2rx = PositionCompareMotorClass("ss2rx", "BL12I-MO-TAB-06:PITCH.VAL", "BL12I-MO-TAB-06:PITCH.RBV", "BL12I-MO-TAB-06:PITCH.STOP", 0.002, "deg", "%.3f")
ss2ry = PositionCompareMotorClass("ss2ry", "BL12I-MO-TAB-06:THETA.VAL", "BL12I-MO-TAB-06:THETA.RBV", "BL12I-MO-TAB-06:THETA.STOP", 0.002, "deg", "%.3f")

pco.setHdfFormat(False) #@UndefinedVariable

#EPG - 8 March 2011 - Hack to force Nexus for edxd
#pixium.setSRSFormat() #@UndefinedVariable
pco.setExternalTriggered(True) #@UndefinedVariable

print "create 'eurotherm1' and 'eurotherm2'" 
eurotherm1temp = DisplayEpicsPVClass('eurotherm1', 'BL12I-EA-FURN-01:PV:RBV', 'c', '%.3f')
eurotherm2temp = DisplayEpicsPVClass('eurotherm2', 'BL12I-EA-FURN-02:PV:RBV', 'c', '%.3f')


print "create linkam"
linkamRampStatus = DisplayEpicsPVClass('linkamRampStatus','BL12I-CS-TEMPC-01:STATUS','bool','%i')
linkamRampControl = EpicsReadWritePVClass('linkamRampControl', 'BL12I-CS-TEMPC-01:RAMP:CTRL:SET', '', '%.3g')
linkamRampRate = EpicsReadWritePVClass('linkamRampRate', 'BL12I-CS-TEMPC-01:RAMP:RATE:SET', 'deg/min', '%.3g')
linkamRampLimit = EpicsReadWritePVClass('linkamRampLimit', 'BL12I-CS-TEMPC-01:RAMP:LIMIT:SET', 'deg', '%.3g')
linkamTemp = DisplayEpicsPVClass('linkamTemp','BL12I-CS-TEMPC-01:TEMP','degrees','%.3g')


from tomographyScan import tomoScan, reportJythonNamespaceMapping #@UnusedImport
alias("reportJythonNamespaceMapping")

try:
    from tomo import tomoAlignment #@UnusedImport
except:
    print "Unable to import 'tomoAlignment'"
#print
#print "setup tomographyScan:"
#from tomo import tomographyScan
#run("tomo/tomographyScan.py")

#from pv_scannable_utils import *
#print "added pv_scannable_utils" 

from PixiumAfterIOCStart_ModeChange import pixiumExp80ms, pixiumExp500ms, pixiumExp1000ms,pixiumExp2000ms, pixiumExp4000ms,pixiumAfterIOCStart
alias("pixiumExp80ms")
alias("pixiumExp500ms")
alias("pixiumExp1000ms")
alias("pixiumExp2000ms")
alias("pixiumExp4000ms")
alias("pixiumAfterIOCStart")

try:
    print "\n Add default scannables:"
    default_scannables = []
    default_scannables.append(ring_topup_countdown)
    default_scannables.append(actualTime)
    
    for s in default_scannables:
        add_default s
except:
    print "Unable to add default scannables"

print 
print "==================================================="
print "local station initialisation completed."
