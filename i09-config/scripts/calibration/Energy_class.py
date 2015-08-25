from gda.device.scannable import ScannableMotionBase
import gda.factory.Finder as Finder
import sys
#from gda.function.lookup import LookupTable
import math
from LookupTables import readLookupTable
from gda.device.scannable.scannablegroup import ScannableGroup
from gda.configuration.properties import LocalProperties


class BeamEnergy(ScannableMotionBase):
    '''Create beam energy scannable that encapsulates and fan-outs control to ID gap and DCM energy.
    
        This pseudo device requies a lookup table object to provide ID parameters for calculation of ID gap from beam 
        energy required and harmonic order. The lookup table object must be created before the instance creation of this class.
        The child scannables or pseudo devices must exist in jython's global namespace prior to any method call of this class 
        instance.
        The lookup Table object is described by gda.function.LookupTable class.'''
        
    def __init__(self, name, gap="igap", dcm="dcmenergy", undulatorperiod=27, lut="IIDCalibrationTable.txt"):
        '''Constructor - Only succeed if it find the lookup table, otherwise raise exception.'''
        finder=Finder.getInstance()
        self.lut=readLookupTable(LocalProperties.get("gda.config")+"/lookupTables/"+lut)
        self.gap=gap
        self.dcm=dcm
        self.lambdau=undulatorperiod
        if dcm is None:
            self.scannableNames=[gap]
        else:
            self.scannableNames=[dcm,gap]
        self.scannables=ScannableGroup(name, [finder.find(x) for x in self.scannableNames])
        self._busy=0
        self.setName(name)
        self.setLevel(3)
        self.setOutputFormat(["%10.6f"])
        self.inputNames=[name]
        if self.dcm == "dcmenergy":
            self.order=3
        else:
            self.order=1
        self.energy=self.scannables.getGroupMember(self.scannableNames[0]).getPosition()
        self.polarisation='H'
    
    def setPolarisation(self, value):
        if self.getName()=="jenergy":
            if value == "H" or value == "V":
                self.polarisation=value
            else:
                raise ValueError("Input "+str(value)+" invalid. Valid values are 'H' or 'V'.")
        else:
            print "No polaristion parameter for Hard X-ray ID"
    
    def getPolarisation(self):
        if self.getName()=="jenergy":
            return self.polarisation
        else:
            return "No polaristion parameter for Hard X-ray ID"
    
    def HarmonicEnergyRanges(self):
        print ("%s\t%s\t%s" % ("Harmonic", "Min Energy", "Max Energy"))
        keys=[int(key) for key in self.lut.keys()]
        for key in sorted(keys):
            print ("%8.0d\t%10.2f\t%10.2f" % (key,self.lut[key][2],self.lut[key][3]))
            
    def eneryRangeForOrder(self, order):
        return [self.lut[order][2],self.lut[order][3]]
        
    def setOrder(self,n):
        self.order=n
        
    def getOrder(self):
        return self.order
    
    def idgap(self, Ep, n):
        gap=20.0
        if self.getName() == "ienergy":
            lambdaU=self.lambdau
            M=4
            h=16
            me=0.510999
            gamma=1000*self.lut[n][0]/me
            Ksquared=(4.959368e-6*(n*gamma*gamma/(lambdaU*Ep))-2)
            if Ksquared < 0:
                raise ValueError("Ksquared must be positive!")
            K=math.sqrt(Ksquared)
            A=(2*0.0934*lambdaU*self.lut[n][1]*M/math.pi)*math.sin(math.pi/M)*(1-math.exp(-2*math.pi*h/lambdaU))
            gap=(lambdaU/math.pi) * math.log(A/K)+self.lut[n][6]
#            if self.gap=="igap" and (gap<5.1 or gap>9.1):
#                raise ValueError("Required Hard X-Ray ID gap is out side allowable bound (5.1, 9.1)!")
            if self.gap=="jgap" and gap<16:
                raise ValueError("Required Soft X-Ray ID gap is out side allowable bound (> 16 mm)!")
        elif (self.getName() == "jenergy" and self.getPolarisation()=="H"):
            if (Ep<0.104 or Ep > 1.2):
                raise ValueError("Demanding energy must lie between 0.105 and 1.2 keV!")
            gap=2.56288 + 186.99257*Ep - 653.74749*Ep**2 + 1589.71628*Ep**3 - 2375.03513*Ep**4 + 2110.75282*Ep**5 - 1019.61741*Ep**6 + 206.70745*Ep**7
            if self.gap=="jgap" and (gap<16 or gap>60):
                raise ValueError("Required Soft X-Ray ID gap is out side allowable bound (16, 60)!")
        elif self.getName() == "jenergy" and self.getPolarisation()=="V":
            if (Ep<0.22 or Ep > 1.0):
                raise ValueError("Demanding energy must lie between 0.22 and 1.0 eV!")
            gap = 5.33595 + 72.53678*Ep - 133.96826*Ep**2 + 179.99229*Ep**3 - 128.83048*Ep**4 + 39.34346*Ep**5
            if self.gap=="jgap" and (gap<16.01 or gap>35):
                raise ValueError("Required Soft X-Ray ID gap is out side allowable bound (16, 34)!")
        else:
            raise ValueError("Unsupported scannable or polarisation mode")
        return gap
        
    def rawGetPosition(self):
        '''returns the current position of the beam energy.'''
        self.energy=self.scannables.getGroupMember(self.scannableNames[0]).getPosition()
        return self.energy;
    
    def calc(self, energy, order):
        return self.idgap(energy, order)

    def rawAsynchronousMoveTo(self, new_position):
        '''move beam energy to specified value.
        At the background this moves both ID gap and Mono Bragg to the values corresponding to this energy.
        If a child scannable can not be reached for whatever reason, it just prints out a message, then continue to next.'''
        self.energy = float(new_position)
        gap = 7
        try:
            if self.getName() == "dummyenergy":
                gap=self.energy
            else:
                gap=self.idgap(self.energy, self.order)
        except:
            raise
        if self.getName() == "ienergy":
            if self.energy<self.eneryRangeForOrder(self.order)[0] or self.energy>self.eneryRangeForOrder(self.order)[1]:
                raise ValueError("Requested photon energy is out of range for this harmonic!")
        for s in self.scannables.getGroupMembers():
            if s.getName() == self.gap:
                try:
                    s.asynchronousMoveTo(gap)
                except:
                    print "cannot set " + s.getName() + " to " + str(gap)
                    raise
            else:
                try:
                    if s.getName() == "pgmenergy":
                        s.asynchronousMoveTo(self.energy*1000)
                        # caput("ELECTRON-ANALYSER-01:TEST:EXCITATION_ENERGY", self.energy*1000)
                    else:
                        s.asynchronousMoveTo(self.energy)
                        # caput("ELECTRON-ANALYSER-01:TEST:EXCITATION_ENERGY", self.energy*1000)
                except:
                    print "cannot set " + s.getName() + " to " + str(self.energy)
                    raise
                
    def rawIsBusy(self):
        '''checks the busy status of all child scannable.
        
        If and only if all child scannable are done this will be set to False.'''  
        self._busy=0      
        for s in self.scannables.getGroupMembers():
            try:
                self._busy += s.isBusy()
            except:
                print s.getName() + " isBusy() throws exception ", sys.exc_info()
                raise
        if self._busy == 0:
            return 0
        else:
            return 1

    def toString(self):
        '''formats what to print to the terminal console.'''
        return self.name + " : " + str(self.rawGetPosition())
    
   

