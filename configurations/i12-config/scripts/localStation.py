#    file: localStation.py
#
#    For beamline specific initialisation code
import sys	
from gdascripts.messages import handle_messages
from gda.jython.commands import GeneralCommands

print "Performing I12 specific initialisation code"
print "=============================================="

from gda.jython.commands.GeneralCommands import alias, vararg_alias

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

#from beamEnergy import setEnergy
#alias("setEnergy")

#from detectorModeSwitching import moveToImagingMode, moveToDiffractionMode
#alias("moveToImagingMode")
#alias("moveToDiffractionMode")

print "create commands for folder operations: wd, pwd, nwd, nfn, cfn, setSubdirectory('subdir-name')"
print "-------------------------------------------------"
# function to find the last file path

from i12utilities import wd, pwd, nwd, nfn, cfn, setSubdirectory, setDataWriterToNexus, setDataWriterToSrs, getDataWriter, ls_scannables
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

import i12info

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

from gdascripts.metadata.metadata_commands import setTitle, getTitle
alias("setTitle")
alias("getTitle")

finder = Finder.getInstance() 

print "setup meta-data provider"
from gdascripts.metadata.metadata_commands import meta_add, meta_ll, meta_ls, meta_rm
alias("meta_add")
alias("meta_ll")
alias("meta_ls")
alias("meta_rm")
from gda.data.scan.datawriter import NexusDataWriter
LocalProperties.set(NexusDataWriter.GDA_NEXUS_METADATAPROVIDER_NAME,"metashop")

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
    ttlout01_1 = EpicsReadWritePVClass('ttlout01_1','BL12I-EA-DIO-01:OUT:00','bool','%i') #labelled according to RACK names, not EPICS
    ttlout01_2 = EpicsReadWritePVClass('ttlout01_2','BL12I-EA-DIO-01:OUT:01','bool','%i')
    ttlout01_3 = EpicsReadWritePVClass('ttlout01_3','BL12I-EA-DIO-01:OUT:02','bool','%i')
    ttlout01_4 = EpicsReadWritePVClass('ttlout01_4','BL12I-EA-DIO-01:OUT:03','bool','%i')
    ttlout01_5 = EpicsReadWritePVClass('ttlout01_5','BL12I-EA-DIO-01:OUT:04','bool','%i')
    ttlout01_6 = EpicsReadWritePVClass('ttlout01_6','BL12I-EA-DIO-01:OUT:05','bool','%i')
    ttlout01_7 = EpicsReadWritePVClass('ttlout01_7','BL12I-EA-DIO-01:OUT:06','bool','%i')
    ttlout01_8 = EpicsReadWritePVClass('ttlout01_8','BL12I-EA-DIO-01:OUT:07','bool','%i')

    ttlin01_1 = DisplayEpicsPVClass('ttlin01_1','BL12I-EA-DIO-01:IN:00','bool','%i')
    ttlin01_2 = DisplayEpicsPVClass('ttlin01_2','BL12I-EA-DIO-01:IN:01','bool','%i')
    ttlin01_3 = DisplayEpicsPVClass('ttlin01_3','BL12I-EA-DIO-01:IN:02','bool','%i')
    ttlin01_4 = DisplayEpicsPVClass('ttlin01_4','BL12I-EA-DIO-01:IN:03','bool','%i')
    ttlin01_5 = DisplayEpicsPVClass('ttlin01_5','BL12I-EA-DIO-01:IN:04','bool','%i')  
    ttlin01_6 = DisplayEpicsPVClass('ttlin01_6','BL12I-EA-DIO-01:IN:05','bool','%i')
    ttlin01_7 = DisplayEpicsPVClass('ttlin01_7','BL12I-EA-DIO-01:IN:06','bool','%i')
    ttlin01_8 = DisplayEpicsPVClass('ttlin01_7','BL12I-EA-DIO-01:IN:07','bool','%i')
    
    adc01_1 = DisplayEpicsPVClass('adc01_1', 'BL12I-EA-ADC-01:CH0', 'V', '%.3g') #labelled according to RACK names, not EPICS
    adc01_2 = DisplayEpicsPVClass('adc01_2', 'BL12I-EA-ADC-01:CH1', 'V', '%.3g')
    adc01_3 = DisplayEpicsPVClass('adc01_3', 'BL12I-EA-ADC-01:CH2', 'V', '%.3g')
    adc01_4 = DisplayEpicsPVClass('adc01_4', 'BL12I-EA-ADC-01:CH3', 'V', '%.3g')
    adc01_5 = DisplayEpicsPVClass('adc01_5', 'BL12I-EA-ADC-01:CH4', 'V', '%.3g')
    adc01_6 = DisplayEpicsPVClass('adc01_6', 'BL12I-EA-ADC-01:CH5', 'V', '%.3g')
    adc01_7 = DisplayEpicsPVClass('adc01_7', 'BL12I-EA-ADC-01:CH6', 'V', '%.3g')
    adc01_8 = DisplayEpicsPVClass('adc01_8', 'BL12I-EA-ADC-01:CH7', 'V', '%.3g')

    adc02_1 = DisplayEpicsPVClass('adc02_1', 'BL12I-EA-ADC-02:CH0', 'V', '%.3g') #labelled according to RACK names, not EPICS
    adc02_2 = DisplayEpicsPVClass('adc02_2', 'BL12I-EA-ADC-02:CH1', 'V', '%.3g')
    adc02_3 = DisplayEpicsPVClass('adc02_3', 'BL12I-EA-ADC-02:CH2', 'V', '%.3g')
    adc02_4 = DisplayEpicsPVClass('adc02_4', 'BL12I-EA-ADC-02:CH3', 'V', '%.3g')
    adc02_5 = DisplayEpicsPVClass('adc02_5', 'BL12I-EA-ADC-02:CH4', 'V', '%.3g')
    adc02_6 = DisplayEpicsPVClass('adc02_6', 'BL12I-EA-ADC-02:CH5', 'V', '%.3g')
    adc02_7 = DisplayEpicsPVClass('adc02_7', 'BL12I-EA-ADC-02:CH6', 'V', '%.3g')
    adc02_8 = DisplayEpicsPVClass('adc02_8', 'BL12I-EA-ADC-02:CH7', 'V', '%.3g')
    
    dac01_1 = EpicsReadWritePVClass('dac01_1', 'BL12I-EA-DAC-01:00', 'volt', '%.3f') #labelled according to RACK names, not EPICS
    dac01_2 = EpicsReadWritePVClass('dac01_2', 'BL12I-EA-DAC-01:01', 'volt', '%.3f')
    dac01_3 = EpicsReadWritePVClass('dac01_3', 'BL12I-EA-DAC-01:02', 'volt', '%.3f')
    dac01_4 = EpicsReadWritePVClass('dac01_4', 'BL12I-EA-DAC-01:03', 'volt', '%.3f')
    dac01_5 = EpicsReadWritePVClass('dac01_5', 'BL12I-EA-DAC-01:04', 'volt', '%.3f')
    dac01_6 = EpicsReadWritePVClass('dac01_6', 'BL12I-EA-DAC-01:05', 'volt', '%.3f')
    dac01_7 = EpicsReadWritePVClass('dac01_7', 'BL12I-EA-DAC-01:06', 'volt', '%.3f')
    dac01_8 = EpicsReadWritePVClass('dac01_8', 'BL12I-EA-DAC-01:07', 'volt', '%.3f')  
