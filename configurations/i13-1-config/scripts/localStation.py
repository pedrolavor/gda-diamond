import sys	
import os
from gdascripts.messages import handle_messages
from gda.jython import InterfaceProvider
import gda.factory.FactoryException
import time

	
#try:
from gda.device import Scannable
from gda.jython.commands.GeneralCommands import ls_names, vararg_alias
from gda.device.scannable import ScannableBase
class ExperimentShutterEnumPositioner(ScannableBase):
	"""
	Class to handle 
	"""
	def __init__(self, name, delegate):
		self.name = name
		self.inputNames = [name]
		self.delegate = delegate
	def isBusy(self):
		return self.delegate.isBusy()
	def rawAsynchronousMoveTo(self,new_position):
		if new_position == "Open":
			self.delegate.asynchronousMoveTo(5.)
		else:
			self.delegate.asynchronousMoveTo(0.)
	def rawGetPosition(self):
		position = self.delegate.getPosition()
		if int(position) == 5:
			return "Open" 
		return "Closed"


def ls_scannables():
	ls_names(Scannable)

scansReturnToOriginalPositions=1

from epics_scripts.pv_scannable_utils import createPVScannable, caput, caget, caputStringAsWaveform, ls_pv_scannables
alias("ls_pv_scannables")
alias("caput")
alias("caget")

from gda.factory import Finder
from gda.configuration.properties import LocalProperties
#	from gdascripts.scannable.detector.ProcessingDetectorWrapper import ProcessingDetectorWrapper
import i13j

#import for help
from maxipix import mpx_set_folder, mpx_reset_configure, mpx_config_file_monitor
from robots import calcRobotMotors, calcRobotMotorsInverse
from gda.device.lima import LimaCCD
from gda.device.maxipix2 import MaxiPix2
from gda.util import VisitPath

finder = Finder.getInstance() 
beamline = finder.find("Beamline")
ring= finder.find("Ring")
commandServer = InterfaceProvider.getJythonNamespace()
#	import tests.testRunner
#	tests.testRunner.run_tests()

from gda.scan.RepeatScan import create_repscan, repscan
vararg_alias("repscan")

from gdascripts.pd.time_pds import waittimeClass2, showtimeClass, showincrementaltimeClass, actualTimeClass
waittime=waittimeClass2('waittime')
showtime=showtimeClass('showtime')
inctime=showincrementaltimeClass('inctime')
actualTime=actualTimeClass("actualTime")

from i13j_utilities import csn, nsn
alias("csn")
alias("nsn")

from gdascripts.metadata.metadata_commands import setTitle, meta_add, meta_ll, meta_ls, meta_rm
alias("setTitle")
alias("meta_add")
alias("meta_ll")
alias("meta_ls")
alias("meta_rm")
from gda.data.scan.datawriter import NexusDataWriter
LocalProperties.set(NexusDataWriter.GDA_NEXUS_METADATAPROVIDER_NAME,"metashop")

import help_cmds
if not LocalProperties.check("gda.dummy.mode"):
	try:
		import filter_array
		xia_filter=filter_array.filter_array("xia_filter", prefix="BL13J-OP-ATTN-02:", elements=["Cr", "Fe", "Cu", "Nb"])
	except gda.factory.FactoryException, e:
		print "!!!!!!!!!!!!!!!!!!!!!!! problem configuring xia_filter"
		print e
		print "Continuing anyway..."

from flyscan_script import flyscan, flyscannable, WaitForScannableAtLineEnd
vararg_alias("flyscan")
try:
	waitForQcm_bragg1 = WaitForScannableAtLineEnd('waitForQcm_bragg1', qcm_bragg1)
except NameError:
	print "!!!!!!!!!!!!!!!!!!!!!!! qcm_bragg1 not found so could not create waitForQcm_bragg1 "
	print "Continuing anyway..."
#createPVScannable( "d1_total", "BL13J-DI-PHDGN-01:STAT:Total_RBV")

if not LocalProperties.check("gda.dummy.mode"):
	try:
