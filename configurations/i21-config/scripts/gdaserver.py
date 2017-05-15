''' gdaserver.py: generated by SpringObjectServer.writeFindablesJythonModule

Generated on server start, this Jython module 'gdaserver.py', in each config's
config/scripts directory, acts as a development-time reference for Findable
objects created by Spring XML. This trick enables PyDev auto-completion of
server-side GDA objects and their methods in the IDE and Pythonic import
syntax of multiple device in user scripts, e.g.:

>>> from gdaserver import gripper_x, gripper_grp as gripper_jaws

See Confluence for rationale: http://confluence.diamond.ac.uk/x/IwyvAw

PLEASE DO NOT COMMIT THIS FILE
You should ignore it in: config/scripts/.gitignore

ANY CHANGES WILL BE OVERWRITTEN WITHOUT WARNING

'''

# generation-time attributes
__beamline__ = 'I21'
__gdaversion__ = '9.4.0'
__xmlfile__ = '/scratch/gda_versions/gda_master/workspace_git/gda-dls-beamlines-i21.git/i21-config/servers/main/dummy/server.xml'
__pid__ = '25069'
__hostname__ = 'ws128.diamond.ac.uk'
__timestamp__ = '2017-05-15 14:31:26.546'

# get function (finder.find for now)
from gda.factory import Finder
get = Finder.getInstance().find
del Finder