except:
    print "cannot create EH1 ACD/DAC scannables"      
      
    
try:
    ttlout02_1 = EpicsReadWritePVClass('ttlout02_1','BL12I-EA-DIO-02:OUT:00','bool','%i') #labelled according to RACK names, not EPICS
    ttlout02_2 = EpicsReadWritePVClass('ttlout02_2','BL12I-EA-DIO-02:OUT:01','bool','%i')
    ttlout02_3 = EpicsReadWritePVClass('ttlout02_3','BL12I-EA-DIO-02:OUT:02','bool','%i')
    ttlout02_4 = EpicsReadWritePVClass('ttlout02_4','BL12I-EA-DIO-02:OUT:03','bool','%i')
    ttlout02_5 = EpicsReadWritePVClass('ttlout02_5','BL12I-EA-DIO-02:OUT:04','bool','%i')
    ttlout02_6 = EpicsReadWritePVClass('ttlout02_6','BL12I-EA-DIO-02:OUT:05','bool','%i')
    ttlout02_7 = EpicsReadWritePVClass('ttlout02_7','BL12I-EA-DIO-02:OUT:06','bool','%i')
    ttlout02_8 = EpicsReadWritePVClass('ttlout02_8','BL12I-EA-DIO-02:OUT:07','bool','%i')
    
    dac03_1 = EpicsReadWritePVClass('dac03_1', 'BL12I-EA-DAC-03:00', 'volt', '%.3f') #labelled according to RACK names, not EPICS
    dac03_2 = EpicsReadWritePVClass('dac03_2', 'BL12I-EA-DAC-03:01', 'volt', '%.3f')
    dac03_3 = EpicsReadWritePVClass('dac03_3', 'BL12I-EA-DAC-03:02', 'volt', '%.3f')
    dac03_4 = EpicsReadWritePVClass('dac03_4', 'BL12I-EA-DAC-03:03', 'volt', '%.3f')
    dac03_5 = EpicsReadWritePVClass('dac03_5', 'BL12I-EA-DAC-03:04', 'volt', '%.3f')
    dac03_6 = EpicsReadWritePVClass('dac03_6', 'BL12I-EA-DAC-03:05', 'volt', '%.3f')
    dac03_7 = EpicsReadWritePVClass('dac03_7', 'BL12I-EA-DAC-03:06', 'volt', '%.3f')
    dac03_8 = EpicsReadWritePVClass('dac03_8', 'BL12I-EA-DAC-03:07', 'volt', '%.3f')

    adc03_1 = DisplayEpicsPVClass('adc03_1', 'BL12I-EA-ADC-03:CH0', 'V', '%.3g') #labelled according to RACK names, not EPICS
    adc03_2 = DisplayEpicsPVClass('adc03_2', 'BL12I-EA-ADC-03:CH1', 'V', '%.3g')
    adc03_3 = DisplayEpicsPVClass('adc03_3', 'BL12I-EA-ADC-03:CH2', 'V', '%.3g')
    adc03_4 = DisplayEpicsPVClass('adc03_4', 'BL12I-EA-ADC-03:CH3', 'V', '%.3g')
    adc03_5 = DisplayEpicsPVClass('adc03_5', 'BL12I-EA-ADC-03:CH4', 'V', '%.3g')
    adc03_6 = DisplayEpicsPVClass('adc03_6', 'BL12I-EA-ADC-03:CH5', 'V', '%.3g')
    adc03_7 = DisplayEpicsPVClass('adc03_7', 'BL12I-EA-ADC-03:CH6', 'V', '%.3g')
    adc03_8 = DisplayEpicsPVClass('adc03_8', 'BL12I-EA-ADC-03:CH7', 'V', '%.3g')
   