#		createPVScannable( "fs1", "BL13J-EA-FSHTR-01:CONTROL", hasUnits=False)
		createPVScannable( "expt_fastshutter_raw", "BL13J-EA-FSHTR-01:RAWCONTROL", hasUnits=False)
		expt_fastshutter = ExperimentShutterEnumPositioner("expt_fastshutter", expt_fastshutter_raw)
	except gda.factory.FactoryException, e:
		print "!!!!!!!!!!!!!!!!!!!!!!! problem configuring fast shutter "
		print e
		print "Continuing anyway..."
	try:
		createPVScannable( "ic1", "BL13J-DI-IONC-01:I", hasUnits=True)
		createPVScannable( "ic1_rate", "BL13J-DI-IONC-01:HRPHOTONRATE", hasUnits=True)
		createPVScannable( "ic2", "BL13J-DI-IONC-02:I", hasUnits=True)
		createPVScannable( "ic2_rate", "BL13J-DI-IONC-02:HRPHOTONRATE", hasUnits=True)
		
	except gda.factory.FactoryException, e:
		print "!!!!!!!!!!!!!!!!!!!!!!! problem configuring ion chamber"
		print e
		print "Continuing anyway..."


from gda.device.scannable import TwoDScanPlotter
t1_sxy_plotter = TwoDScanPlotter()
t1_sxy_plotter.setName("t1_sxy_plotter")
t1_sxy_plotter.setZ_colName("total")
#we should the ability to not count hot pixels however they are specified.



from gda.device.scannable.scannablegroup import ScannableGroup
#now done in sample_stage_t1.xml and diff.xml
#make scannablegroup for driving sample stage
#t1_sxy = ScannableGroup()
#t1_sxy.addGroupMember(t1_sx)
#t1_sxy.addGroupMember(t1_sy)
#t1_sxy.addGroupMember(ix)
#t1_sxy.setName("t1_sxy")
#t1_sxy.configure()

#diff_xy = ScannableGroup()
#diff_xy.addGroupMember(diff_x)
#diff_xy.addGroupMember(diff_y)
#diff_xy.addGroupMember(ix)
#diff_xy.setName("diff_xy")
#diff_xy.configure()


dummy_xy = ScannableGroup()
dummy_xy.addGroupMember(ix)
dummy_xy.addGroupMember(iy)
dummy_xy.addGroupMember(iz)
dummy_xy.setName("dummy_xy")
dummy_xy.configure()



#make ScanPointProvider
import sample_stage_position_provider
two_motor_positions = sample_stage_position_provider.ScanPositionProviderFromFile()
#two_motor_positions.load("/dls_sw/i13-1/software/gda_versions/gda_trunk2/i13j-config/scripts/tests/sample_stage_position_provider_test.dat",(0.,0.))

imageFitter = finder.find("imageFitter")
imageStats = finder.find("imageStats")
imagePlotter = finder.find("imagePlotter")
imageROI = finder.find("imageROI")
imageFitter2 = finder.find("imageFitter2")
imageStats2 = finder.find("imageStats2")
imagePlotter2 = finder.find("imagePlotter2")
imageROI2 = finder.find("imageROI2")
imageFitter3 = finder.find("imageFitter3")
imageStats3 = finder.find("imageStats3")
imagePlotter3 = finder.find("imagePlotter3")
imageROI3 = finder.find("imageROI3")

#disable profile as it does not support Integer - see DataSetStats line 70?
imageStats.profileY=False
imageStats.profileX=False

import roi_operations
mpx_roi_total_diff = roi_operations.roi_diff("mpx_roi_total_diff","mpx_roi_total_diff",mpx_wrap)
mpx_roi_average_diff = roi_operations.roi_diff("mpx_roi_average_diff","mpx_roi_average_diff",mpx_wrap, "mpx", "image_data.average", "image_data.average2")

#create objects in namespace
try:
	mpx_controller = mpx.getMaxiPix2MultiFrameDetector()
	mpx_threshold = mpx_controller.energyThreshold
	mpx_limaCCD = mpx_controller.getLimaCCD()
	mpx_maxipix = mpx_controller.getMaxiPix2()
	mpx_reset_configure()
