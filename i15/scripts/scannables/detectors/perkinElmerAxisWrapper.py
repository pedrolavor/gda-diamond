import os
from time import sleep
from gdascripts.messages.handle_messages import simpleLog
from operationalControl import moveMotor
from ccdScanMechanics import setMaxVelocity
from ccdScanMechanics import deactivatePositionCompare
from ccdScanMechanics import scanGeometry
from ccdScanMechanics import setVelocity
from gda.data.fileregistrar import FileRegistrarHelper
from glob import glob
from scannables.detectors.detector_axis_wrapper import DetectorAxisWrapperNew

class PerkinElmerAxisWrapper(DetectorAxisWrapperNew):
    def __init__(self, detector, isccd, prop, feabsb, fmfabsb, exposureTime=1,
                 axis=None, step=None, sync=False, fileName="pe_scan",
                 noOfExpPerPos=1, rock=False, pause=False, exposeDark=False):
        
        DetectorAxisWrapperNew.__init__(self, detector, isccd, prop, feabsb,
            fmfabsb, pause, -11, exposureTime, axis, sync, exposeDark)
        self.fileName = fileName
        #self.fullFileName = ""
        self.exposureNo = 1
        self.noOfExpPerPos = noOfExpPerPos
        #self.nextScanNo = getNextMarScanNumber()
        self.inc = 1;
        self.setName("perkin elmer wrapper")
        self.rock=rock
        
        if step:
            self.step = float(step)
            self.velocity = float(abs(self.step)) / float(self.exposureTime)
        else:
            self.velocity = 0

    def atScanStart(self):
        DetectorAxisWrapperNew.atScanStart(self)
        self.detector.prepareForCollection()

    def acquireOneImage(self, position):
        if self.detector.verbose:
            simpleLog("PerkinElmerAxisWrapper.acquireOneImage(%r)" % position)
        runUp = ((self.velocity*.25)/2) + 0.1 # acceleration time .25 may
        #change. This seems to solve the problem of the fast shutter not
        #staying open.
        
        self.detector.darkExpose = False
        
        if self.detector.skippedAtStart > 0:
            simpleLog("Acquiring dummy image to clear last acquisition...")
            self.detector.skipExpose = True
            self.detector.collectData()
            #sleep(self.detector.skippedAtStart *
            #      self.detector.pe.exposureTime_get())
            simpleLog("Waiting for Perkin Elmer status idle after dummy image")
            #while self.detector.getStatus():
            while self.detector.fileIndex == self.detector.pe.fileIndex_get():
                sleep(0.5)
                print ".",
            print "."
            
            simpleLog("Resetting fileIndex")
            self.detector.pe.fileIndex_set(self.detector.fileIndex) # fileIndex
            # is the next two be written, so set it back to the previous values
            # after acquiring a skipped image.
            while self.detector.fileIndex != self.detector.pe.fileIndex_get():
                sleep(0.5)
                print ".",
            print "."
            self.detector.skipExpose = False
        
        if self.detector.verbose:
            simpleLog("Setting collection time...")
        
        self.detector.setCollectionTime(self.exposureTime)
        
        if self.detector.verbose:
            simpleLog("Acquiring image...")
        
        if self.sync:
            setMaxVelocity(self.axis)
            deactivatePositionCompare() #Prevent false triggers when debounce on
            moveMotor(self.axis, position - runUp)
            scanGeometry(self.axis, self.velocity, position , position + self.step)
            sleep(0.2)
            self.isccd.xpsSync("dummy", self.exposureTime)
            
            self.preExposeCheck()
            
            self.detector.collectData()
            moveMotor(self.axis, position + self.step + runUp)
            
            deactivatePositionCompare()
            
        elif self.axis:
            simpleLog("(fast shutter not synchronised with motor)")
            setMaxVelocity(self.axis)
            moveMotor(self.axis, position - runUp)
            setVelocity(self.axis, self.velocity)
            self.isccd.openS()
            
            self.detector.collectData()
            moveMotor(self.axis, position + self.step + runUp)
            
            self.isccd.closeS()
            
        elif self.exposeDark:
            self.detector.darkExpose = True
            self.detector.collectData()
            sleep(self.exposureTime+0.1)
        else:
            self.isccd.openS()
            self.detector.collectData()
            sleep(self.exposureTime)
            self.isccd.closeS()
        
        if self.detector.verbose:
            simpleLog("Waiting for Perkin Elmer status idle")
        while self.detector.getStatus():
            sleep(0.5)
            print ".",
        print "."
        if self.detector.verbose:
            simpleLog("Detector idle")
        
        # Since the scanning mechanism calls the detector readout, do we need
        # this here too?
        self.detector.readout()
        if self.detector.verbose:
            simpleLog("Readout complete")

    def rawAsynchronousMoveTo(self, position):

        self.files = []
        
        for exp in range(self.noOfExpPerPos):
            
            if self.velocity <= 8.0:
            
                self.isccd.flush()
                
                split = os.path.split(self.fileName)
                visitDir = self.visitPath.replace(self.detector.dataDirRoot+"/","")
                self.detector.visitDir = visitDir
                self.detector.relativePath = split[0]
                self.detector.filePattern = split[1]
                
                self.acquireOneImage(position)
                
                if self.postExposeCheckFailed():
                    self.acquireOneImage(position)
                
