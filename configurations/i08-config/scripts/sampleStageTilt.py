from org.jscience.physics.quantities import Quantity
from org.jscience.physics.units import SI
from gda.factory import Finder

def setOffset(axis, offset):
    offset_quantity = Quantity.valueOf(offset, SI.MILLI(SI.METER))
    Finder.getInstance().find(axis.getName()).setOffset(offset_quantity)
    
def getOffset(axis):
    sc_MicroFocusSampleStage = Finder.getInstance().find("sc_MicroFocusSampleStage")
    return sc_MicroFocusSampleStage.getPositionOffset(axis.dofname)

def showStage():
    sc_MicroFocusSampleX = Finder.getInstance().find("sc_MicroFocusSampleX")
    sc_MicroFocusSampleY = Finder.getInstance().find("sc_MicroFocusSampleY")
    sc_sample_y1 = Finder.getInstance().find("sc_sample_y1")
    sc_sample_y2 = Finder.getInstance().find("sc_sample_y2")
    sc_sample_y3 = Finder.getInstance().find("sc_sample_y3")
    y1_motor = Finder.getInstance().find("sample_y1_motor")
    y2_motor = Finder.getInstance().find("sample_y2_motor")
    y3_motor = Finder.getInstance().find("sample_y3_motor")
    print "Stage Status:"
    print "\t (X,Y) = (%s, %s) " % (sc_MicroFocusSampleX.getPosition(), sc_MicroFocusSampleY.getPosition())
    print "\t (Y1,Y2,Y3) = (%s, %s, %s)" % (sc_sample_y1.getPosition(), sc_sample_y2.getPosition(), sc_sample_y3.getPosition())
    print "\t Actual (Y1,Y2,Y3) = (%s, %s, %s)" % (y1_motor.getPosition(), y2_motor.getPosition(), y3_motor.getPosition())

def resetOffsets():
    sc_sample_y1 = Finder.getInstance().find("sc_sample_y1")
    sc_sample_y2 = Finder.getInstance().find("sc_sample_y2")
    sc_sample_y3 = Finder.getInstance().find("sc_sample_y3")
    setOffset(sc_sample_y1, 0.0)
    setOffset(sc_sample_y2, 0.0)
    setOffset(sc_sample_y3, 0.0)
    
def listOffsets():
    sc_sample_y1 = Finder.getInstance().find("sc_sample_y1")
    sc_sample_y2 = Finder.getInstance().find("sc_sample_y2")
    sc_sample_y3 = Finder.getInstance().find("sc_sample_y3")
    print "Stage Offsets:"
    print "\t Y1 Offset :%s" % sc_sample_y1.getOffset()
    print "\t Y2 Offset :%s" % sc_sample_y2.getOffset()
    print "\t Y3 Offset :%s" % sc_sample_y3.getOffset()
    
def helpTilt():
    print "The available commands are:"
    print "\t showStage()"
    print "\t listOffsets()"
    print "\t setOffset(axis,offset)"
    print "\t \t e.g. setOffset(sample_y1, 0.24)"
    print "\t resetOffsets()"
