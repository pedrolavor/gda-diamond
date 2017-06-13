from gda.device.scannable import ScannableBase
from uk.ac.diamond.daq.persistence.jythonshelf import LocalParameters
from org.apache.commons.configuration import XMLConfiguration
from gda.jython.commands.ScannableCommands import pos
class SaveAndReload(object):
    def __init__(self, name, listOfScannables=[]):
        if listOfScannables == []:
            scannable_group = finder.find(name)
            nameslist = scannable_group.getGroupMemberNames()
            self.listOfScannables=[]
            for scname in nameslist:
                self.listOfScannables.append(scannable_group.getGroupMember(scname)) 
        else:
            self.listOfScannables = listOfScannables
        self.rootElementName = name+"Positions"
        self.config=LocalParameters.getXMLConfiguration(name+ "Positions")
    def save(self):
        for scannable in self.listOfScannables:
            self.config.setProperty(scannable.getName(), scannable.getPosition())
        self.config.save()
        
    def load(self):
        positionsList=[]
        for scannable in self.listOfScannables:
            pos1 = self.config.getProperty(scannable.getName())
            pos([scannable, pos1])
            positionsList.append(pos1)
        return positionsList

    def list(self):
        printList= ""
        for scannable in self.listOfScannables:
            pos1 = self.config.getProperty(scannable.getName())
            printList  += scannable.getName() +  " " + str(pos1)+"\n"
        print printList