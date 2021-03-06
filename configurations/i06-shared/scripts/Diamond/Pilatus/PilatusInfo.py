
class PilatusInfo(object):
	PILATUS_TYPE_100K_SOCKET, PILATUS_TYPE_100K_EPICS, PILATUS_TYPE_2M_SOCKET, PILATUS_TYPE_2M_EPICS = range(4);
	PILATUS_MODEL_100K, PILATUS_MODEL_2M = range(2);
	DETECTOR_STATUS_IDLE, DETECTOR_STATUS_BUSY, DETECTOR_STATUS_PAUSED, DETECTOR_STATUS_STANDBY, DETECTOR_STATUS_FAULT, DETECTOR_STATUS_MONITORING = range(6);
	EPICS_GAIN_THRESHOLD = ['7-30KeV/LowG', '5-18KeV/MediumG', '3-6KeV/HighG', '2-5KeV/UltraG'] 
	GAIN_THRESHOLD = ['lowG', 'midG', 'highG', 'ultraG']