except:
    print "cannot create EH2 ADC/DAC scannables"
    
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
#rocktheta = RockingMotion("rocktheta", ss1.theta, -1, 1) #@UndefinedVariable
#print rocktheta.getName()

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

import tomographyScan
from tomographyScan import tomoScan, reportJythonNamespaceMapping, reportTomo  #@UnusedImport
alias("reportJythonNamespaceMapping")
alias("reportTomo")

tomography_additional_scannables=[]
#try:
#    tomography_additional_scannables.append(p2r_force)
#    tomography_additional_scannables.append(p2r_y)
#except:
#    print "Unable to append p2r scannables to tomography_additional_scannables"

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

print "adding mass flow controller scannables"
try:
    mfc_pressure = DisplayEpicsPVClass('mfc_pressure', 'ME08G-EA-GIR-01:MFC2:PBAR:RD', 'bar', '%5.3g')
    mfc_temperature = DisplayEpicsPVClass('mfc_temperature', 'ME08G-EA-GIR-01:MFC2:TEMP:RD', 'C', '%5.3g')
    mfc_volumetric_flow = DisplayEpicsPVClass('mfc_volumetric_flow', 'ME08G-EA-GIR-01:MFC2:VOL:FLOW:RD', 'CCM', '%5.3g')
except:
    print "cannot create mass flow controller scannables"
    

