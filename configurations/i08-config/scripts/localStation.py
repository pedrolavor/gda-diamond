#import sys    
#import os
#import time
from gda.configuration.properties import LocalProperties
from gda.device.scannable import DummyScannable
from gda.factory import Finder
from gdascripts.messages import handle_messages
from gda.jython import InterfaceProvider
from gda.device.scannable import ScannableBase
from gda.data.scan.datawriter import NexusDataWriter

print "Initialisation Started";

finder = Finder.getInstance()

test = DummyScannable("test")
try:
    from gda.device import Scannable
    from gda.jython.commands.GeneralCommands import ls_names, vararg_alias
    
    def ls_scannables():
        ls_names(Scannable)

    
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

    from gdascripts.pd.time_pds import waittimeClass, showtimeClass, showincrementaltimeClass, actualTimeClass
    waittime=waittimeClass('waittime')
    showtime=showtimeClass('showtime')
    inctime=showincrementaltimeClass('inctime')
    actualTime=actualTimeClass("actualTime")

    # After scan process the data, fit the spectrum with a gaussian and obtain the peak value (important for calibration)
    from gdascripts.scan.installStandardScansWithProcessing import * #@UnusedWildImport
    scan_processor.rootNamespaceDict=globals()
    
    #run "gda_startup.py"
    print "Initialisation Complete";

except:
    exceptionType, exception, traceback = sys.exc_info()
    handle_messages.log(None, "Error in localStation", exceptionType, exception, traceback, False)
