from gda.configuration.properties import LocalProperties
from gda.device.scannable import DummyScannable
from gda.factory import Finder
from gdascripts.messages import handle_messages
from gda.jython import InterfaceProvide
from gda.device.scannable import ScannableBase,BeamMonitorScannableWithResume, CoupledScannabl
from gda.device.monitor import EpicsMonitor
from gdascripts.parameters.beamline_parameters import JythonNameSpaceMapping
#from gdascripts.scannable.beamokay import WaitWhileScannableBelowThreshold, WaitForScannableState

print "Initialisation Started";

finder = Finder.getInstance()

test = DummyScannable("test")


from gda.device import Scannable
from gda.jython.commands.GeneralCommands import ls_names, vararg_alias

def ls_scannables():
    ls_names(Scannable)


from ScannableInvertedValue import PositionInvertedValue
photoDiode1Inverted = PositionInvertedValue("photoDiode1Inverted","photoDiode1")

#from epics_scripts.pv_scannable_utils import createPVScannable, caput, caget
#alias("createPVScannable")
#alias("caput")
#alias("caget")

from gda.scan.RepeatScan import create_repscan, repscan
vararg_alias("repscan")

from gdascripts.metadata.metadata_commands import setTitle, meta_add, meta_ll, meta_ls, meta_rm
alias("setTitle")
alias("meta_add")
alias("meta_ll")
alias("meta_ls")
alias("meta_rm")
from gda.data.scan.datawriter import NexusDataWriter
LocalProperties.set(NexusDataWriter.GDA_NEXUS_METADATAPROVIDER_NAME,"metashop")

# Remove this metadata scriptfor 8.38 version writes metadata in before_scan folder
#from metadata import setMetadata
#setMetadata()

from gdascripts.scan.installStandardScansWithProcessing import * #@UnusedWildImport
scan_processor.rootNamespaceDict=globals()

from gdascripts.pd.time_pds import waittimeClass, showtimeClass, showincrementaltimeClass, actualTimeClass
waittime=waittimeClass('waittime')
showtime=showtimeClass('showtime')
inctime=showincrementaltimeClass('inctime')
actualTime=actualTimeClass("actualTime")

# Use for the calibration of the pgm energy, create a scannable idEnergy
from idEnergy import my_energy_class1

#checkrc = WaitWhileScannableBelowThreshold('checkrc', rc, 190, secondsBetweenChecks=1,secondsToWaitAfterBeamBackUp=5) #@UndefinedVariable
#checkfe = WaitForScannableState('checkfe', frontend, secondsBetweenChecks=1,secondsToWaitAfterBeamBackUp=60) #@UndefinedVariable
#checkshtr1 = WaitForScannableState('checkshtr1', shtr1, secondsBetweenChecks=1,secondsToWaitAfterBeamBackUp=60) #@UndefinedVariable
#checkbeam = ScannableGroup('checkbeam', [checkrc,  checkfe, checkshtr1])
#checkbeam.configure()

#if (LocalProperties.get("gda.mode") == 'live'): 
#    beamMonitor.configure()
#    add_default beamMonitor
#    add_default topupMonitor 
   

# set up the Andor Area Detector ROIs etc for hardware-driven mapping
#run "AndorConfiguration"
# create the command to run STXM mpas which involve andor

run "andormap"
#run('startup_raster')
#run "gda_startup.py"

# create plotters for raster maps
test2 = gda.device.scannable.DummyScannable()
test2.setName("test2")
from gda.device.scannable import TwoDScanPlotter
horizontal_plotter = TwoDScanPlotter()
horizontal_plotter.setName("horizontal_plotter")
horizontal_plotter.setZ_colName('Horizontal')
horizontal_plotter.setPlotViewname("Horizontal Gradient")

vertical_plotter = TwoDScanPlotter()
vertical_plotter.setName("vertical_plotter")
vertical_plotter.setZ_colName('Vertical')
vertical_plotter.setPlotViewname("Vertical Gradient")

transmission_plotter = TwoDScanPlotter()
transmission_plotter.setName("transmission_plotter")
transmission_plotter.setZ_colName('transmission_total')
transmission_plotter.setPlotViewname("Transmission")

add_default horizontal_plotter vertical_plotter transmission_plotter


print "Initialisation Complete";






