from gda.util import ElogEntry
from gda.data.metadata import GDAMetadataProvider

def setTitle(title):
    GDAMetadataProvider.getInstance().setMetadataValue("title", title)

def getTitle():
    return GDAMetadataProvider.getInstance().getMetadataValue("title")

def setVisit(visit):
    user=GDAMetadataProvider.getInstance().getMetadataValue("federalid")
    if user in ["i06user", "i07user", "i11user", "i22user"]:
        oldvisit = GDAMetadataProvider.getInstance().getMetadataValue("visit")
        try:
            ElogEntry.post("visit manually changed from %s to %s by %s" % (oldvisit, visit, user), "", "gda", None, "BLI07", "BLI07-USR", None)
        except:
            pass
    GDAMetadataProvider.getInstance().setMetadataValue("visit", visit)

def getVisit():
    return GDAMetadataProvider.getInstance().getMetadataValue("visit")

alias("getTitle");
alias("setTitle");
alias("getVisit");
alias("setVisit");

