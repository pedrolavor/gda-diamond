import sys
import installation

from gdascripts.messages.handle_messages import simpleLog
from gdascripts.scannable.dummy import SingleInputDummy
from gda.device.scannable.scannablegroup import ScannableGroup

from gdascripts.degas.degas import Degas  # @UnusedImport

from gda.jython.commands.GeneralCommands import alias
from time import sleep  # @UnusedImport

from calibration.Energy_class import BeamEnergy
from gda.jython.commands import GeneralCommands
from gdaserver import lakeshore, b2, x
import gdascripts
from utils.ExceptionLogs import localStation_exception

print "-----------------------------------------------------------------------------------------------------------------"
print "Set scan returns to the original positions on completion to false (0); default is 0."
print "   To set scan returns to its start positions on completion please do:"
print "      >>>scansReturnToOriginalPositions=1"
scansReturnToOriginalPositions=0;
print
print sys.path
print
# set up a nice method for getting the latest file path
from i21commands.dirFileCommands import pwd, lwf, nwf, nfn, setSubdirectory, getSubdirectory  # @UnusedImport
alias("pwd")
alias("lwf")
alias("nwf")
alias("nfn")
print
from plottings.configScanPlot import setYFieldVisibleInScanPlot,getYFieldVisibleInScanPlot,setXFieldInScanPlot,useSeparateYAxes,useSingleYAxis  # @UnusedImport
alias("useSeparateYAxes")
alias("useSingleYAxis")
print
def interruptable():
    GeneralCommands.pause()
alias("interruptable")
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
print
print "-----------------------------------------------------------------------------------------------------------------"
print "Adding timer devices t, dt, and w, clock"
from gdascripts.scannable.timerelated import timerelated #@UnusedImport
print "-----------------------------------------------------------------------------------------------------------------"
print "Adding timer devices t, dt, and w, clock"
print "Adding dummy devices dummies.x, dummies.y and dummies.z"
dummies = ScannableGroup()
dummies.setName("dummies")
dummies.setGroupMembers([SingleInputDummy("x"), SingleInputDummy("y"), SingleInputDummy("z")])

print
simpleLog("================ INITIALISING I21 GDA ================")

if installation.isLive():
    print "Running in live mode"
    print "create camera total count scannables: d1camtotal, d2camtotal, d3acamtotal, d4camtotal, smpcam1total,smpcam2total,smpcam3total, smpcam4total"
    d1camtotal=DisplayEpicsPVClass('d1camtotal', 'BL21I-DI-DCAM-01:STAT:Total_RBV', 'counts', '%10d')
    d2camtotal=DisplayEpicsPVClass('d2camtotal', 'BL21I-DI-DCAM-02:STAT:Total_RBV', 'counts', '%10d')
    d3acamtotal=DisplayEpicsPVClass('d3acamtotal', 'BL21I-DI-DCAM-03:STAT:Total_RBV', 'counts', '%10d')
    d4camtotal=DisplayEpicsPVClass('d4camtotal', 'BL21I-DI-DCAM-04:STAT:Total_RBV', 'counts', '%10d')
    d8camtotal=DisplayEpicsPVClass('d8camtotal', 'BL21I-DI-DCAM-24:STAT:Total_RBV', 'counts', '%10d')
    smpcam1total=DisplayEpicsPVClass('smpcam1total', 'BL21I-DI-DCAM-20:STAT1:Total_RBV', 'counts', '%10d')
    smpcam2total=DisplayEpicsPVClass('smpcam2total', 'BL21I-DI-DCAM-21:STAT1:Total_RBV', 'counts', '%10d')
    smpcam3total=DisplayEpicsPVClass('smpcam3total', 'BL21I-DI-DCAM-22:STAT1:Total_RBV', 'counts', '%10d')
    smpcam4total=DisplayEpicsPVClass('smpcam4total', 'BL21I-DI-DCAM-23:STAT1:Total_RBV', 'counts', '%10d')
    s5camtotal=DisplayEpicsPVClass('s5camtotal', 'BL21I-DI-DCAM-55:STAT:Total_RBV', 'counts', '%10d')
    andortotal=DisplayEpicsPVClass('andortotal', 'BL21I-EA-DET-01:STAT:Total_RBV', 'counts', '%10d')

    from epics_scripts.pv_scannable_utils import createPVScannable
    pgmMirrorPitch_UserOffset = createPVScannable('pgmMirrorPitch_UserOffset', 'BL21I-OP-PGM-01:MIR:PITCH.OFF')
    pgmGratingPitch_UserOffset = createPVScannable('pgmGratingPitch_UserOffset', 'BL21I-OP-PGM-01:GRT:PITCH.OFF')
    
    from scannabledevices.feedbackScannable import FeedbackScannable, FeedbackOffScannable
    fbs=FeedbackScannable("fbs", pvroot="BL21I-OP-MIRR-01:FBCTRL")
    fboff=FeedbackOffScannable("fboff", pvroot="BL21I-OP-MIRR-01:FBCTRL")
    
    #fast shutter source control
    def erio():
        caput("BL21I-OP-SHTR-01:SRC", 0)
    
    def primary():
        caput("BL21I-OP-SHTR-01:SRC", 1)
    
    def polarimeter():
        caput("BL21I-OP-SHTR-01:SRC", 2)
        
    alias("erio")
    alias("primary")
    alias("polarimeter")