# not executed so types not in: dir(gdaserver)
if False:
	
	# fake imports for fake assignments below
	from gda.commandqueue import FindableProcessorQueue
	from gda.data import ObservablePathConstructor
	from gda.data.fileregistrar import ClientFileAnnouncer
	from gda.data.fileregistrar import FileRegistrar
	from gda.data.metadata import GdaMetadata
	from gda.data.metadata import NXMetaDataProvider
	from gda.data.metadata import StoredMetadataEntry
	from gda.data.scan.datawriter import DefaultDataWriterFactory
	from gda.device.detector import NXDetector
	from gda.device.enumpositioner import DummyEnumPositioner
	from gda.device.insertiondevice import Apple2IDDummy
	from gda.device.insertiondevice import Apple2IDGapPolarPos
	from gda.device.monitor import DummyEpicsMonitorDouble
	from gda.device.motor import DummyMotor
	from gda.device.scannable import DummyScannable
	from gda.device.scannable import ScannableMotor
	from gda.device.scannable.scannablegroup import ScannableGroup
	from gda.jython import JythonServer
	from gda.util.findableHashtable import FindableHashtable
	from uk.ac.diamond.scisoft.analysis.plotserver import PlotServerBase
	
	# fake assignments for PyDev type-inference
	b2 = DummyEpicsMonitorDouble()
	cff = DummyScannable()
	client_file_announcer = ClientFileAnnouncer()
	command_server = JythonServer()
	commandQueueProcessor = FindableProcessorQueue()
	d1 = ScannableGroup()
	d1cam = NXDetector()
	d1motor = DummyMotor()
	d1pos = DummyEnumPositioner()
	d1stick = ScannableMotor()
	d2 = ScannableGroup()
	d2cam = NXDetector()
	d2motor = DummyMotor()
	d2pos = DummyEnumPositioner()
	d2stick = ScannableMotor()
	d3a = ScannableGroup()
	d3acam = NXDetector()
	d3afemto = DummyEpicsMonitorDouble()
	d3amotor = DummyMotor()
	d3apos = DummyEnumPositioner()
	d3astick = ScannableMotor()
	d3b = ScannableGroup()
	d3bfemto = DummyEpicsMonitorDouble()
	d3bmotor = DummyMotor()
	d3bpos = DummyEnumPositioner()
	d3bstick = ScannableMotor()
	d4 = ScannableGroup()
	d4cam = NXDetector()
	d4femto = DummyEpicsMonitorDouble()
	d4motor = DummyMotor()
	d4pos = DummyEnumPositioner()
	d4stick = ScannableMotor()
	d7 = ScannableGroup()
	d7femto1 = DummyEpicsMonitorDouble()
	d7femto2 = DummyEpicsMonitorDouble()
	d7gascell = ScannableMotor()
	d7motor = DummyMotor()
	d8 = ScannableGroup()
	d8cam = NXDetector()
	d8femto1 = DummyEpicsMonitorDouble()
	d8motor = DummyMotor()
	d8stick = ScannableMotor()
	DefaultDataWriterFactory = DefaultDataWriterFactory()
	dgn = ScannableGroup()
	dgncam = NXDetector()
	dgnmotor = DummyMotor()
	dgnpos = DummyEnumPositioner()
	dgnstick = ScannableMotor()
	diodetth = ScannableMotor()
	diodetthMotor = DummyMotor()
	draincurrent = DummyEpicsMonitorDouble()
	eref = DummyScannable()
	feShutter = DummyEnumPositioner()
	FileRegistrar = FileRegistrar()
	fixdiode1 = DummyEpicsMonitorDouble()
	fixdiode2 = DummyEpicsMonitorDouble()
	fy1 = DummyEpicsMonitorDouble()
	gauge01 = DummyEpicsMonitorDouble()
	gauge02 = DummyEpicsMonitorDouble()
	gauge03 = DummyEpicsMonitorDouble()
	gauge04 = DummyEpicsMonitorDouble()
	gauge05 = DummyEpicsMonitorDouble()
	gauge06 = DummyEpicsMonitorDouble()
	gauge07 = DummyEpicsMonitorDouble()
	gauge08 = DummyEpicsMonitorDouble()
	gauges = ScannableGroup()
	GDAHashtable = FindableHashtable()
	GDAMetadata = GdaMetadata()
	id = ScannableGroup()
	idcontrol = Apple2IDDummy()
	idgap = ScannableMotor()
	idgapMotor = DummyMotor()
	idscannable = Apple2IDGapPolarPos()
	m1 = ScannableGroup()
	m1height = ScannableMotor()
	m1heightMotor = DummyMotor()
	m1pitch = ScannableMotor()
	m1pitchMotor = DummyMotor()
	m1roll = ScannableMotor()
	m1rollMotor = DummyMotor()
	m1temp1 = DummyEpicsMonitorDouble()
	m1x = ScannableMotor()
	m1x1Cone = ScannableMotor()
	m1x1ConeMotor = DummyMotor()
	m1x2flatVee = ScannableMotor()
	m1x2flatVeeMotor = DummyMotor()
	m1xMotor = DummyMotor()
	m1y1Cone = ScannableMotor()
	m1y1ConeMotor = DummyMotor()
	m1y2Vee = ScannableMotor()
	m1y2VeeMotor = DummyMotor()
	m1y3flat = ScannableMotor()
	m1y3flatMotor = DummyMotor()
	m1yaw = ScannableMotor()
	m1yawMotor = DummyMotor()
	m2 = ScannableGroup()
	m2height = ScannableMotor()
	m2heightMotor = DummyMotor()
	m2pitch = ScannableMotor()
	m2pitchMotor = DummyMotor()
	m2roll = ScannableMotor()
	m2rollMotor = DummyMotor()
	m2temp1 = DummyEpicsMonitorDouble()
	m2temp2 = DummyEpicsMonitorDouble()
	m2temp3 = DummyEpicsMonitorDouble()
	m2x = ScannableMotor()
	m2x1Cone = ScannableMotor()
	m2x1ConeMotor = DummyMotor()
	m2x2flatVee = ScannableMotor()
	m2x2flatVeeMotor = DummyMotor()
	m2xMotor = DummyMotor()
	m2y1Cone = ScannableMotor()
	m2y1ConeMotor = DummyMotor()
	m2y2Vee = ScannableMotor()
	m2y2VeeMotor = DummyMotor()
	m2y3flat = ScannableMotor()
	m2y3flatMotor = DummyMotor()
	m2yaw = ScannableMotor()
	m2yawMotor = DummyMotor()
	m2yRotMotor = DummyMotor()
	m4 = ScannableGroup()
	m4femto1 = DummyEpicsMonitorDouble()
	m4femto2 = DummyEpicsMonitorDouble()
	m4longy = ScannableMotor()
	m4rx = ScannableMotor()
	m4ry = ScannableMotor()
	m4rz = ScannableMotor()
	m4VerticalStage = DummyMotor()
	m4x = ScannableMotor()
	m4xRotMotor = DummyMotor()
	m4xTransMotor = DummyMotor()
	m4y = ScannableMotor()
	m4yTransMotor = DummyMotor()
	m4z = ScannableMotor()
	m4zRotMotor = DummyMotor()
	m4zTransMotor = DummyMotor()
	m5 = ScannableGroup()
	m5hqrx = ScannableMotor()
	m5hqrxMotor = DummyMotor()
	m5hqry = ScannableMotor()
	m5hqryMotor = DummyMotor()
	m5hqrz = ScannableMotor()
	m5hqrzMotor = DummyMotor()
	m5hqx = ScannableMotor()
	m5hqxt = DummyMotor()
	m5hqy = ScannableMotor()
	m5hqyt = DummyMotor()
	m5hqz = ScannableMotor()
	m5hqzt = DummyMotor()
	m5longy = ScannableMotor()
	m5lqrx = ScannableMotor()
	m5lqrxMotor = DummyMotor()
	m5lqry = ScannableMotor()
	m5lqryMotor = DummyMotor()
	m5lqrz = ScannableMotor()
	m5lqrzMotor = DummyMotor()
	m5lqx = ScannableMotor()
	m5lqxt = DummyMotor()
	m5lqy = ScannableMotor()
	m5lqyt = DummyMotor()
	m5lqz = ScannableMotor()
	m5lqzt = DummyMotor()
	m5rstageMotor = DummyMotor()
	m5tth = ScannableMotor()
	m5vstageMotor = DummyMotor()
	m_pgm = DummyScannable()
	metashop = NXMetaDataProvider()
	n_pgm = DummyScannable()
	pgm = ScannableGroup()
	pgmB2Shadow = ScannableMotor()
	pgmB2ShadowMotor = DummyMotor()
	pgmEnergy = ScannableMotor()
	pgmEnergyMotor = DummyMotor()
	pgmGratingPitch = ScannableMotor()
	pgmGratingPitchMotor = DummyMotor()
	pgmGratingSelect = DummyEnumPositioner()
	pgmGratingSelectMotor = DummyMotor()
	pgmGratingSelectReal = ScannableMotor()
	pgmMirrorPitch = ScannableMotor()
	pgmMirrorPitchMotor = DummyMotor()
	pgmMirrorSelect = DummyEnumPositioner()
	pgmMirrorSelectMotor = DummyMotor()
	pgmMirrorSelectReal = ScannableMotor()
	plot_server = PlotServerBase()
	ring = ScannableGroup()
	ringCurrent = DummyEpicsMonitorDouble()
	ringEnergy = DummyEpicsMonitorDouble()
	rotatingdiode = DummyEpicsMonitorDouble()
	s1 = ScannableGroup()
	s1hcentre = ScannableMotor()
	s1hcentreMotor = DummyMotor()
	s1hsize = ScannableMotor()
	s1hsizeMotor = DummyMotor()
	s1lower = ScannableMotor()
	s1lowerMotor = DummyMotor()
	s1nearside = ScannableMotor()
	s1nearsideMotor = DummyMotor()
	s1offside = ScannableMotor()
	s1offsideMotor = DummyMotor()
	s1upper = ScannableMotor()
	s1upperMotor = DummyMotor()
	s1vcentre = ScannableMotor()
	s1vcentreMotor = DummyMotor()
	s1vsize = ScannableMotor()
	s1vsizeMotor = DummyMotor()
	s2 = ScannableGroup()
	s2femto1 = DummyEpicsMonitorDouble()
	s2femto2 = DummyEpicsMonitorDouble()
	s2femto3 = DummyEpicsMonitorDouble()
	s2femto4 = DummyEpicsMonitorDouble()
	s2hcentre = ScannableMotor()
	s2hcentreMotor = DummyMotor()
	s2hsize = ScannableMotor()
	s2hsizeMotor = DummyMotor()
	s2lower = ScannableMotor()
	s2lowerMotor = DummyMotor()
	s2nearside = ScannableMotor()
	s2nearsideMotor = DummyMotor()
	s2offside = ScannableMotor()
	s2offsideMotor = DummyMotor()
	s2upper = ScannableMotor()
	s2upperMotor = DummyMotor()
	s2vcentre = ScannableMotor()
	s2vcentreMotor = DummyMotor()
	s2vsize = ScannableMotor()
	s2vsizeMotor = DummyMotor()
	s3 = ScannableGroup()
	s3femto1 = DummyEpicsMonitorDouble()
	s3femto2 = DummyEpicsMonitorDouble()
	s3femto3 = DummyEpicsMonitorDouble()
	s3femto4 = DummyEpicsMonitorDouble()
	s3hcentre = ScannableMotor()
	s3hcentreMotor = DummyMotor()
	s3hsize = ScannableMotor()
	s3hsizeMotor = DummyMotor()
	s3lower = ScannableMotor()
	s3lowerMotor = DummyMotor()
	s3nearside = ScannableMotor()
	s3nearsideMotor = DummyMotor()
	s3offside = ScannableMotor()
	s3offsideMotor = DummyMotor()
	s3upper = ScannableMotor()
	s3upperMotor = DummyMotor()
	s3vcentre = ScannableMotor()
	s3vcentreMotor = DummyMotor()
	s3vsize = ScannableMotor()
	s3vsizeMotor = DummyMotor()
	s4 = ScannableGroup()
	s4femto1 = DummyEpicsMonitorDouble()
	s4femto2 = DummyEpicsMonitorDouble()
	s4femto3 = DummyEpicsMonitorDouble()
	s4femto4 = DummyEpicsMonitorDouble()
	s4hcentre = ScannableMotor()
	s4hcentreMotor = DummyMotor()
	s4hsize = ScannableMotor()
	s4hsizeMotor = DummyMotor()
	s4lower = ScannableMotor()
	s4lowerMotor = DummyMotor()
	s4nearside = ScannableMotor()
	s4nearsideMotor = DummyMotor()
	s4offside = ScannableMotor()
	s4offsideMotor = DummyMotor()
	s4upper = ScannableMotor()
	s4upperMotor = DummyMotor()
	s4vcentre = ScannableMotor()
	s4vcentreMotor = DummyMotor()
	s4vsize = ScannableMotor()
	s4vsizeMotor = DummyMotor()
	s5 = ScannableGroup()
	s5hdso = ScannableMotor()
	s5hdsoMotor = DummyMotor()
	s5hgap = ScannableMotor()
	s5hgapMotor = DummyMotor()
	s5sut = ScannableMotor()
	s5sutMotor = DummyMotor()
	s5v1gap = ScannableMotor()
	s5v1gapMotor = DummyMotor()
	s5v2gap = ScannableMotor()
	s5v2gapMotor = DummyMotor()
	s5vdso1 = ScannableMotor()
	s5vdso1Motor = DummyMotor()
	s5vdso2 = ScannableMotor()
	s5vdso2Motor = DummyMotor()
	s6 = ScannableGroup()
	s6bottom = ScannableMotor()
	s6bottomMotor = DummyMotor()
	s6hcentre = ScannableMotor()
	s6hcentreMotor = DummyMotor()
	s6hgap = ScannableMotor()
	s6hgapMotor = DummyMotor()
	s6nearside = ScannableMotor()
	s6nearsideMotor = DummyMotor()
	s6offside = ScannableMotor()
	s6offsideMotor = DummyMotor()
	s6top = ScannableMotor()
	s6topMotor = DummyMotor()
	s6vcentre = ScannableMotor()
	s6vcentreMotor = DummyMotor()
	s6vgap = ScannableMotor()
	s6vgapMotor = DummyMotor()
	saazimuth = ScannableMotor()
	sapolar = ScannableMotor()
	satilt = ScannableMotor()
	sax = ScannableMotor()
	say = ScannableMotor()
	saz = ScannableMotor()
	sgm = ScannableGroup()
	sgmgratingpitchMotor = DummyMotor()
	sgmgratingtranslationMotor = DummyMotor()
	sgmheightMotor = DummyMotor()
	sgmlongxMotor = DummyMotor()
	sgmpitch = ScannableMotor()
	sgmr1 = ScannableMotor()
	sgmroll = ScannableMotor()
	sgmrollMotor = DummyMotor()
	sgmwedgenearside = ScannableMotor()
	sgmwedgenearsideMotor = DummyMotor()
	sgmwedgeoffside = ScannableMotor()
	sgmwedgeoffsideMotor = DummyMotor()
	sgmx = ScannableMotor()
	sgmy = ScannableMotor()
	simcam = NXDetector()
	smp = ScannableGroup()
	smpazimuthMotor = DummyMotor()
	smplcam1 = NXDetector()
	smplcam2 = NXDetector()
	smplcam3 = NXDetector()
	smplcam4 = NXDetector()
	smprzMotor = DummyMotor()
	smptiltMotor = DummyMotor()
	smpxMotor = DummyMotor()
	smpyMotor = DummyMotor()
	smpzMotor = DummyMotor()
	specgamma = ScannableMotor()
	specgammaMotor = DummyMotor()
	spectrometer = ScannableGroup()
	specx = ScannableMotor()
	specxMotor = DummyMotor()
	specz = ScannableMotor()
	speczMotor = DummyMotor()
	straightdiode = DummyEpicsMonitorDouble()
	subdirectory = StoredMetadataEntry()
	terminallog_path_provider = ObservablePathConstructor()
	timeToRefill = DummyEpicsMonitorDouble()
	tthdiode = DummyEpicsMonitorDouble()

