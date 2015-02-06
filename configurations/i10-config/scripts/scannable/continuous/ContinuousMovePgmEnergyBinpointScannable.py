"""
Continuous Energy Scannable and Controller for using Constant Velocity on I10
for use with GDA at Diamond Light Source
"""

from gda.device.scannable import ContinuouslyScannableViaController, \
    ScannableMotionBase, PositionCallableProvider
from java.util.concurrent import Callable
from org.slf4j import LoggerFactory
from pgm.pgm import angles2energy

""" This scannable uses the motor controller to just control the motor and calculates the
    actual position from the position callables provided by the specified pitch motors.
"""
class ContinuousMovePgmEnergyBinpointScannable(ContinuouslyScannableViaController, ScannableMotionBase, PositionCallableProvider):
    """ Since the binpoints are slaved from a multi channel scaler card, motion will fail if the
        no scaler channels are specified in the scan.
        
        Also, since this scannable takes over starting the binpoint mecahnism, it may not work if
        individual binpoint scannables are added to the scan. """

    def __init__(self, name, move_controller, binpointGrtPitch, binpointMirPitch, binpointPgmEnergy):
        self.name = name
        #from gda.device.continuouscontroller import ConstantVelocityMoveController
        #self._move_controller = ConstantVelocityMoveController() # Enable completion of interface methods
        #self._binpointGrtPitch = PositionCallableProvider() # Enable completion of interface methods
        #self._binpointGrtPitch = ScannableMotionBase()      # Enable completion of class methods
        #self._binpointMirPitch = PositionCallableProvider() # Enable completion of interface methods
        #self._binpointMirPitch = ScannableMotionBase()      # Enable completion of class methods

        self._move_controller = move_controller
        self._binpointGrtPitch = binpointGrtPitch
        self._binpointMirPitch = binpointMirPitch
        self._binpointPgmEnergy = binpointPgmEnergy

        self.inputNames = [name]
        self.extraNames = EnergyCalculatingCallable.getPositionCallableExtraNames()
        self.outputFormat = EnergyCalculatingCallable.getPositionCallableFormat()

        self._operating_continuously = False
        self._last_requested_position = None
        self.logger = LoggerFactory.getLogger("ContinuousMovePgmEnergyBinpointScannable:%s" % name)
        self.verbose = False

    # Implement: public interface ContinuouslyScannableViaController extends Scannable

    def setOperatingContinuously(self, b):
        if self.verbose:
            self.logger.info('setOperatingContinuously(%r) was %r' % (b, self._operating_continuously))
        self._operating_continuously = b

    def isOperatingContinously(self):
        return self._operating_continuously

    def getContinuousMoveController(self):
        return self._move_controller

    # Implement: public interface PositionCallableProvider<T> {

    # public Callable<T> getPositionCallable() throws DeviceException;
    def getPositionCallable(self):
        if self.verbose:
            self.logger.info('getPositionCallable()... last_requested_position=%r' % (
                                               self._last_requested_position))
        return EnergyCalculatingCallable(self, self._last_requested_position,
                                         self._binpointGrtPitch.getPositionCallable(),
                                         self._binpointMirPitch.getPositionCallable(),
                                         self._binpointPgmEnergy.getPositionCallable())
        # Note that we use the binpoint mechanism to get the actual positions of the grating
        # and mirror pitch and calculate the energy from those positions at each point.

    # Override: public class ScannableMotionBase extends ScannableBase implements ScannableMotion, INeXusInfoWriteable

    def asynchronousMoveTo(self, position):
        if self.verbose:
            self.logger.info('asynchronousMoveTo(%r)...' % position)
        position = float(position)
        if self._operating_continuously:
            self._last_requested_position = position
        else:
            raise Exception()

    def atScanLineStart(self):
        self._binpointGrtPitch.atScanLineStart()
        self._binpointMirPitch.atScanLineStart()
        self._binpointPgmEnergy.atScanLineStart()
        self._binpointGrtPitch.collectData()
        self._binpointMirPitch.collectData()
        self._binpointPgmEnergy.collectData()
        
        (self.grating_density , _, self.grating_offset, self.plane_mirror_offset,  self.energy_calibration_gradient, 
         self.energy_calibration_reference) = self._move_controller.getPgmEnergyParameters()

    def atScanLineEnd(self):
        self._binpointGrtPitch.atScanLineEnd()
        self._binpointMirPitch.atScanLineEnd()
        self._binpointPgmEnergy.atScanLineEnd()
        # TODO: This race condition should be fixed in gda-8.44
        # There is a race condition here, where if the motion completes before all position callables
        # have been returned, the detector will be told to shut down.

    def getPosition(self):
        if self.verbose:
            self.logger.info('getPosition()...')
        if self._operating_continuously:
            raise Exception()
            # Should be using getPositionCallable
            #return self._last_requested_position
        else:
            raise Exception()

    def waitWhileBusy(self):
        if self.verbose:
            self.logger.info('waitWhileBusy()...')
        if self._operating_continuously:
            return # self._move_controller.waitWhileMoving()
        else:
            raise Exception()

    def isBusy(self):
        if self._operating_continuously:
            return False #self._move_controller.isBusy()
        else:
            raise Exception()

    # public interface ScannableMotion extends Scannable

    # Override: public interface Scannable extends Device

    # Note that neither stop() nor atCommandFailure() are called when operatingContinuously, however stopAndReset()
    # is called on the move_controller, so the move_controller needs to handle failures there.
    
    # We do need an atScanEnd() though, since unlike stop() and atCommandFailure(), stopAndReset() isn't called
    # when the scan line completes.
    def atScanEnd(self):
        if self.verbose: self.logger.info('atScanEnd()... _operating_continuously=%r' % self._operating_continuously)
        if self._operating_continuously:
            self._move_controller.atScanEnd()
        else:
            #raise Exception()
            self._move_controller.atScanEnd()
        """ Note, self._operating_continuously is being set back to false before atScanEnd is being called. See:
2015-02-04 21:43:26,833 INFO  ContinuousPgmEnergyScannable:egy - setOperatingContinuously(1) was 0
...
2015-02-04 21:43:27,048 INFO  ContinuousPgmEnergyScannable:egy - asynchronousMoveTo(841)...  
2015-02-04 21:43:27,048 INFO  ContinuousPgmEnergyScannable:egy - waitWhileBusy()...  
2015-02-04 21:43:27,048 INFO  ContinuousPgmEnergyScannable:egy - waitWhileBusy()...  
2015-02-04 21:43:27,048 INFO  ContinuousPgmEnergyScannable:egy - getPositionCallable()... last_requested_position=841.0  
...
2015-02-04 21:30:53,128 INFO  ContinuousPgmEnergyScannable:egy - setOperatingContinuously(0) was 1
2015-02-04 21:30:53,128 INFO  ContinuousPgmEnergyScannable:egy - atScanEnd()... _operating_continuously=0
"""

