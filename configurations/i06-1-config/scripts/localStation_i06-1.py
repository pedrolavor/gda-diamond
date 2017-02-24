
#localStation.py
#For beamline specific initialisation code.
print "===================================================================";
print "Performing Beamline I06 branch line specific initialisation code (localStation_i06-1.py).";
print

#Setup the environment variables
import java
import sys
from gda.configuration.properties import LocalProperties

localStationErrorCount=0

# try:
#     print "-------------------------------------------------------------------"
#     print "Set up the m6qgmax routing"
# 
#     execfile(gdaScriptDir + "BeamlineI06/m6qgmax.py");
# except:
#     exceptionType, exception, traceback=sys.exc_info();
#     print "XXXXXXXXXX:  m6qgmax Error "
#     logger.dump("---> ", exceptionType, exception, traceback)
#     localStationErrorCount+=1

try:
    print "-------------------------------------------------------------------"
    #print "Change the default output format to meet the branch line requirements"
    execfile(gdaScriptDir + "BeamlineI06/setOutputFormat_i06-1.py");
    
    #Group the hexapod legs into list
    m1legs = [m1leg1, m1leg2, m1leg3, m1leg4, m1leg5, m1leg6];
    m6legs = [m6leg1, m6leg2, m6leg3, m6leg4, m6leg5, m6leg6];
    m7legs = [m7leg1, m7leg2, m7leg3, m7leg4, m7leg5, m7leg6];
except:
    exceptionType, exception, traceback=sys.exc_info();
    print "XXXXXXXXXX:  Errors when running the localstation_i06.py"
    logger.dump("---> ", exceptionType, exception, traceback)
    localStationErrorCount+=1

print "-------------------------------------------------------------------"
print "Set up idio and ifio"

try:
    execfile(gdaScriptDir + "BeamlineI06/idivio.py");
except:
    exceptionType, exception, traceback=sys.exc_info();
    print "XXXXXXXXXX:  idivio Error "
    logger.dump("---> ", exceptionType, exception, traceback)
    localStationErrorCount+=1

print "-------------------------------------------------------------------"
print "Waveplate 3 (EC2) motor: wp32"

try:
    from Diamond.PseudoDevices.EpicsMotors import EpicsCallbackMotorClass
    wp32 = EpicsCallbackMotorClass('wp32', "BL06I-OP-WAVE-32:MTR", '%.4f');
except:
    exceptionType, exception, traceback=sys.exc_info();
    print "XXXXXXXXXX:  wp32 Error "
    logger.dump("---> ", exceptionType, exception, traceback)
    localStationErrorCount+=1


print "-------------------------------------------------------------------"
print "==================================================================="
print "Total number of localStation errors was", localStationErrorCount
print "==================================================================="