else:
    print "Running in dummy mode"

print "create clever amplifier scannables: cleverd7femto1, cleverd7femto2"
from i21_utils import DisplayEpicsPVClass_neg, DisplayEpicsPVClass_pos
d7femto1_neg = DisplayEpicsPVClass_neg('d7femto1_neg', d7femto1)  # @UndefinedVariable
d7femto2_pos = DisplayEpicsPVClass_pos('d7femto2_pos', d7femto2)  # @UndefinedVariable

from scannabledevices.cleverAmplifier import CleverAmplifier
cleverd7femto1=CleverAmplifier("cleverd7femto1", d7femto1_neg, 0.5, 9.0, "%.4f", "%.4e")  # @UndefinedVariable
cleverd7femto2=CleverAmplifier("cleverd7femto2", d7femto2_pos, 0.5, 9.0, "%.4f", "%.4e")  # @UndefinedVariable
cleverm4femto1=CleverAmplifier("cleverm4femto1", m4femto1, 0.5, 9.0, "%.4f", "%.4e")  # @UndefinedVariable
cleverm4femto2=CleverAmplifier("cleverm4femto2", m4femto2, 0.5, 9.0, "%.4f", "%.4e")  # @UndefinedVariable
clevertthdiode=CleverAmplifier("clevertthdiode", tthdiode, 0.5, 9.0, "%.4f", "%.4e")  # @UndefinedVariable

print
print "-----------------------------------------------------------------------------------------------------------------"
print "Create an 'dummyenergy' scannable which can be used for test energy scan in GDA. It moves dummy motor 'dummies.x' and 'dummies.y'"
dummyenergy=BeamEnergy("dummyenergy",idscannable, dummies.x, dummies.y,pgmGratingSelect)  # @UndefinedVariable
print "Create an 'energy' scannable which can be used for energy scan in GDA. It moves both ID gap and PGM energy"
energy=BeamEnergy("energy",idscannable, idgap, pgmEnergy, pgmGratingSelect)  # @UndefinedVariable

