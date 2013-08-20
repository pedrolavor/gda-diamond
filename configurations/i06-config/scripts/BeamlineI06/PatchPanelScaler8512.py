
#from Diamond.PseudoDevices.Scaler8512DirectPV import ScalerChannelEpicsPVClass;
from Diamond.PseudoDevices.Scaler8512Device import Scaler8512ChannelEpicsDeviceClass;
from Diamond.PseudoDevices.Scaler8512Device import DetectorIntegrationsDevice;

#Both Patch Panel U1 and U2 use the same scaler preset/trigger signal from the same scaler card
pvPatchPanelScalerTP='BL06I-DI-8512-02:PRESET';
pvPatchPanelScalerCNT='BL06I-DI-8512-02:STARTCOUNT';

#For Patch Panel U2
#Use the scaler Raw count
pvCA61CRAW = 'BL06J-EA-USER-01:SC1-RAW';
pvCA62CRAW = 'BL06J-EA-USER-01:SC2-RAW';
pvCA63CRAW = 'BL06J-EA-USER-01:SC3-RAW';
pvCA64CRAW = 'BL06J-EA-USER-01:SC4-RAW';
pvCA65CRAW = 'BL06J-EA-USER-01:SC5-RAW';
pvCA66CRAW = 'BL06J-EA-USER-01:SC6-RAW';
pvCA67CRAW = 'BL06J-EA-USER-01:SC7-RAW';
pvCA68CRAW = 'BL06J-EA-USER-01:SC8-RAW';

ca61sr = Scaler8512ChannelEpicsDeviceClass('ca61sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA61CRAW);
ca62sr = Scaler8512ChannelEpicsDeviceClass('ca62sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA62CRAW);
ca63sr = Scaler8512ChannelEpicsDeviceClass('ca63sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA63CRAW);
ca64sr = Scaler8512ChannelEpicsDeviceClass('ca64sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA64CRAW);
ca65sr = Scaler8512ChannelEpicsDeviceClass('ca65sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA65CRAW);
ca66sr = Scaler8512ChannelEpicsDeviceClass('ca66sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA66CRAW);
ca67sr = Scaler8512ChannelEpicsDeviceClass('ca67sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA67CRAW);
ca68sr = Scaler8512ChannelEpicsDeviceClass('ca68sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA68CRAW);


#For Patch Panel U1
#Use the scaler Raw count
pvCA51CRAW = 'BL06I-EA-USER-01:SC1-RAW';
pvCA52CRAW = 'BL06I-EA-USER-01:SC2-RAW';
pvCA53CRAW = 'BL06I-EA-USER-01:SC3-RAW';
pvCA54CRAW = 'BL06I-EA-USER-01:SC4-RAW';

ca51sr = Scaler8512ChannelEpicsDeviceClass('ca51sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA51CRAW);
ca52sr = Scaler8512ChannelEpicsDeviceClass('ca52sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA52CRAW);
ca53sr = Scaler8512ChannelEpicsDeviceClass('ca53sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA53CRAW);
ca54sr = Scaler8512ChannelEpicsDeviceClass('ca54sr',pvPatchPanelScalerTP, pvPatchPanelScalerCNT, pvCA54CRAW);


#acqtime = DetectorIntegrationsDevice('acqtime', [ca61sr]);
#acqtime.addDetectors([ca11sr]);