# real assignments of module-level attributes
b2 = get("b2")
cff = get("cff")
client_file_announcer = get("client_file_announcer")
command_server = get("command_server")
commandQueueProcessor = get("commandQueueProcessor")
d1 = get("d1")
d1cam = get("d1cam")
d1motor = get("d1motor")
d1pos = get("d1pos")
d1stick = get("d1stick")
d2 = get("d2")
d2cam = get("d2cam")
d2motor = get("d2motor")
d2pos = get("d2pos")
d2stick = get("d2stick")
d3a = get("d3a")
d3acam = get("d3acam")
d3afemto = get("d3afemto")
d3amotor = get("d3amotor")
d3apos = get("d3apos")
d3astick = get("d3astick")
d3b = get("d3b")
d3bfemto = get("d3bfemto")
d3bmotor = get("d3bmotor")
d3bpos = get("d3bpos")
d3bstick = get("d3bstick")
d4 = get("d4")
d4cam = get("d4cam")
d4femto = get("d4femto")
d4motor = get("d4motor")
d4pos = get("d4pos")
d4stick = get("d4stick")
d7 = get("d7")
d7femto1 = get("d7femto1")
d7femto2 = get("d7femto2")
d7gascell = get("d7gascell")
d7motor = get("d7motor")
d8 = get("d8")
d8cam = get("d8cam")
d8femto1 = get("d8femto1")
d8motor = get("d8motor")
d8stick = get("d8stick")
DefaultDataWriterFactory = get("DefaultDataWriterFactory")
dgn = get("dgn")
dgncam = get("dgncam")
dgnmotor = get("dgnmotor")
dgnpos = get("dgnpos")
dgnstick = get("dgnstick")
diodetth = get("diodetth")
diodetthMotor = get("diodetthMotor")
draincurrent = get("draincurrent")
eref = get("eref")
feShutter = get("feShutter")
FileRegistrar = get("FileRegistrar")
fixdiode1 = get("fixdiode1")
fixdiode2 = get("fixdiode2")
fy1 = get("fy1")
gauge01 = get("gauge01")
gauge02 = get("gauge02")
gauge03 = get("gauge03")
gauge04 = get("gauge04")
gauge05 = get("gauge05")
gauge06 = get("gauge06")
gauge07 = get("gauge07")
gauge08 = get("gauge08")
gauges = get("gauges")
GDAHashtable = get("GDAHashtable")
GDAMetadata = get("GDAMetadata")
id = get("id")
idcontrol = get("idcontrol")
idgap = get("idgap")
idgapMotor = get("idgapMotor")
idscannable = get("idscannable")
m1 = get("m1")
m1height = get("m1height")
m1heightMotor = get("m1heightMotor")
m1pitch = get("m1pitch")
m1pitchMotor = get("m1pitchMotor")
m1roll = get("m1roll")
m1rollMotor = get("m1rollMotor")
m1temp1 = get("m1temp1")
m1x = get("m1x")
m1x1Cone = get("m1x1Cone")
m1x1ConeMotor = get("m1x1ConeMotor")
m1x2flatVee = get("m1x2flatVee")
m1x2flatVeeMotor = get("m1x2flatVeeMotor")
m1xMotor = get("m1xMotor")
m1y1Cone = get("m1y1Cone")
m1y1ConeMotor = get("m1y1ConeMotor")
m1y2Vee = get("m1y2Vee")
m1y2VeeMotor = get("m1y2VeeMotor")
m1y3flat = get("m1y3flat")
m1y3flatMotor = get("m1y3flatMotor")
m1yaw = get("m1yaw")
m1yawMotor = get("m1yawMotor")
m2 = get("m2")
m2height = get("m2height")
m2heightMotor = get("m2heightMotor")
m2pitch = get("m2pitch")
m2pitchMotor = get("m2pitchMotor")
m2roll = get("m2roll")
m2rollMotor = get("m2rollMotor")
m2temp1 = get("m2temp1")
m2temp2 = get("m2temp2")
m2temp3 = get("m2temp3")
m2x = get("m2x")
m2x1Cone = get("m2x1Cone")
m2x1ConeMotor = get("m2x1ConeMotor")
m2x2flatVee = get("m2x2flatVee")
m2x2flatVeeMotor = get("m2x2flatVeeMotor")
m2xMotor = get("m2xMotor")
m2y1Cone = get("m2y1Cone")
m2y1ConeMotor = get("m2y1ConeMotor")
m2y2Vee = get("m2y2Vee")
m2y2VeeMotor = get("m2y2VeeMotor")
m2y3flat = get("m2y3flat")
m2y3flatMotor = get("m2y3flatMotor")
m2yaw = get("m2yaw")
m2yawMotor = get("m2yawMotor")
m2yRotMotor = get("m2yRotMotor")
m4 = get("m4")
m4femto1 = get("m4femto1")
m4femto2 = get("m4femto2")
m4longy = get("m4longy")
m4rx = get("m4rx")
m4ry = get("m4ry")
m4rz = get("m4rz")
m4VerticalStage = get("m4VerticalStage")
m4x = get("m4x")
m4xRotMotor = get("m4xRotMotor")
m4xTransMotor = get("m4xTransMotor")
m4y = get("m4y")
m4yTransMotor = get("m4yTransMotor")
m4z = get("m4z")
m4zRotMotor = get("m4zRotMotor")
m4zTransMotor = get("m4zTransMotor")
m5 = get("m5")
m5hqrx = get("m5hqrx")
m5hqrxMotor = get("m5hqrxMotor")
m5hqry = get("m5hqry")
m5hqryMotor = get("m5hqryMotor")
m5hqrz = get("m5hqrz")
m5hqrzMotor = get("m5hqrzMotor")
m5hqx = get("m5hqx")
m5hqxt = get("m5hqxt")
m5hqy = get("m5hqy")
m5hqyt = get("m5hqyt")
m5hqz = get("m5hqz")
m5hqzt = get("m5hqzt")
m5longy = get("m5longy")
m5lqrx = get("m5lqrx")
m5lqrxMotor = get("m5lqrxMotor")
m5lqry = get("m5lqry")
m5lqryMotor = get("m5lqryMotor")
m5lqrz = get("m5lqrz")
m5lqrzMotor = get("m5lqrzMotor")
m5lqx = get("m5lqx")
m5lqxt = get("m5lqxt")
m5lqy = get("m5lqy")
m5lqyt = get("m5lqyt")
m5lqz = get("m5lqz")
m5lqzt = get("m5lqzt")
m5rstageMotor = get("m5rstageMotor")
m5tth = get("m5tth")
m5vstageMotor = get("m5vstageMotor")
m_pgm = get("m_pgm")
metashop = get("metashop")
n_pgm = get("n_pgm")
pgm = get("pgm")
pgmB2Shadow = get("pgmB2Shadow")
pgmB2ShadowMotor = get("pgmB2ShadowMotor")
pgmEnergy = get("pgmEnergy")
pgmEnergyMotor = get("pgmEnergyMotor")
pgmGratingPitch = get("pgmGratingPitch")
pgmGratingPitchMotor = get("pgmGratingPitchMotor")
pgmGratingSelect = get("pgmGratingSelect")
pgmGratingSelectMotor = get("pgmGratingSelectMotor")
pgmGratingSelectReal = get("pgmGratingSelectReal")
pgmMirrorPitch = get("pgmMirrorPitch")
pgmMirrorPitchMotor = get("pgmMirrorPitchMotor")
pgmMirrorSelect = get("pgmMirrorSelect")
pgmMirrorSelectMotor = get("pgmMirrorSelectMotor")
pgmMirrorSelectReal = get("pgmMirrorSelectReal")
plot_server = get("plot_server")
ring = get("ring")
ringCurrent = get("ringCurrent")
ringEnergy = get("ringEnergy")
rotatingdiode = get("rotatingdiode")
s1 = get("s1")
s1hcentre = get("s1hcentre")
s1hcentreMotor = get("s1hcentreMotor")
s1hsize = get("s1hsize")
s1hsizeMotor = get("s1hsizeMotor")
s1lower = get("s1lower")
s1lowerMotor = get("s1lowerMotor")
s1nearside = get("s1nearside")
s1nearsideMotor = get("s1nearsideMotor")
s1offside = get("s1offside")
s1offsideMotor = get("s1offsideMotor")
s1upper = get("s1upper")
s1upperMotor = get("s1upperMotor")
s1vcentre = get("s1vcentre")
s1vcentreMotor = get("s1vcentreMotor")
s1vsize = get("s1vsize")
s1vsizeMotor = get("s1vsizeMotor")
s2 = get("s2")
s2femto1 = get("s2femto1")
s2femto2 = get("s2femto2")
s2femto3 = get("s2femto3")
s2femto4 = get("s2femto4")
s2hcentre = get("s2hcentre")
s2hcentreMotor = get("s2hcentreMotor")
s2hsize = get("s2hsize")
s2hsizeMotor = get("s2hsizeMotor")
s2lower = get("s2lower")
s2lowerMotor = get("s2lowerMotor")
s2nearside = get("s2nearside")
s2nearsideMotor = get("s2nearsideMotor")
s2offside = get("s2offside")
s2offsideMotor = get("s2offsideMotor")
s2upper = get("s2upper")
s2upperMotor = get("s2upperMotor")
s2vcentre = get("s2vcentre")
s2vcentreMotor = get("s2vcentreMotor")
s2vsize = get("s2vsize")
s2vsizeMotor = get("s2vsizeMotor")
s3 = get("s3")
s3femto1 = get("s3femto1")
s3femto2 = get("s3femto2")
s3femto3 = get("s3femto3")
s3femto4 = get("s3femto4")
s3hcentre = get("s3hcentre")
s3hcentreMotor = get("s3hcentreMotor")
s3hsize = get("s3hsize")
s3hsizeMotor = get("s3hsizeMotor")
s3lower = get("s3lower")
s3lowerMotor = get("s3lowerMotor")
s3nearside = get("s3nearside")
s3nearsideMotor = get("s3nearsideMotor")
s3offside = get("s3offside")
s3offsideMotor = get("s3offsideMotor")
s3upper = get("s3upper")
s3upperMotor = get("s3upperMotor")
s3vcentre = get("s3vcentre")
s3vcentreMotor = get("s3vcentreMotor")
s3vsize = get("s3vsize")
s3vsizeMotor = get("s3vsizeMotor")
s4 = get("s4")
s4femto1 = get("s4femto1")
s4femto2 = get("s4femto2")
s4femto3 = get("s4femto3")
s4femto4 = get("s4femto4")
s4hcentre = get("s4hcentre")
s4hcentreMotor = get("s4hcentreMotor")
s4hsize = get("s4hsize")
s4hsizeMotor = get("s4hsizeMotor")
s4lower = get("s4lower")
s4lowerMotor = get("s4lowerMotor")
s4nearside = get("s4nearside")
s4nearsideMotor = get("s4nearsideMotor")
s4offside = get("s4offside")
s4offsideMotor = get("s4offsideMotor")
s4upper = get("s4upper")
s4upperMotor = get("s4upperMotor")
s4vcentre = get("s4vcentre")
s4vcentreMotor = get("s4vcentreMotor")
s4vsize = get("s4vsize")
s4vsizeMotor = get("s4vsizeMotor")
s5 = get("s5")
s5hdso = get("s5hdso")
s5hdsoMotor = get("s5hdsoMotor")
s5hgap = get("s5hgap")
s5hgapMotor = get("s5hgapMotor")
s5sut = get("s5sut")
s5sutMotor = get("s5sutMotor")
s5v1gap = get("s5v1gap")
s5v1gapMotor = get("s5v1gapMotor")
s5v2gap = get("s5v2gap")
s5v2gapMotor = get("s5v2gapMotor")
s5vdso1 = get("s5vdso1")
s5vdso1Motor = get("s5vdso1Motor")
s5vdso2 = get("s5vdso2")
s5vdso2Motor = get("s5vdso2Motor")
s6 = get("s6")
s6bottom = get("s6bottom")
s6bottomMotor = get("s6bottomMotor")
s6hcentre = get("s6hcentre")
s6hcentreMotor = get("s6hcentreMotor")
s6hgap = get("s6hgap")
s6hgapMotor = get("s6hgapMotor")
s6nearside = get("s6nearside")
s6nearsideMotor = get("s6nearsideMotor")
s6offside = get("s6offside")
s6offsideMotor = get("s6offsideMotor")
s6top = get("s6top")
s6topMotor = get("s6topMotor")
s6vcentre = get("s6vcentre")
s6vcentreMotor = get("s6vcentreMotor")
s6vgap = get("s6vgap")
s6vgapMotor = get("s6vgapMotor")
saazimuth = get("saazimuth")
sapolar = get("sapolar")
satilt = get("satilt")
sax = get("sax")
say = get("say")
saz = get("saz")
sgm = get("sgm")
sgmgratingpitchMotor = get("sgmgratingpitchMotor")
sgmgratingtranslationMotor = get("sgmgratingtranslationMotor")
sgmheightMotor = get("sgmheightMotor")
sgmlongxMotor = get("sgmlongxMotor")
sgmpitch = get("sgmpitch")
sgmr1 = get("sgmr1")
sgmroll = get("sgmroll")
sgmrollMotor = get("sgmrollMotor")
sgmwedgenearside = get("sgmwedgenearside")
sgmwedgenearsideMotor = get("sgmwedgenearsideMotor")
sgmwedgeoffside = get("sgmwedgeoffside")
sgmwedgeoffsideMotor = get("sgmwedgeoffsideMotor")
sgmx = get("sgmx")
sgmy = get("sgmy")
simcam = get("simcam")
smp = get("smp")
smpazimuthMotor = get("smpazimuthMotor")
smplcam1 = get("smplcam1")
smplcam2 = get("smplcam2")
smplcam3 = get("smplcam3")
smplcam4 = get("smplcam4")
smprzMotor = get("smprzMotor")
smptiltMotor = get("smptiltMotor")
smpxMotor = get("smpxMotor")
smpyMotor = get("smpyMotor")
smpzMotor = get("smpzMotor")
specgamma = get("specgamma")
specgammaMotor = get("specgammaMotor")
spectrometer = get("spectrometer")
specx = get("specx")
specxMotor = get("specxMotor")
specz = get("specz")
speczMotor = get("speczMotor")
straightdiode = get("straightdiode")
subdirectory = get("subdirectory")
terminallog_path_provider = get("terminallog_path_provider")
timeToRefill = get("timeToRefill")
tthdiode = get("tthdiode")
# so you can import identifiers instead of strings

# don't leak get function
del get
