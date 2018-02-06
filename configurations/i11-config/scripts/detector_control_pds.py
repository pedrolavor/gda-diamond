from detector_control_class import DetectorControlClass
pds=[]
# MAc stage1 
llim11=DetectorControlClass('llim11', 'BL11I-EA-MAC-01:E1:LLIM', 'BL11I-EA-MAC-01:E1:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim11)
ulim11=DetectorControlClass('ulim11', 'BL11I-EA-MAC-01:E1:ULIM', 'BL11I-EA-MAC-01:E1:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim11)
pmt11=DetectorControlClass('pmt11', 'BL11I-EA-MAC-01:E1:CTRL', 'BL11I-EA-MAC-01:E1:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt11)
llim12=DetectorControlClass('llim12', 'BL11I-EA-MAC-01:E2:LLIM', 'BL11I-EA-MAC-01:E2:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim12)
ulim12=DetectorControlClass('ulim12', 'BL11I-EA-MAC-01:E2:ULIM', 'BL11I-EA-MAC-01:E2:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim12)
pmt12=DetectorControlClass('pmt12', 'BL11I-EA-MAC-01:E2:CTRL', 'BL11I-EA-MAC-01:E2:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt12)
llim13=DetectorControlClass('llim13', 'BL11I-EA-MAC-01:E3:LLIM', 'BL11I-EA-MAC-01:E3:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim13)
ulim13=DetectorControlClass('ulim13', 'BL11I-EA-MAC-01:E3:ULIM', 'BL11I-EA-MAC-01:E3:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim13)
pmt13=DetectorControlClass('pmt13', 'BL11I-EA-MAC-01:E3:CTRL', 'BL11I-EA-MAC-01:E3:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt13)
llim14=DetectorControlClass('llim14', 'BL11I-EA-MAC-01:E4:LLIM', 'BL11I-EA-MAC-01:E4:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim14)
ulim14=DetectorControlClass('ulim14', 'BL11I-EA-MAC-01:E4:ULIM', 'BL11I-EA-MAC-01:E4:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim14)
pmt14=DetectorControlClass('pmt14', 'BL11I-EA-MAC-01:E4:CTRL', 'BL11I-EA-MAC-01:E4:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt14)
llim15=DetectorControlClass('llim15', 'BL11I-EA-MAC-01:E5:LLIM', 'BL11I-EA-MAC-01:E5:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim15)
ulim15=DetectorControlClass('ulim15', 'BL11I-EA-MAC-01:E5:ULIM', 'BL11I-EA-MAC-01:E5:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim15) 
pmt15=DetectorControlClass('pmt15', 'BL11I-EA-MAC-01:E5:CTRL', 'BL11I-EA-MAC-01:E5:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt15)
llim16=DetectorControlClass('llim16', 'BL11I-EA-MAC-01:E6:LLIM', 'BL11I-EA-MAC-01:E6:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim16)
ulim16=DetectorControlClass('ulim16', 'BL11I-EA-MAC-01:E6:ULIM', 'BL11I-EA-MAC-01:E6:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim16)
pmt16=DetectorControlClass('pmt16', 'BL11I-EA-MAC-01:E6:CTRL', 'BL11I-EA-MAC-01:E6:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt16)
llim17=DetectorControlClass('llim17', 'BL11I-EA-MAC-01:E7:LLIM', 'BL11I-EA-MAC-01:E7:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim17)
ulim17=DetectorControlClass('ulim17', 'BL11I-EA-MAC-01:E7:ULIM', 'BL11I-EA-MAC-01:E7:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim17)
pmt17=DetectorControlClass('pmt17', 'BL11I-EA-MAC-01:E7:CTRL', 'BL11I-EA-MAC-01:E7:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt17)
llim18=DetectorControlClass('llim18', 'BL11I-EA-MAC-01:E8:LLIM', 'BL11I-EA-MAC-01:E8:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim18)
ulim18=DetectorControlClass('ulim18', 'BL11I-EA-MAC-01:E8:ULIM', 'BL11I-EA-MAC-01:E8:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim18)
pmt18=DetectorControlClass('pmt18', 'BL11I-EA-MAC-01:E8:CTRL', 'BL11I-EA-MAC-01:E8:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt18)
llim19=DetectorControlClass('llim19', 'BL11I-EA-MAC-01:E9:LLIM', 'BL11I-EA-MAC-01:E9:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim19)
ulim19=DetectorControlClass('ulim19', 'BL11I-EA-MAC-01:E9:ULIM', 'BL11I-EA-MAC-01:E9:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim19)
pmt19=DetectorControlClass('pmt19', 'BL11I-EA-MAC-01:E9:CTRL', 'BL11I-EA-MAC-01:E9:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt19)
# MAC stage 2
llim21=DetectorControlClass('llim21', 'BL11I-EA-MAC-02:E1:LLIM', 'BL11I-EA-MAC-02:E1:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim21)
ulim21=DetectorControlClass('ulim21', 'BL11I-EA-MAC-02:E1:ULIM', 'BL11I-EA-MAC-02:E1:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim21)
pmt21=DetectorControlClass('pmt21', 'BL11I-EA-MAC-02:E1:CTRL', 'BL11I-EA-MAC-02:E1:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt21)
llim22=DetectorControlClass('llim22', 'BL11I-EA-MAC-02:E2:LLIM', 'BL11I-EA-MAC-02:E2:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim22)
ulim22=DetectorControlClass('ulim22', 'BL11I-EA-MAC-02:E2:ULIM', 'BL11I-EA-MAC-02:E2:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim22)
pmt22=DetectorControlClass('pmt22', 'BL11I-EA-MAC-02:E2:CTRL', 'BL11I-EA-MAC-02:E2:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt22)
llim23=DetectorControlClass('llim23', 'BL11I-EA-MAC-02:E3:LLIM', 'BL11I-EA-MAC-02:E3:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim23)
ulim23=DetectorControlClass('ulim23', 'BL11I-EA-MAC-02:E3:ULIM', 'BL11I-EA-MAC-02:E3:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim23)
pmt23=DetectorControlClass('pmt23', 'BL11I-EA-MAC-02:E3:CTRL', 'BL11I-EA-MAC-02:E3:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt23)
llim24=DetectorControlClass('llim24', 'BL11I-EA-MAC-02:E4:LLIM', 'BL11I-EA-MAC-02:E4:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim24)
ulim24=DetectorControlClass('ulim24', 'BL11I-EA-MAC-02:E4:ULIM', 'BL11I-EA-MAC-02:E4:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim24)
pmt24=DetectorControlClass('pmt24', 'BL11I-EA-MAC-02:E4:CTRL', 'BL11I-EA-MAC-02:E4:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt24)
llim25=DetectorControlClass('llim25', 'BL11I-EA-MAC-02:E5:LLIM', 'BL11I-EA-MAC-02:E5:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim25)
ulim25=DetectorControlClass('ulim25', 'BL11I-EA-MAC-02:E5:ULIM', 'BL11I-EA-MAC-02:E5:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim25)
pmt25=DetectorControlClass('pmt25', 'BL11I-EA-MAC-02:E5:CTRL', 'BL11I-EA-MAC-02:E5:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt25)
llim26=DetectorControlClass('llim26', 'BL11I-EA-MAC-02:E6:LLIM', 'BL11I-EA-MAC-02:E6:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim26)
ulim26=DetectorControlClass('ulim26', 'BL11I-EA-MAC-02:E6:ULIM', 'BL11I-EA-MAC-02:E6:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim26)
pmt26=DetectorControlClass('pmt26', 'BL11I-EA-MAC-02:E6:CTRL', 'BL11I-EA-MAC-02:E6:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt26)
llim27=DetectorControlClass('llim27', 'BL11I-EA-MAC-02:E7:LLIM', 'BL11I-EA-MAC-02:E7:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim27)
ulim27=DetectorControlClass('ulim27', 'BL11I-EA-MAC-02:E7:ULIM', 'BL11I-EA-MAC-02:E7:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim27)
pmt27=DetectorControlClass('pmt27', 'BL11I-EA-MAC-02:E7:CTRL', 'BL11I-EA-MAC-02:E7:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt27)
llim28=DetectorControlClass('llim28', 'BL11I-EA-MAC-02:E8:LLIM', 'BL11I-EA-MAC-02:E8:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim28)
ulim28=DetectorControlClass('ulim28', 'BL11I-EA-MAC-02:E8:ULIM', 'BL11I-EA-MAC-02:E8:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim28)
pmt28=DetectorControlClass('pmt28', 'BL11I-EA-MAC-02:E8:CTRL', 'BL11I-EA-MAC-02:E8:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt28)
llim29=DetectorControlClass('llim29', 'BL11I-EA-MAC-02:E9:LLIM', 'BL11I-EA-MAC-02:E9:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim29)
ulim29=DetectorControlClass('ulim29', 'BL11I-EA-MAC-02:E9:ULIM', 'BL11I-EA-MAC-02:E9:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim29)
pmt29=DetectorControlClass('pmt29', 'BL11I-EA-MAC-02:E9:CTRL', 'BL11I-EA-MAC-02:E9:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt29)
# MAC stage 3
llim31=DetectorControlClass('llim31', 'BL11I-EA-MAC-03:E1:LLIM', 'BL11I-EA-MAC-03:E1:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim31)
ulim31=DetectorControlClass('ulim31', 'BL11I-EA-MAC-03:E1:ULIM', 'BL11I-EA-MAC-03:E1:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim31)
pmt31=DetectorControlClass('pmt31', 'BL11I-EA-MAC-03:E1:CTRL', 'BL11I-EA-MAC-03:E1:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt31)
llim32=DetectorControlClass('llim32', 'BL11I-EA-MAC-03:E2:LLIM', 'BL11I-EA-MAC-03:E2:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim32)
ulim32=DetectorControlClass('ulim32', 'BL11I-EA-MAC-03:E2:ULIM', 'BL11I-EA-MAC-03:E2:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim32)
pmt32=DetectorControlClass('pmt32', 'BL11I-EA-MAC-03:E2:CTRL', 'BL11I-EA-MAC-03:E2:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt32)
llim33=DetectorControlClass('llim33', 'BL11I-EA-MAC-03:E3:LLIM', 'BL11I-EA-MAC-03:E3:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim33)
ulim33=DetectorControlClass('ulim33', 'BL11I-EA-MAC-03:E3:ULIM', 'BL11I-EA-MAC-03:E3:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim33)
pmt33=DetectorControlClass('pmt33', 'BL11I-EA-MAC-03:E3:CTRL', 'BL11I-EA-MAC-03:E3:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt33)
llim34=DetectorControlClass('llim34', 'BL11I-EA-MAC-03:E4:LLIM', 'BL11I-EA-MAC-03:E4:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim34)
ulim34=DetectorControlClass('ulim34', 'BL11I-EA-MAC-03:E4:ULIM', 'BL11I-EA-MAC-03:E4:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim34)
pmt34=DetectorControlClass('pmt34', 'BL11I-EA-MAC-03:E4:CTRL', 'BL11I-EA-MAC-03:E4:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt34)
llim35=DetectorControlClass('llim35', 'BL11I-EA-MAC-03:E5:LLIM', 'BL11I-EA-MAC-03:E5:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim35)
ulim35=DetectorControlClass('ulim35', 'BL11I-EA-MAC-03:E5:ULIM', 'BL11I-EA-MAC-03:E5:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim35)
pmt35=DetectorControlClass('pmt35', 'BL11I-EA-MAC-03:E5:CTRL', 'BL11I-EA-MAC-03:E5:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt35)
llim36=DetectorControlClass('llim36', 'BL11I-EA-MAC-03:E6:LLIM', 'BL11I-EA-MAC-03:E6:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim36)
ulim36=DetectorControlClass('ulim36', 'BL11I-EA-MAC-03:E6:ULIM', 'BL11I-EA-MAC-03:E6:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim36)
pmt36=DetectorControlClass('pmt36', 'BL11I-EA-MAC-03:E6:CTRL', 'BL11I-EA-MAC-03:E6:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt36)
llim37=DetectorControlClass('llim37', 'BL11I-EA-MAC-03:E7:LLIM', 'BL11I-EA-MAC-03:E7:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim37)
ulim37=DetectorControlClass('ulim37', 'BL11I-EA-MAC-03:E7:ULIM', 'BL11I-EA-MAC-03:E7:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim37)
pmt37=DetectorControlClass('pmt37', 'BL11I-EA-MAC-03:E7:CTRL', 'BL11I-EA-MAC-03:E7:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt37)
llim38=DetectorControlClass('llim38', 'BL11I-EA-MAC-03:E8:LLIM', 'BL11I-EA-MAC-03:E8:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim38)
ulim38=DetectorControlClass('ulim38', 'BL11I-EA-MAC-03:E8:ULIM', 'BL11I-EA-MAC-03:E8:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim38)
pmt38=DetectorControlClass('pmt38', 'BL11I-EA-MAC-03:E8:CTRL', 'BL11I-EA-MAC-03:E8:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt38)
llim39=DetectorControlClass('llim39', 'BL11I-EA-MAC-03:E9:LLIM', 'BL11I-EA-MAC-03:E9:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim39)
ulim39=DetectorControlClass('ulim39', 'BL11I-EA-MAC-03:E9:ULIM', 'BL11I-EA-MAC-03:E9:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim39)
pmt39=DetectorControlClass('pmt39', 'BL11I-EA-MAC-03:E9:CTRL', 'BL11I-EA-MAC-03:E9:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt39)
# MAC stage4
llim41=DetectorControlClass('llim41', 'BL11I-EA-MAC-04:E1:LLIM', 'BL11I-EA-MAC-04:E1:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim41)
ulim41=DetectorControlClass('ulim41', 'BL11I-EA-MAC-04:E1:ULIM', 'BL11I-EA-MAC-04:E1:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim41)
pmt41=DetectorControlClass('pmt41', 'BL11I-EA-MAC-04:E1:CTRL', 'BL11I-EA-MAC-04:E1:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt41)
llim42=DetectorControlClass('llim42', 'BL11I-EA-MAC-04:E2:LLIM', 'BL11I-EA-MAC-04:E2:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim42)
ulim42=DetectorControlClass('ulim42', 'BL11I-EA-MAC-04:E2:ULIM', 'BL11I-EA-MAC-04:E2:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim42)
pmt42=DetectorControlClass('pmt42', 'BL11I-EA-MAC-04:E2:CTRL', 'BL11I-EA-MAC-04:E2:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt42)
llim43=DetectorControlClass('llim43', 'BL11I-EA-MAC-04:E3:LLIM', 'BL11I-EA-MAC-04:E3:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim43)
ulim43=DetectorControlClass('ulim43', 'BL11I-EA-MAC-04:E3:ULIM', 'BL11I-EA-MAC-04:E3:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim43)
pmt43=DetectorControlClass('pmt43', 'BL11I-EA-MAC-04:E3:CTRL', 'BL11I-EA-MAC-04:E3:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt43)
llim44=DetectorControlClass('llim44', 'BL11I-EA-MAC-04:E4:LLIM', 'BL11I-EA-MAC-04:E4:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim44)
ulim44=DetectorControlClass('ulim44', 'BL11I-EA-MAC-04:E4:ULIM', 'BL11I-EA-MAC-04:E4:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim44)
pmt44=DetectorControlClass('pmt44', 'BL11I-EA-MAC-04:E4:CTRL', 'BL11I-EA-MAC-04:E4:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt44)
llim45=DetectorControlClass('llim45', 'BL11I-EA-MAC-04:E5:LLIM', 'BL11I-EA-MAC-04:E5:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim45)
ulim45=DetectorControlClass('ulim45', 'BL11I-EA-MAC-04:E5:ULIM', 'BL11I-EA-MAC-04:E5:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim45)
pmt45=DetectorControlClass('pmt45', 'BL11I-EA-MAC-04:E5:CTRL', 'BL11I-EA-MAC-04:E5:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt45)
llim46=DetectorControlClass('llim46', 'BL11I-EA-MAC-04:E6:LLIM', 'BL11I-EA-MAC-04:E6:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim46)
ulim46=DetectorControlClass('ulim46', 'BL11I-EA-MAC-04:E6:ULIM', 'BL11I-EA-MAC-04:E6:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim46)
pmt46=DetectorControlClass('pmt46', 'BL11I-EA-MAC-04:E6:CTRL', 'BL11I-EA-MAC-04:E6:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt46)
llim47=DetectorControlClass('llim47', 'BL11I-EA-MAC-04:E7:LLIM', 'BL11I-EA-MAC-04:E7:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim47)
ulim47=DetectorControlClass('ulim47', 'BL11I-EA-MAC-04:E7:ULIM', 'BL11I-EA-MAC-04:E7:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim47)
pmt47=DetectorControlClass('pmt47', 'BL11I-EA-MAC-04:E7:CTRL', 'BL11I-EA-MAC-04:E7:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt47)
llim48=DetectorControlClass('llim48', 'BL11I-EA-MAC-04:E8:LLIM', 'BL11I-EA-MAC-04:E8:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim48)
ulim48=DetectorControlClass('ulim48', 'BL11I-EA-MAC-04:E8:ULIM', 'BL11I-EA-MAC-04:E8:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim48)
pmt48=DetectorControlClass('pmt48', 'BL11I-EA-MAC-04:E8:CTRL', 'BL11I-EA-MAC-04:E8:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt48)
llim49=DetectorControlClass('llim49', 'BL11I-EA-MAC-04:E9:LLIM', 'BL11I-EA-MAC-04:E9:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim49)
ulim49=DetectorControlClass('ulim49', 'BL11I-EA-MAC-04:E9:ULIM', 'BL11I-EA-MAC-04:E9:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim49)
pmt49=DetectorControlClass('pmt49', 'BL11I-EA-MAC-04:E9:CTRL', 'BL11I-EA-MAC-04:E9:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt49)
# MAC stage5
llim51=DetectorControlClass('llim51', 'BL11I-EA-MAC-05:E1:LLIM', 'BL11I-EA-MAC-05:E1:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim51)
ulim51=DetectorControlClass('ulim51', 'BL11I-EA-MAC-05:E1:ULIM', 'BL11I-EA-MAC-05:E1:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim51)
pmt51=DetectorControlClass('pmt51', 'BL11I-EA-MAC-05:E1:CTRL', 'BL11I-EA-MAC-05:E1:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt51)
llim52=DetectorControlClass('llim52', 'BL11I-EA-MAC-05:E2:LLIM', 'BL11I-EA-MAC-05:E2:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim52)
ulim52=DetectorControlClass('ulim52', 'BL11I-EA-MAC-05:E2:ULIM', 'BL11I-EA-MAC-05:E2:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim52)
pmt52=DetectorControlClass('pmt52', 'BL11I-EA-MAC-05:E2:CTRL', 'BL11I-EA-MAC-05:E2:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt52)
llim53=DetectorControlClass('llim53', 'BL11I-EA-MAC-05:E3:LLIM', 'BL11I-EA-MAC-05:E3:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim53)
ulim53=DetectorControlClass('ulim53', 'BL11I-EA-MAC-05:E3:ULIM', 'BL11I-EA-MAC-05:E3:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim53)
pmt53=DetectorControlClass('pmt53', 'BL11I-EA-MAC-05:E3:CTRL', 'BL11I-EA-MAC-05:E3:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt53)
llim54=DetectorControlClass('llim54', 'BL11I-EA-MAC-05:E4:LLIM', 'BL11I-EA-MAC-05:E4:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim54)
ulim54=DetectorControlClass('ulim54', 'BL11I-EA-MAC-05:E4:ULIM', 'BL11I-EA-MAC-05:E4:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim54)
pmt54=DetectorControlClass('pmt54', 'BL11I-EA-MAC-05:E4:CTRL', 'BL11I-EA-MAC-05:E4:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt54)
llim55=DetectorControlClass('llim55', 'BL11I-EA-MAC-05:E5:LLIM', 'BL11I-EA-MAC-05:E5:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim55)
ulim55=DetectorControlClass('ulim55', 'BL11I-EA-MAC-05:E5:ULIM', 'BL11I-EA-MAC-05:E5:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim55)
pmt55=DetectorControlClass('pmt55', 'BL11I-EA-MAC-05:E5:CTRL', 'BL11I-EA-MAC-05:E5:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt55)
llim56=DetectorControlClass('llim56', 'BL11I-EA-MAC-05:E6:LLIM', 'BL11I-EA-MAC-05:E6:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim56)
ulim56=DetectorControlClass('ulim56', 'BL11I-EA-MAC-05:E6:ULIM', 'BL11I-EA-MAC-05:E6:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim56)
pmt56=DetectorControlClass('pmt56', 'BL11I-EA-MAC-05:E6:CTRL', 'BL11I-EA-MAC-05:E6:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt56)
llim57=DetectorControlClass('llim57', 'BL11I-EA-MAC-05:E7:LLIM', 'BL11I-EA-MAC-05:E7:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim57)
ulim57=DetectorControlClass('ulim57', 'BL11I-EA-MAC-05:E7:ULIM', 'BL11I-EA-MAC-05:E7:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim57)
pmt57=DetectorControlClass('pmt57', 'BL11I-EA-MAC-05:E7:CTRL', 'BL11I-EA-MAC-05:E7:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt57)
llim58=DetectorControlClass('llim58', 'BL11I-EA-MAC-05:E8:LLIM', 'BL11I-EA-MAC-05:E8:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim58)
ulim58=DetectorControlClass('ulim58', 'BL11I-EA-MAC-05:E8:ULIM', 'BL11I-EA-MAC-05:E8:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim58)
pmt58=DetectorControlClass('pmt58', 'BL11I-EA-MAC-05:E8:CTRL', 'BL11I-EA-MAC-05:E8:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt58)
llim59=DetectorControlClass('llim59', 'BL11I-EA-MAC-05:E9:LLIM', 'BL11I-EA-MAC-05:E9:LLIM:RBV', 'mv', '%4.0f'); pds.append(llim59)
ulim59=DetectorControlClass('ulim59', 'BL11I-EA-MAC-05:E9:ULIM', 'BL11I-EA-MAC-05:E9:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulim59)
pmt59=DetectorControlClass('pmt59', 'BL11I-EA-MAC-05:E9:CTRL', 'BL11I-EA-MAC-05:E9:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmt59)
# Io 
llimIo=DetectorControlClass('llimIo', 'BL11I-DI-IMON-01:E1:LLIM', 'BL11I-DI-IMON-01:E1:LLIM:RBV', 'mv', '%4.0f'); pds.append(llimIo)
ulimIo=DetectorControlClass('ulimIo', 'BL11I-DI-IMON-01:E1:ULIM', 'BL11I-DI-IMON-01:E1:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulimIo)
pmtIo=DetectorControlClass('pmtIo', 'BL11I-DI-IMON-01:E1:CTRL', 'BL11I-DI-IMON-01:E1:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmtIo)
# Ie 
llimIe=DetectorControlClass('llimIe', 'BL11I-DI-IMON-02:E1:LLIM', 'BL11I-DI-IMON-02:E1:LLIM:RBV', 'mv', '%4.0f'); pds.append(llimIe)
ulimIe=DetectorControlClass('ulimIe', 'BL11I-DI-IMON-02:E1:ULIM', 'BL11I-DI-IMON-02:E1:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulimIe)
pmtIe=DetectorControlClass('pmtIe', 'BL11I-DI-IMON-02:E1:CTRL', 'BL11I-DI-IMON-02:E1:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmtIe)
# etl1 
llimetl1=DetectorControlClass('llimetl1', 'BL11I-EA-ENV-01:E1:LLIM', 'BL11I-EA-ENV-01:E1:LLIM:RBV', 'mv', '%4.0f'); pds.append(llimetl1)
ulimetl1=DetectorControlClass('ulimetl1', 'BL11I-EA-ENV-01:E1:ULIM', 'BL11I-EA-ENV-01:E1:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulimetl1)
pmtetl1=DetectorControlClass('pmtetl1', 'BL11I-EA-ENV-01:E1:CTRL', 'BL11I-EA-ENV-01:E1:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmtetl1)
# etl2 
llimetl2=DetectorControlClass('llimetl2', 'BL11I-DI-IMON-02:E1:LLIM', 'BL11I-DI-IMON-02:E1:LLIM:RBV', 'mv', '%4.0f'); pds.append(llimetl2)
ulimetl2=DetectorControlClass('ulimetl2', 'BL11I-DI-IMON-02:E1:ULIM', 'BL11I-DI-IMON-02:E1:ULIM:RBV', 'mv', '%4.0f'); pds.append(ulimetl2)
pmtetl2=DetectorControlClass('pmtetl2', 'BL11I-DI-IMON-02:E1:CTRL', 'BL11I-DI-IMON-02:E1:CTRL:RBV', 'mv', '%4.0f'); pds.append(pmtetl2)

print "finished ETL Detector object creation"
    