from gda.configuration.properties import LocalProperties
from gda.device.scannable import DummyScannable
from exafsscripts.vortex.vortexConfig import vortex
from exafsscripts.xspress.xspressConfig import xspress
from gda.device.scannable import TopupScannable
from gda.device.scannable import BeamMonitorWithFeedbackSwitchScannable
from gda.device.scannable import DetectorFillingMonitorScannable
from gda.device.scannable import BeamMonitorScannableForLineRepeat
from gda.data.fileregistrar import IcatXMLCreator
from cid_photodiode import CidPhotoDiode

from microfocus.map_select import MapSelect
from microfocus.map import Map
from microfocus.raster_map import RasterMap
from microfocus.raster_map_return_write import RasterMapReturnWrite

from gda.factory import Finder
from exafsscripts.exafs.i08DetectorPreparer import I08DetectorPreparer
from exafsscripts.exafs.i08SamplePreparer import I08SamplePreparer
from exafsscripts.exafs.i08OutputPreparer import I08OutputPreparer
from exafsscripts.exafs.i08ScanScripts import I08XasScan
#from exafsscripts.exafs.qexafs_scan import QexafsScan
from gda.data import PathConstructor

from microfocus.microfocus_elements import getXY,plotSpectrum,displayMap

from uk.ac.gda.client.microfocus.scan.datawriter import MicroFocusWriterExtender

from edxd_calibrator import refinement #script refinement that is used to calibrate the vortex about once a year

from sampleStageTilt import *

print "Initialization Started";

finder = Finder.getInstance()

gdaConfigDir = LocalProperties.get("gda.config")
gdaConfigDir = gdaConfigDir + "/"

rcpController = finder.find("RCPController")

if (LocalProperties.get("gda.mode") == 'live'):
    print "Create topup , detector and beam monitors to pause and resume scans"
    topupMonitor = TopupScannable()
    topupMonitor.setName("topupMonitor")
    topupMonitor.setTolerance(1.0)
    topupMonitor.setWaittime(1)
    topupMonitor.setTimeout(600)
    #topupMonitor.setTopupPV("SR-CS-FILL-01:COUNTDOWN")
    topupMonitor.setScannableToBeMonitored(epicsTopupMonitor)
    topupMonitor.configure()

    #beam = BeamMonitorWithFeedbackSwitchScannable('FE18I-RS-ABSB-02:STA',['BL18I-OP-DCM-01:FPMTR:FFB.FBON'],['BL18I-OP-DCM-01:FRMTR:FFB.FBON'])
    beam = BeamMonitorWithFeedbackSwitchScannable('FE18I-RS-ABSB-02:STA', [''])
    beam.setName("beam")
    beam.setTimeout(7200)
    beam.setWaittime(60)
    beam.configure()

    detectorFillingMonitor = DetectorFillingMonitorScannable()
    detectorFillingMonitor.setName("detectorFillingMonitor")
    detectorFillingMonitor.setTimeout(7200)
    detectorFillingMonitor.setStartTime(9)
    detectorFillingMonitor.setDuration(25.0)
    detectorFillingMonitor.configure()

    trajBeamMonitor = BeamMonitorScannableForLineRepeat(beam)
    trajBeamMonitor.setName("trajBeamMonitor")
    trajBeamMonitor.setTolerance(5)
    trajBeamMonitor.setWaittime(1)
    trajBeamMonitor.setTimeout(7200)
    trajBeamMonitor.configure()
    trajBeamMonitor.setLevel(1)

    add_default topupMonitor
    add_default trajBeamMonitor

    archiver = IcatXMLCreator()
    archiver.setDirectory("/dls/bl-misc/dropfiles2/icat/dropZone/i08/i08_")

detectorPreparer = I08DetectorPreparer()
samplePreparer = I08SamplePreparer(rcpController, sc_MicroFocusSampleX, sc_MicroFocusSampleY, sc_sample_z, D7A, D7B, kb_vfm_x)
outputPreparer = I08OutputPreparer()

loggingcontroller = Finder.getInstance().find("XASLoggingScriptController")

xas = I08XasScan(loggingcontroller,detectorPreparer, samplePreparer, outputPreparer, None)

non_raster_map = Map(D7A, D7B, counterTimer01, rcpController)
raster_map = RasterMap(D7A, D7B, counterTimer01, traj1ContiniousX, traj3ContiniousX, raster_counterTimer01, raster_xmap, traj1PositionReader, traj3PositionReader, raster_xspress, rcpController)
raster_map_return_write = RasterMapReturnWrite(D7A, D7B, counterTimer01, raster_xmap, traj1PositionReader, traj3PositionReader, traj1tfg, traj1xmap,traj3tfg, traj3xmap, traj1SampleX, traj3SampleX, raster_xspress, rcpController)
map = MapSelect(non_raster_map, raster_map, raster_map_return_write)

if (LocalProperties.get("gda.mode") == 'live'):
    xas.addMonitors(topupMonitor, beam, detectorFillingMonitor, trajBeamMonitor)
else:
    xas.addMonitors(None, None, None, None)

#qexafs = QexafsScan(loggingcontroller,detectorPreparer, samplePreparer, outputPreparer, qexafs_energy, qexafs_counterTimer01)
xanes = xas

alias("xas")
alias("xanes")
alias("vortex")
alias("xspress")
#alias("qexafs")
alias("map")
alias("raster_map")
alias("raster_map_return_write")

test = DummyScannable("test")

gdaRoot = LocalProperties.get("gda.root")
gdaConfigDir = LocalProperties.get("gda.config")
gdaConfigDir = gdaConfigDir + "/"

global mapRunning
mapRunning = 0

cid = CidPhotoDiode('cid', 'BL18I-DI-PHDGN-08')
cid.setExtraNames(['CID_Rminusdiode', 'CID_Rplusdiode', 'CID_Lminusdiode', 'CID_Lplusdiode']) 
cid.setOutputFormat(['%4.10f', '%4.10f', '%4.10f', '%4.10f'])

raster_xspress.setInputNames([])
raster_xmap.setInputNames([])

photonccd.setOutputFolderRoot("x:/data/2013/nt3894-1/xrd/")

print "Initialization Complete";