from PixiumAfterIOCStart_ModeChange import pixiumExp80ms, pixiumExp500ms, pixiumExp1000ms,pixiumExp2000ms, pixiumExp4000ms,pixiumAfterIOCStart
alias("pixiumExp80ms")
alias("pixiumExp500ms")
alias("pixiumExp1000ms")
alias("pixiumExp2000ms")
alias("pixiumExp4000ms")
alias("pixiumAfterIOCStart")


from i12utilities import includeEarlyFrames, excludeEarlyFrames, reportEarlyFrames, setBaseExposureTime, getBaseExposureTime, setBaseAcquisitionTime, getBaseAcquisitionTime, setPUMode, getPUMode, setExposuresPerImage, getExposuresPerImage, pixCalibrate 
alias("includeEarlyFrames")
alias("excludeEarlyFrames")
alias("reportEarlyFrames")
alias("setBaseExposureTime")
alias("getBaseExposureTime")
alias("setBaseAcquisitionTime")
alias("getBaseAcquisitionTime")
alias("setPUMode")
alias("getPUMode")
alias("setExposuresPerImage")
alias("getExposuresPerImage")
alias("pixCalibrate") 

try:
    print "\n Adding default scannables"
    default_scannables = []
    default_scannables.append(ring)
    default_scannables.append(actualTime)
    #default_scannables.append(I0eh1)
    #default_scannables.append(I0eh1l)
    #default_scannables.append(I0eh2)
    #default_scannables.append(I0eh2l)
    #default_scannables.append(I0oh2l)
    
    for s in default_scannables:
        add_default(s)
except:
    exceptionType, exception, traceback = sys.exc_info()
    msg = "Unable to add default scannables: "
    handle_messages.log(None, msg, exceptionType, exception, traceback, False)

try:
    print "\n Adding meta (before-scan) scannables"
    meta_scannables = []
    meta_scannables.append(cam1)
    #meta_scannables.append(cam3)
    
    meta_scannables.append(f2)
    meta_scannables.append(f3)
    meta_scannables.append(f4)
    
    meta_scannables.append(mc1_bragg)
    meta_scannables.append(mc2)
    
    #meta_scannables.append(s1)
    #meta_scannables.append(s2)
    #meta_scannables.append(s3)
    
    meta_scannables.append(t3)
    meta_scannables.append(t7)
    
    for s in meta_scannables:
        meta_add(s)
    
    msg = meta_ls()
    print msg
except:
    exceptionType, exception, traceback = sys.exc_info()
    msg = "Unable to add meta (before-scan) scannables: "
    handle_messages.log(None, msg, exceptionType, exception, traceback, False)

import os
def stress12(exposureTime=1.0,startAng=0.0, stopAng=180.0, stepAng=0.05, subDir=None, loopNum=1):
    """
    Function to collect a tomogram for stress test on i12
    Arguments:
    exposureTime - exposure time in seconds (default = 1.0)
    startAng - first rotation angle (default=0.0)
    stopAng  - last rotation angle (default=180.0)
    stepAng - rotation step size (default = 0.05)
    subDir - name of the sub-directory of the visit/tmp directory to be used for saving out images 
            (default = None, in which case data go to /dls/i12/data/yyyy/visitID/tmp/)
    loopNum - total number of scans to be run (default = 1)
    """
    print "Entering stress12"
    sub = "tmp"
    if subDir is not None:
        sub += os.sep + subDir
    setSubdirectory(sub)
    msg = pwd()
    print "Saving data in: " + msg
    for i in range(0, loopNum):
        print "scan index : %i" %(i) 
        tomoScan("stress12", ss1_x_dummy(), ss1_x_dummy(), exposureTime, startAng, stopAng, stepAng, darkFieldInterval=0, flatFieldInterval=0, imagesPerDark=0, imagesPerFlat=0, optimizeBeamInterval=0, pattern='default', tomoRotationAxis=0, addNXEntry=True, autoAnalyse=False, additionalScannables=[])
    print "Finished stress12"

print 
print "==================================================="
print "local station initialisation completed."
