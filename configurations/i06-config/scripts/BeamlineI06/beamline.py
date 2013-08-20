from gda.configuration.properties import LocalProperties
from gda.jython.commands.GeneralCommands import run, alias

from gda.factory import Finder
from Diamond.Utility.BeamlineFunctions import BeamlineFunctionClass
from Diamond.Utility.ScriptLogger import ScriptLoggerClass;


finder = Finder.getInstance();

logger=ScriptLoggerClass();
i06=BeamlineFunctionClass('i06');
i06.setTerminalLogger();


print "-------------------------------------------------------------------"
print "Enable the setAlias/setGdaAlias functions"
print "Usage: "
print "     setAlias('aliasName', 'AliasedJythonExpression')"
print "or:"
print "     setGdaAlias('aliasName', 'AliasedJythonExpression')"
print "For example:"
print "    setGdaAlias('t1', 'testMotor1.moveTo(1)')"
print "will create an aliase 't1' command to move the testMotor1 to 1 effectively"


from Diamond.PseudoDevices.AliasDevice import AliasDeviceClass;

#Use the AliasDeviceClass to setup an alias
def setAlias(aliasName, gdaExpression):
    exec(aliasName+"=None") in globals();
    globals()[aliasName]=AliasDeviceClass(aliasName, gdaExpression);

#Use the GDA alias function to setup an alias
def setGdaAlias(aliasName, gdaExpression):
#    b="exec('"+gdaExpression+"') in globals()";
    a="def "+ aliasName + "():\n\t" + "exec('" + gdaExpression + "') in globals()" + "\n";
    exec(a) in globals();
    alias(aliasName);

def psg(sm):
    if not isinstance(sm, gda.device.scannable.scannablegroup.ScannableGroup):
        print "This device is not a 'ScannableGroup' type"
        return;
    
    for sn in sm.getGroupMemberNames():
        s=sm.getGroupMember(sn);
        print s;

alias("psg")


#Usage: 
#setAlias("t1", "testMotor1.moveTo(1)");

#setGdaAlias("t2", "testMotor1.moveTo(2)");


def lastscan():
#    return i06.getLastSrsScanFile("tmp")
    return i06.getLastScanFile();

def setTitle(title):
    i06.setTitle(title);
def settitle(title):
    i06.setTitle(title);

def getTitle():
    return i06.getTitle();

def gettitle():
    return i06.getTitle();

def setVisit(visit):
    i06.setVisit(visit);
    i06.setSubDir("");
    
def setvisit(visit):
    i06.setVisit(visit);
    i06.setSubDir("");

def getVisit():
    return i06.getVisit();
def getvisit():
    return i06.getVisit();

def setDir(newSubDir):
    i06.setSubDir(newSubDir);
def setdir(newSubDir):
    i06.setSubDir(newSubDir);
    


alias("lastscan")
alias("getTitle"); alias("gettitle")
alias("setTitle"); alias("settitle")
alias("getVisit"); alias("getvisit")
alias("setVisit"); alias("setvisit")
alias("setDir");   alias("setdir")


