from gda.scan import ConstantVelocityRasterScan
from gdascripts.scan import rasterscans
from gdascripts.scan.rasterscans import RasterScan
from gdascripts.scan.trajscans import setDefaultScannables
from gda.epics import CAClient
import time
import math

class AndorMap(RasterScan):
     
    def __init__(self,rowScannable,columnScannable,andor):
        RasterScan.__init__(self)
        self.Xsize = 50 # default
        self.Ysize = 50 # default
        self.rowScannable = rowScannable
        self.columnScannable = columnScannable
        self.andor = andor
        # setup the Andor trigger to internal for snapshots by default
        andor.getCollectionStrategy().getAdBase().setTriggerMode(0)
         
         
    def __call__(self, *args):

        # if one arg, then use that as the map size, else ignore any and all args
        if len(args) == 1:
            self.Xsize = int(args[0])
            self.Ysize = int(args[0])
        elif len(args) == 2:
            self.Xsize  = int(args[0])
            self.Ysize = int(args[1])
        # not implemented still waiting for SLS feedback
        #else :
         #   self.map_size = CAClient().get("BL08I-EA-DET-01:HDF5:ExtraDimSizeX_RBV")
          #  print "Map size will be",str(self.map_size)
        self.PrepareForCollection()
        self.scanargs = [self.rowScannable, 1, float(self.Ysize), 1, self.columnScannable, 1, float(self.Xsize), 1, self.andor, 0.1]
        RasterScan.__call__(self,self.scanargs)
     
    def _createScan(self, args):

        # TODO create/ configure a scannable which will oberve data points and broadcast out transmission/phase-contrast to plotting system
        
        # TODO get scan size from Epics PVs to replace self.map_size
        
        # TODO check Epics PV holding STXM status as a safety check

        #rasterscan row 1 20 1 col 1 20 1 _andorrastor .1 'col'
#         args = [self.rowScannable, 1, float(self.map_size), 1, self.columnScannable, 1, float(self.map_size), 1, self.andor]
        #self.ROISetup()
        myscan = ConstantVelocityRasterScan(self.scanargs)
        
        # TODO set a PV to tell stxm the scan number
        #scanNumber = scan.getScanNumber()
        
        # TODO tell the stxm the scan number, or the file prefix at this point

        return myscan
    
#configure the ROIs for both the step and raster andor objects
    def ROISetup(self):
        Xsize = andor.getCollectionStrategy().getAdBase().getArraySizeX_RBV()
        Ysize = andor.getCollectionStrategy().getAdBase().getArraySizeY_RBV()        
        XmidSize = Xsize/2
        YmidSize = Ysize/2
        
        print "Setting up Regions of Interest for andor and _andorrastor objects..."
        andor.roistats1.setRoi(0,0,XmidSize,YmidSize,"quadrant1")
        andor.roistats2.setRoi(0,YmidSize,XmidSize,YmidSize,"quadrant2")
        andor.roistats3.setRoi(XmidSize,0,XmidSize,YmidSize,"quadrant3")
        andor.roistats4.setRoi(XmidSize,YmidSize,XmidSize,YmidSize,"quadrant4")
        andor.roistats5.setRoi(0,0,Xsize,Ysize,"transmission")
      
    def OptimizeChunk(self):
        Xsize = andor.getCollectionStrategy().getAdBase().getArraySizeX_RBV()
        Ysize = andor.getCollectionStrategy().getAdBase().getArraySizeY_RBV() 
        dataType = andor.getCollectionStrategy().getAdBase().getDataType()
        # Each chunk is 1 MByte
        chunkSize = (1024**2)
        #pixel size in bytes
        pixelSize = (dataType+1)*2
        print "pixelSize:",pixelSize
        framesPerChunk = (chunkSize)/(Xsize*Ysize*pixelSize)
        print "framesperChunk:",framesPerChunk
        andor.getAdditionalPluginList()[0].setFramesChunks(framesPerChunk)
        
    def OpenAndorShutter(self):
        CAClient().put("BL08I-EA-DET-01:CAM:AndorShutterMode","1")
     
    def PrepareForCollection(self):   
        andor.getCollectionStrategy().getAdBase().stopAcquiring()
        time.sleep(1)
        self.OpenAndorShutter()
        self.ROISetup()
        self.OptimizeChunk()
        self.resetPlotters()
        
    def resetPlotters(self):
         transmission_plotter.setXArgs(0, self.Xsize, 1)
         transmission_plotter.setYArgs(0, self.Ysize, 1)
         horizontal_plotter.setXArgs(0, self.Xsize, 1)
         horizontal_plotter.setYArgs(0, self.Ysize, 1)
         vertical_plotter.setXArgs(0, self.Xsize, 1)
         vertical_plotter.setYArgs(0, self.Ysize, 1)
         
# then create the scan wrapper for map scans
# col = stxmDummy.stxmDummyX
# row = stxmDummy.stxmDummyY
andormap = AndorMap(stxmDummy.stxmDummyY,stxmDummy.stxmDummyX,_andorrastor)
alias andormap
print "Command andormap(mapSize) created for arming the Andor detector before running STXM maps"