#                if self.noOfExpPerPos > 1:
#                    self.fullFileName = self.fileName + "_%03d" % self.exposureNo
#                elif self.rock:
#                    self.fullFileName = self.fileName
#                else:
#                    self.fullFileName = self.fileName + "_%03d" % self.inc
#
#                # Make sure that any output files do not exist before we start:
#                expectedFile = self.visitPath + "/" + self.fullFileName
#                expectedGlob =expectedFile + "_001.*"
#                filesAtLocation = glob(expectedGlob)
                
#                if len(filesAtLocation) > 0:
#                    simpleLog("Warning, files found matching %s: \n%s\nRenaming..." %
#                              (expectedGlob, "\n".join(filesAtLocation)))
#                    for file in filesAtLocation:
#                        newFile = file.replace("_001.","_bak.")
#                        try:
#                            os.rename(file, newFile)
#                        except OSError:
#                            simpleLog("Error renaming file %s to %s" %
#                                      (file, newFile))

#                #self.scanTheMarWithChecks(300)
#            
#                # There should now be only one file which starts with fullFileName
#                filesAtLocation = glob(expectedGlob)
#
#                if len(filesAtLocation) == 1:
#                    # Rename it to strip out the 
#                    self.fullFileLocation = filesAtLocation[0].replace("_001.",".")
#                    try:
#                        #simpleLog("Renaming file %s to %s" %
#                        #          (filesAtLocation[0], self.fullFileLocation))
#                        os.rename(filesAtLocation[0], self.fullFileLocation)
#                        self.files.append(self.fullFileLocation)
#                        FileRegistrarHelper.registerFile(self.fullFileLocation)    
#                    except OSError:
#                        simpleLog("Error renaming file %s to %s" %
#                                  (filesAtLocation[0], self.fullFileLocation))
#                        # Since  we can't rename it, register the unrenamed file. 
#                        self.files.append(filesAtLocation[0])
#                        FileRegistrarHelper.registerFile(filesAtLocation[0])    
#                        
#                # If there are no or 2+ matching files, try to fail gracefully.
#                elif len(filesAtLocation) == 0:
#                    simpleLog("Error, no file(s) found matching %s" % expectedGlob)
#                    
#                else:
#                    simpleLog("Error, multiple files found matching %s: \n%s" %
#                              (expectedGlob, "\n".join(filesAtLocation)))
#                
#                
#                #modMar = modMarName(self.fullFileLocation)
#                #modMar.start()
                filename = self.detector.readout()
                self.files.append(filename)
                simpleLog("self.files=%r @ exp=%d" % (self.files, exp))
                FileRegistrarHelper.registerFile(filename)
            else:
                simpleLog("velocity too high, please specify a longer exposure time (max velocity of kphi=8.0 deg/sec)")
        
            self.exposureNo += 1
        self.inc +=1
                
    def rawIsBusy(self):
        return self.detector.getStatus();

#    def scanTheMarWithChecks(self, timeout):
#        """
#        Scan the mar, checking for correct status 
#        """
#        self.detector.setRootName(self.fullFileName)
#
#        mar_mode = self.detector.getMode()
#        if (mar_mode != 4):
#            simpleLog( "Mar mode is %d not the default 4, use 'mar.setMode(X)' to change mode to X or mar.setMode(-1) to list modes." % mar_mode)
#
#        # Wait for mar to be ready before starting scan
#        timeTaken = self.waitForStatus(timeout, 0)
#        if (timeTaken == -1):
#            raise "Timed out waiting for mar to be ready, so scan not performed"
#    
#        simpleLog("mar ready in time %.2f" % timeTaken + "s")
#        # Wait for mar to start scanning
#        simpleLog("Scan command sent to mar... (timeout = " + str(timeout) + ")") 
#        self.detector.scan()
#        timeTaken = self.waitForStatus(timeout, 1)
#        if (timeTaken == -1):
#            raise "Timed out waiting for mar to start, so scan not performed"
#    
#        simpleLog("mar busy in time %.2f" % timeTaken + "s")
#        # Scan scanning and wait for mar to be ready
#        timeTaken = self.waitForStatus(timeout, 0)
#        if (timeTaken == -1):
#            raise "Timed out waiting for mar to stop scanning"
#
#        simpleLog("Scanned in time %.2f" % timeTaken + "s")

#    def waitForStatus(self, timeout, status):
#        
#        t0 = clock()
#        t1 = t0
#        while ((t1 - t0) < timeout): 
#            if (self.detector.getStatus() == status):
#                simpleLog("Mar status of " + str(status) + " reached in time %.2f" % (t1 - t0) + "s")
#                return (t1 - t0)
#            t1 = clock()
#            pause()                     # ensures script can be stopped promptly
#    
#        simpleLog("Timed out waiting for mar status of " + str(status) + " (waited " + str(timeout) + "s)")
#        return - 1

#    def remove_001Suffix(self):
#        """
#        Remove '_001' suffix from file paths (added by mar software)
#        """
#        simpleLog("removing '_001' suffix from all files created...")
#        filesCreated = []
#        for filePath in self.filePaths:
#            print filePath
#            fileWithSuffix_001 = filePath.replace(".mar3450", "_001.mar3450")
#            if (doesFileExist(fileWithSuffix_001)):
#                os.rename(fileWithSuffix_001, filePath)
#            else:
#                simpleLog("Could not find file " + fileWithSuffix_001 + " to rename")