except gda.factory.FactoryException, e:
	print "!!!!!!!!!!!!!!!!!!!!!!! problem configuring mpx detector"
	print e
	print "Continuing anyway..."
import file_converter

import mpx_external_scan_monitor
import mll
import integrate_mpx_scan
#	try:
#		mpx_set_folder("test","mpx")
#	except :
#		exceptionType, exception, traceback = sys.exc_info()
#		handle_messages.log(None, "Problem setting mpx folder and prefix",exceptionType, exception, traceback,False)
#from tests.testRunner import run_tests

#comment out when not connected
#from autocollimator_script import  * #@UnusedWildImport

#run("i13diffcalc")
#del diff, delta, gamma, eta, chi, phi
#execfile("/dls_sw/i13-1/software/diffcalc/example/startup/sixcircle_dummy.py")
#execfile("/dls_sw/i13-1/software/diffcalc/example/startup/sixcircle.py")

#except :
#	exceptionType, exception, traceback = sys.exc_info()
#	handle_messages.log(None, "Error in localStation", exceptionType, exception, traceback, False)

from gdascripts.scannable.beamokay import WaitWhileScannableBelowThresholdMonitorOnly
#comment out when not connected - 
#beammonitor=WaitWhileScannableBelowThresholdMonitorOnly("beammonitor", d4_i, 1,1,1)

ix.setInputNames(["ix"])
iy.setInputNames(["iy"])
iz.setInputNames(["iz"])

#stuff for Vortex editor
def vortex(vortexParameterName, outputfile):
	from uk.ac.gda.beans.vortex import VortexParameters	
	VortexParameters.writeToXML(XspressParametersToLoad, mll_xmap.getConfigFileName());
	mll_xmap.loadConfigurationFromFile()

alias("vortex")

import scan_aborter
beam_check=scan_aborter.scan_aborter("beam_check",3, 300000., "Too high")
#imageROI.enable = True
#imageStats.enable = True
#imageROI.setROI(370, 390, 370, 390)#    ( y_start, y_end, x_start, x_end)


if not LocalProperties.check("gda.dummy.mode"):
	import average
	d4_i_avg = average.Average(d4_i,numPoints=10, timeBetweenReadings=0.1)

def eh_shtr_control():
	if eh_shtr()=="Open":
		pos eh_shtr "Close"
	else:
		pos eh_shtr "Reset"
		time.sleep(3)
		pos eh_shtr "Open"


def fs_control():
	if fs()=="Open":
		pos fs "Closed"
	else:
		pos fs "Open"

#mtscripts have been commented out of JythonServerFacade as this is used temprarily for moveable equipment
#import mtscripts.moveable.me07m
#from mtscripts.moveable.me07m import mepiezo1x, mepiezo1y, eembimorph, dummy_bimorph

#import dataset_provider

#from gdascripts.scannable.detector.DetectorDataProcessor import DetectorDataProcessorWithRoi
#from gdascripts.analysis.datasetprocessor.twod.TwodGaussianPeak import TwodGaussianPeak
#from gdascripts.analysis.datasetprocessor.twod.SumMaxPositionAndValue import SumMaxPositionAndValue
#from gdascripts.analysis.datasetprocessor.twod.PixelIntensity import PixelIntensity

#detDSProvider = dataset_provider.NXDetectorDataWithFilepathForSrsDatasetProvider(pcoEdge,fileLoadTimout=5.)

#peak2d = DetectorDataProcessorWithRoi('peak2d', detDSProvider, [TwodGaussianPeak()])
#max2d = DetectorDataProcessorWithRoi('max2d', detDSProvider, [SumMaxPositionAndValue()])
#intensity2d = DetectorDataProcessorWithRoi('intensity2d', detDSProvider, [PixelIntensity()])

###############################################################################
###                   Configure scan data processing                        ###
###############################################################################
#from analysis_FindScanPeak import FindScanPeak
#from analysis_FindScanCentroid import findCentroidPoint, FindScanCentroid, readSRSDataFile
#print "Importing analysis commands (peak, centroid & peak optimisation)"
#peak=FindScanPeak #@UndefinedVariable
#cen=FindScanCentroid #@UndefinedVariable

