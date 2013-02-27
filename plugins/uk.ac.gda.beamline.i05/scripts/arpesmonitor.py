import time, sys
import gda.factory.Finder
import uk.ac.diamond.scisoft.analysis.SDAPlotter

class ARPESMonitor:
    
    def __init__(self):
        self.scienta = gda.factory.Finder.getInstance().listAllLocalObjects("uk.ac.gda.arpes.detector.VGScientaAnalyser")[0]
        self.configure()

    def configure(self):
        self.scienta.prepareFixedMode()
        self.scienta.getAdBase().setNumExposures(1)
        #self.scienta.setCollectionTime(1)
        
    def start(self):
        self.configure()
        self.scienta.getAdBase().setImageMode(2)
        self.scienta.getAdBase().startAcquiring()
    
    def stop(self):
        self.scienta.getAdBase().stopAcquiring()
        self.scienta.getAdBase().setImageMode(0)
        
#am=ARPESMonitor()