# LH,LV,CR,CL,LAN,LAP=["LH","LV","CR","CL","LAN","LAP"]
# from lookup.IDLookup import IDLookup4LinearAngleMode
# from calibration.energy_polarisation_class import BeamEnergyPolarisationClass
# lookup_file='/dls_sw/i09-2/software/gda/config/lookupTables/LinearAngle.csv' #to be replaced by i09-2's own data
# 
# idlamlookup=IDLookup4LinearAngleMode("idlamlookup", lut=lookup_file) 
# energy=BeamEnergyPolarisationClass("energy", jidscannable, pgmenergy,idlamlookup, lut="JIDEnergy2GapCalibrations.txt", polarisationConstant=True)  # @UndefinedVariable
# energy.configure()
# polarisation=BeamEnergyPolarisationClass("polarisation", jidscannable, pgmenergy,idlamlookup, lut="JIDEnergy2GapCalibrations.txt", energyConstant=True)  # @UndefinedVariable
# polarisation.configure()
# energypolarisation=BeamEnergyPolarisationClass("energypolarisation", jidscannable, pgmenergy,idlamlookup, lut="JIDEnergy2GapCalibrations.txt")  # @UndefinedVariable
# energypolarisation.configure()
# energypolarisation.setInputNames(["energy"])
# energypolarisation.setExtraNames(["polarisation"])

from scannabledevices.coupledSampleStageMotion import CoupledSampleStageMotion
sapara=CoupledSampleStageMotion("sapara", x, y, th) # @UndefinedVariable
saperp=CoupledSampleStageMotion("saperp", x, y, th) # @UndefinedVariable

print "-"*80
print "Creating sample temperature aliases: tsample, tshield, tcryostat"
tsample=lakeshore.getTemperature(0)  # @UndefinedVariable
tshield=lakeshore.getTemperature(1)
tcryostat=lakeshore.getTemperature(2)

def input_tsample():
    lakeshore.setInput(1)
    
def input_tshield():
    lakeshore.setInput(2)
    
def input_tcryostat():
    lakeshore.setInput(3)
    
alias("input_tsample")
alias("input_tshield")
alias("input_tcryostat")
print
print "-----------------------------------------------------------------------------------------------------------------"
print "setup meta-data provider commands: meta_add, meta_ll, meta_ls, meta_rm "
from metashop import *  # @UnusedWildImport
import metashop  # @UnusedImport
print
print "-----------------------------------------------------------------------------------------------------------------"
print "Add meta data items to be captured in data files."
metadatalist=[idgap, idscannable, energy] #@UndefinedVariable
m1list=[m1x,m1pitch,m1finepitch,m1height,m1yaw,m1roll,m1feedback] #@UndefinedVariable
m2list=[m2x,m2pitch,m2finepitch,m2height,m2feedback]# @UndefinedVariable
m4list=[m4x,m4y,m4z,m4rx,m4ry,m4rz,m4longy,m4femto1,m4femto2]  # @UndefinedVariable
m5list=[m5hqx,m5hqy,m5hqz,m5hqrx,m5hqry,m5hqrz,m5lqx,m5lqy,m5lqz,m5lqrx,m5lqry,m5lqrz,m5longy,m5tth]  # @UndefinedVariable
pgmlist=[pgmEnergy, pgmGratingSelectReal,pgmMirrorSelectReal,pgmMirrorPitch,pgmGratingPitch,cff, pgmB2Shadow]  # @UndefinedVariable
s1list=[s1hsize,s1vsize,s1hcentre,s1vcentre] #@UndefinedVariable
s2list=[s2hsize,s2vsize,s2hcentre,s2vcentre] #@UndefinedVariable
s3list=[s3hsize,s3vsize,s3hcentre,s3vcentre] #@UndefinedVariable
s4list=[s4hcentre,s4hsize,s4vcentre,s4vsize,s4offside,s4nearside,s4upper,s4lower] #@UndefinedVariable
s5list=[s5v1gap,s5v2gap,s5hgap,s5sut,s5vdso1,s5vdso2,s5hdso] #@UndefinedVariable
s6list=[s6hgap,s6hcentre,s6vgap,s6vcentre]  # @UndefinedVariable
samplelist=[th,x,y,z,phi,chi,difftth,draincurrent, lakeshore, sapara,saperp] # @UndefinedVariable
sgmlist=[sgmx,sgmr1,sgmh,sgmpitch,sgmwedgeoffside,sgmwedgenearside,sgmGratingSelect] # @UndefinedVariable
spectrometerlist=[specgamma,spech,specl] # @UndefinedVariable
#andorlist=[andorAccumulatePeriod,andorShutterMode,andorExtShutterTrigger,andorPreampGain,andorADCSpeed,andorVerticalShiftSpeed,andorVerticalShiftAmplitude,andorEMCCDGain,andorCoolerTemperature,andorCoolerControl,andorBinningSizeX,andorBinningSizeY,andorEffectiveHorizontal,andorEffectiveVertical]  # @UndefinedVariable

