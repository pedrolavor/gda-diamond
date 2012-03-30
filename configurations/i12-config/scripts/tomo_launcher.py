from gda.device.scannable import PseudoDevice

from gda.device.scannable import ScannableUtils
import time
from gda.epics import CAClient

class Recon(PseudoDevice):
    # constructor
    def __init__(self, name):
        self.setName(name) 
        self.setInputNames([])
        self.setExtraNames([])
        self.setOutputFormat([])
        self.setLevel(5)

    # returns the value this scannable represents
    def rawGetPosition(self):
        return []

    # Does the operation this Scannable represents
    def rawAsynchronousMoveTo(self, new_position):
		return

    # Returns the status of this Scannable
    def rawIsBusy(self):
        return 0


    def atScanStart(self):
        print "Starting the tomographic reconstruction scripts"






