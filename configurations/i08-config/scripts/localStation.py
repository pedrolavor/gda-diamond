from gda.configuration.properties import LocalProperties
from andormap import AndorMap
from andormapWithCorrection import AndorMapWithCorrection
from scanForImageCorrection import ScanForImageCorrection

print "Initialisation Started";
from gda.device import Scannable
from gda.jython.commands.GeneralCommands import ls_names, run

def ls_scannables():
    ls_names(Scannable)


from ScannableInvertedValue import PositionInvertedValue
photoDiode1Inverted = PositionInvertedValue("photoDiode1Inverted","photoDiode1")


from gdascripts.metadata.metadata_commands import setTitle, meta_add, meta_ll, meta_ls, meta_rm
alias("setTitle")
alias("meta_add")
alias("meta_ll")
alias("meta_ls")
alias("meta_rm")

from gdascripts.scan.installStandardScansWithProcessing import * #@UnusedWildImport
scan_processor.rootNamespaceDict=globals()

from gdascripts.pd.time_pds import waittimeClass, showtimeClass, showincrementaltimeClass, actualTimeClass
waittime=waittimeClass('waittime')
showtime=showtimeClass('showtime')
inctime=showincrementaltimeClass('inctime')
actualTime=actualTimeClass("actualTime")

#if (LocalProperties.get("gda.mode") == 'live'): 
#    beamMonitor.configure()
#    add_default beamMonitor
#    add_default topupMonitor

# create the command to run STXM mpas which involve andor
andormap = AndorMap(stxmDummy.stxmDummyY,stxmDummy.stxmDummyX,_andorrastor)

alias("andormap")
print "Command andormap(mapSize) created for arming the Andor detector before running STXM maps"

#To obtain the corrected images just use the collection strategy for step scan
scanForImageCorrection = ScanForImageCorrection(andor)
andormapWithCorrection = AndorMapWithCorrection(stxmDummy.stxmDummyY,stxmDummy.stxmDummyX,_andorrastor,scanForImageCorrection)
alias("andormapWithCorrection")

if (LocalProperties.get("gda.mode") == 'live'): 
    run "xrfmap"

print "Initialisation Complete";