meta_data_list= metadatalist+m1list+m2list+m4list+m5list+pgmlist+s1list+s2list+s3list+s4list+s5list+s6list+samplelist+sgmlist+spectrometerlist#+andorlist

for each in meta_data_list:
    meta_add(each)
alias("meta_add")
alias("meta_ll")
alias("meta_ls")
alias("meta_rm")

b2.setOutputFormat(["%7.4f"])
x.setOutputFormat(["%10.6f"])

print
print "*"*80
#DiffCalc
print "import DIFFCALC support for I21"
try:
    from startup.i21 import *  # @UnusedWildImport
#     toolpoint_off()  # @UndefinedVariable
except:
    localStation_exception(sys.exc_info(), "import diffcalc error.")


#Mapping scan
from mapping_scan_commands import *

from scannabledevices.xrayBeamMonitor import XRayBeamMonitor
xbm=XRayBeamMonitor("xbm", xraywatchdog="XRayWatchdog")

from scannabledevices.samplePoistioner_instance import smp_positioner  # @UnusedImport

# repeat acquire at a fixed point
def acquireRIXS(n, det, exposure_time, *args):
    newargs=[tm,1,n,1,det,exposure_time] # @UndefinedVariable
    for arg in args:
        newargs.append(arg)
    scan([e for e in newargs])  
    
alias("acquireRIXS")

# if not installation.isLive():
#     print "Testing scan in hkl using DiffCalc ...."
#     newub('test_i21')  # @UndefinedVariable
#     setlat('test_i21', 3.78, 3.78, 20.1, 90, 90, 90)  # @UndefinedVariable
#     setub([[0.00000, 0.00000, 0.31260], [1.17537, -1.17537, 0.00000], [1.17537, 1.17537, 0.00000]])  # @UndefinedVariable
#     con(a_eq_b)  # @UndefinedVariable
#     setnhkl([0, 0, 1])  # @UndefinedVariable
# #     scan(h, .1, .2, .1, k, .1, .2, .1, l, .1, .2, .1, fourc, ct, 1)  # @UndefinedVariable
#     print "scan in hkl test completed."
    
    
from gdascripts.scan.installStandardScansWithProcessing import * # @UnusedWildImport
scan_processor.rootNamespaceDict=globals()
gdascripts.scan.concurrentScanWrapper.ROOT_NAMESPACE_DICT = globals()
scan_processor_normal_processes = scan_processor.processors
scan_processor_empty_processes  = []
 
def scan_processing_on():
    scan_processor.processors = scan_processor_normal_processes
 
def scan_processing_off():
    scan_processor.processors = scan_processor_empty_processes
 
print "Switch off scan processor by default !!!"    
print " To manually switch on scan processor, run 'scan_processing_on()' function on Jython Terminal."
print " To manually switch off scan processor, run 'scan_processing_off()' function on Jython Terminal."
scan_processing_off()

#Please leave Panic stop customisation last - specify scannables to be excluded from Panic stop
from i21commands.stopJythonScannables import stopJythonScannablesExceptExcluded  # @UnusedImport
STOP_ALL_EXCLUSIONS=[s5cam]  # @UndefinedVariable

simpleLog("===================== GDA ONLINE =====================")