class EnergyCalculatingCallable(Callable):
    def __init__(self, 
               parent,       demand_position,       grtPitchCallable,       mirPitchCallable,       pgmEnergyCallable):
        (self._parent, self._demand_position, self._grtPitchCallable, self._mirPitchCallable, self._pgmEnergyCallable) = (
               parent,       demand_position,       grtPitchCallable,       mirPitchCallable,       pgmEnergyCallable)
    
    def call(self):
        grtPitch = self._grtPitchCallable.call()
        mirPitch = self._mirPitchCallable.call()
        pgmEnergy = self._pgmEnergyCallable.call()
        
        energy = angles2energy(gd       = self._parent.grating_density,
                               grang    = grtPitch, #/1000.,
                               pmang    = mirPitch, #/1000.,
                               groff    = self._parent.grating_offset,
                               pmoff    = self._parent.plane_mirror_offset,
                               ecg      = self._parent.energy_calibration_gradient,
                               ecr      = self._parent.energy_calibration_reference)
        self._parent.logger.info('angles2energy(gd=%r, grang=%r, pmang=%r, groff=%r, pmoff=%r, ecg=%r, ecr=%r) = %r' % (
            self._parent.grating_density, grtPitch, mirPitch, self._parent.grating_offset,
            self._parent.plane_mirror_offset, self._parent.energy_calibration_gradient, self._parent.energy_calibration_reference,
            energy))
        return energy, self._demand_position, self._demand_position-energy, pgmEnergy, pgmEnergy-energy
        # TODO: Calculate and return cff value.
        # Do we also want to return the motor positions too, given that using this
        # scannable prevents us from adding the binpoint scannables individually?
    
    @staticmethod
    def getPositionCallableExtraNames():
        return ['demand', 'diff', 'pgm_energy', 'diff']
    
    @staticmethod
    def getPositionCallableFormat():
        return ['%f', '%f', '%f', '%f', '%f']