#from gdascripts.scan import gdascans
#from gdascripts.scan.installStandardScansWithProcessing import * #@UnusedWildImport
#import gdascripts
#gdascripts.scan.concurrentScanWrapper.PRINTTIME = True
#gdascripts.scan.concurrentScanWrapper.ROOT_NAMESPACE_DICT = globals()
#scancn=gdascans.Scancn([scan_processor])
#alias('scancn');print scancn.__doc__.split('\n')[2]
#lup = dscan # line up apparently!
#alias('lup')

#scan_processor.rootNamespaceDict=globals()
#scan_processor.duplicate_names = {'maxval':'maxpos', 'minval':'minpos'}
#scan_processor.processors.append(Lcen())
#scan_processor.processors.append(Rcen())
#scan_processor.processors.append(GaussianEdge(name='spedge')) # edge already maps to a function edgeDetectRobust


#dacscan is used by excalibur
from dac_scan import dacscan
vararg_alias("dacscan")

import excalibur_config
#from gdascripts.bimorph import bimorph

#from gdascripts.pd.dummy_pds import DummyPD
#from gdascripts.scannable.detector.dummy.focused_beam_dataset import CreateImageReadingDummyDetector
#from gdascripts.scannable.detector.ProcessingDetectorWrapper import ProcessingDetectorWrapper
#from gdascripts.scannable.detector.DetectorDataProcessor import DetectorDataProcessorWithRoi
#from gdascripts.analysis.datasetprocessor.twod.TwodGaussianPeak import TwodGaussianPeak
#from gdascripts.analysis.datasetprocessor.twod.SumMaxPositionAndValue import SumMaxPositionAndValue
#from gdascripts.analysis.datasetprocessor.twod.PixelIntensity import PixelIntensity
#x = DummyPD("x")
#x.asynchronousMoveTo(430)
#cam1det = CreateImageReadingDummyDetector.create(x)
#cam1 = ProcessingDetectorWrapper('cam1', cam1det, [], panel_name_rcp='Plot 1')
#cam1 = ProcessingDetectorWrapper('cam1', pcoEdge_tif, [], panel_name_rcp='Plot 1')
#peak2d = DetectorDataProcessorWithRoi('peak2d', cam1, [TwodGaussianPeak()])
#max2d = DetectorDataProcessorWithRoi('max2d', cam1, [SumMaxPositionAndValue()])
#intensity2d = DetectorDataProcessorWithRoi('intensity2d', cam1, [PixelIntensity()])
#cam1.returnPathAsImageNumberOnly=True

#from gdascripts.bimorph.bimorph_mirror_optimising import SlitScanner, ScanAborter, TopupCountdown
#scanAborter=ScanAborter("scanAborter",ic, -10)
#slitscanner = SlitScanner()
#slitscanner.setScanAborter(scanAborter)
#bm_topup = TopupCountdown("bm_topup")

#	caput ("BL13I-EA-DET-01:CAM:ReverseX", 1)
if( caget("BL13J-EA-DET-01:CAM:Model_RBV") == "PCO.Camera 4000"):
	caput("BL13J-EA-DET-01:CAM:PIX_RATE", "32000000 Hz")
if( caget("BL13J-EA-DET-01:CAM:Model_RBV") == "PCO.Camera Edge"):
	caput("BL13J-EA-DET-01:CAM:PIX_RATE", "286000000 Hz")	


createPVScannable( "afg_chan1_ampl", "BL13J-EA-FNGEN-01:CHAN1:AMPLITUDE", hasUnits=False)
# pos afg_chan1_ampl 2.
createPVScannable( "afg_chan1_state", "BL13J-EA-FNGEN-01:CHAN1:OUTPUT:STATE", hasUnits=False, getAsString=True)
# pos afg_chan1_state "On"

run("localStationUser.py")

#8/4/2014 pie725 not present
#run("startup_pie725")
