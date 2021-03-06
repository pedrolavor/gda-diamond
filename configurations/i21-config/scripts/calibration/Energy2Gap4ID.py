'''
Created on 10 Jan 2018

@author: fy65
'''
from gdaserver import pgmGratingSelect
def idgap_calc(Ep, polarisation):
    gap=19.9
    # Linear Horizontal
    if (polarisation=="LH"):
        if (Ep>915 and Ep < 1020):
            if pgmGratingSelect.getPosition()=="VPG1":
                gap = 19.086332 + 0.02336597*Ep #Corrected for VPG1 on 2017/02/15: SHOULD BE CHECKED: MAY NEED CORRECTING
                #gap = 23.271 + 0.01748*Ep #Corrected for VPG1 on 2016/10/06
            elif pgmGratingSelect.getPosition()=="VPG2":
                #gap = 17.3845068 + 0.02555917*Ep #Corrected for VPG2 on 2017/02/15
                #gap = 12.338 + 0.03074*Ep  #Corrected for VPG2 on 2016/10/06
                gap = 18.669193 + 0.02350180*Ep  #Corrected for VPG2 at 930 eV on 2017/08/08
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap = 18.5611846 + 0.02369966*Ep #Corrected for VPG3 on 2017/09/20
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")
        elif (Ep>500 and Ep<600):
            if pgmGratingSelect.getPosition()=="VPG1":
                #gap = 19.086332 + 0.02336597*Ep #Corrected for VPG1 on 2017/02/15
                gap = 18.0359889 + 0.02485902*Ep #Corrected for VPG1 on 2018/04/19
            elif pgmGratingSelect.getPosition()=="VPG2":
                #gap = 17.3845068 + 0.02555917*Ep #Corrected for VPG2 on 2017/02/15
                #gap = 12.338 + 0.03074*Ep  #Corrected for VPG2 on 2016/10/06
                #gap = 18.669193 + 0.02350180*Ep  #Corrected for VPG2 at 930 eV on 2017/08/08
                gap = 18.0444241 + 0.02478207*Ep  #Corrected for VPG2 around 550 eV on 2018/01/16
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap = 18.0112254 + 0.02490918*Ep #Corrected for VPG3 on 2018/01/20
                
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")
        elif (Ep>600 and Ep<700):
            if pgmGratingSelect.getPosition()=="VPG1":
                #gap = 19.086332 + 0.02336597*Ep #Corrected for VPG1 on 2017/02/15
                gap = 18.9610065 + 0.02329706*Ep #Corrected for VPG1 on 2018/06/22
            elif pgmGratingSelect.getPosition()=="VPG2":
                #gap = 17.3845068 + 0.02555917*Ep #Corrected for VPG2 on 2017/02/15
                #gap = 12.338 + 0.03074*Ep  #Corrected for VPG2 on 2016/10/06
                #gap = 18.669193 + 0.02350180*Ep  #Corrected for VPG2 at 930 eV on 2017/08/08
                gap = 18.9256730 + 0.02327420*Ep  #Corrected for VPG2 around 550 eV on 2018/06/22
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap = 18.9464110 + 0.02331950*Ep #Corrected for VPG3 on 2018/06/22                
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")
        elif (Ep>690 and Ep<820):
            if pgmGratingSelect.getPosition()=="VPG1":
                #gap = 19.2998231 + 0.02285595*Ep #Corrected for VPG1 on 2017/12/01
                gap = 19.2309878 + 0.02296267*Ep #Corrected for VPG1 on 2018/4/23
            elif pgmGratingSelect.getPosition()=="VPG2":
                #gap = 18.7769565 + 0.02352715*Ep  #Corrected for VPG2 on 2018/03/07
                gap = 19.2185231 + 0.02287568*Ep  #Corrected for VPG2 on 2018/04/23
            elif pgmGratingSelect.getPosition()=="VPG3":
                #gap = 19.0918751 + 0.02313526*Ep #Corrected for VPG3 on 2018/03/07
                gap = 18.5124072 + 0.02393300*Ep #Corrected for VPG3 on 2018/04/23
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")    
        elif (Ep>=820 and Ep<=915):
            if pgmGratingSelect.getPosition()=="VPG1":
                #gap = 19.2998231 + 0.02285595*Ep #Corrected for VPG1 on 2017/02/15
                raise Exception("No calibration available for VPG1 in LH mode")
            elif pgmGratingSelect.getPosition()=="VPG2":
                gap = 18.9330761 + 0.02318578*Ep  #Corrected for VPG2 on 2018/01/10
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap = 18.8476189 + 0.02339853*Ep #Corrected for VPG3 on 2018/01/11
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")    
        elif (Ep>=310 and Ep<=410):
            if pgmGratingSelect.getPosition()=="VPG1":
                gap = 15.0738470 + 0.03168032*Ep #Corrected for VPG1 on 2018/04/16
            elif pgmGratingSelect.getPosition()=="VPG2":
                gap = 15.0331831 + 0.03165627*Ep  #Corrected for VPG2 on 2018/04/16
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap = 15.1190608 + 0.03150392*Ep #Corrected for VPG3 on 2018/04/16
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")
        elif (Ep>450 and Ep<500):
            if pgmGratingSelect.getPosition()=="VPG2":
                gap = 17.1120838 + 0.02661410*Ep #Corrected for VPG2 on 2018/08/03
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")
        elif (Ep>=1160 and Ep<=1220):
            if pgmGratingSelect.getPosition()=="VPG1":
                gap = 8.60527040 + 0.03287279*Ep  #Corrected for VPG1 on 2018/06/21
            elif pgmGratingSelect.getPosition()=="VPG2":
                gap = 9.05139093 + 0.03235159*Ep  #Corrected for VPG2 on 2018/06/19
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap = 8.90762510 + 0.03261594*Ep #Corrected for VPG3 on 2018/06/19
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")    
        elif (Ep>=1380 and Ep<=1430):
            if pgmGratingSelect.getPosition()=="VPG1":
                gap =-46.1543877 + 0.07416048*Ep  #Corrected for VPG1 on 2018/06/21
            elif pgmGratingSelect.getPosition()=="VPG2":
                gap =-43.2421160 + 0.07174397*Ep  #Corrected for VPG2 on 2018/06/19
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap =-48.2489975 + 0.07562796*Ep #Corrected for VPG3 on 2018/06/19
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")    
        else:
            raise ValueError("Energy demand %feV is outside calibrated ranges") % (Ep)
    # Linear Vertical
    elif polarisation=="LV":
        if (Ep>915 and Ep < 1020):
            if pgmGratingSelect.getPosition()=="VPG1":
                # gap = 11.1441137 + 0.01881376*Ep #Corrected for VPG1 on 2017/07/31 ---> Linear Vertical
                # gap = 11.6401974 + 0.01819208*Ep #Corrected for VPG1 on 2017/07/07 ---> Linear Vertical
                # gap = 11.0806699 + 0.01891585*Ep #Corrected for VPG1 at 930 eV on 2017/08/03 ---> Linear Vertical
                gap = 10.8954430 + 0.01901698*Ep #Corrected for VPG1 at 930 eV on 2018/04/21 ---> Linear Vertical
            elif pgmGratingSelect.getPosition()=="VPG2":
                # gap = 11.3014613 + 0.01856236*Ep #Corrected for VPG2 on 2017/08/02 ---> Linear Vertical
#                 gap = 11.2363888 + 0.01864200*Ep #Corrected for VPG2 at 930 eV on 2017/08/03 ---> Linear Vertical
                gap = 11.3838749 + 0.01844212*Ep #Corrected for VPG2 at 930 eV on 2017/10/08 ---> Linear Vertical
            elif pgmGratingSelect.getPosition()=="VPG3":
                # gap = 11.2972185 + 0.01862358*Ep #Corrected for VPG3 on 2017/07/27 ---> Linear Vertical
                gap = 11.3218637 + 0.01860144*Ep #Corrected for VPG3 at 930 eV on 2017/08/03 ---> Linear Vertical
            else:
                raise ValueError("Unknown Grating select in LV polarisationMode")
        elif (Ep>500 and Ep<600):
            if pgmGratingSelect.getPosition()=="VPG1":
                #gap = 19.086332 + 0.02336597*Ep #Corrected for VPG1 on 2017/02/15
                gap = 11.4929059 +  0.01866740*Ep #Corrected for VPG1 on 2018/04/19
            elif pgmGratingSelect.getPosition()=="VPG2":
                #gap = 17.3845068 + 0.02555917*Ep #Corrected for VPG2 on 2017/02/15
                #gap = 12.338 + 0.03074*Ep  #Corrected for VPG2 on 2016/10/06
                gap = 11.5139582 + 0.01858746*Ep  #Corrected for VPG2 around 550 eV on 2018/01/15
            elif pgmGratingSelect.getPosition()=="VPG3":
                #gap = 11.4731251 + 0.01873832*Ep #Corrected for VPG3 on 2017/10/09
                gap = 11.4922997 + 0.01867722*Ep #Corrected for VPG3 on 2018/01/20
            else:
                raise ValueError("Unknown Grating select in LV polarisationMode")
        elif (Ep>600 and Ep<700):
            if pgmGratingSelect.getPosition()=="VPG1":
                #gap = 19.086332 + 0.02336597*Ep #Corrected for VPG1 on 2017/02/15
                gap = 12.0417084 + 0.01768560*Ep #Corrected for VPG1 on 2018/06/22
            elif pgmGratingSelect.getPosition()=="VPG2":
                #gap = 17.3845068 + 0.02555917*Ep #Corrected for VPG2 on 2017/02/15
                #gap = 12.338 + 0.03074*Ep  #Corrected for VPG2 on 2016/10/06
                #gap = 18.669193 + 0.02350180*Ep  #Corrected for VPG2 at 930 eV on 2017/08/08
                gap = 12.0417084 + 0.01768560*Ep  #Corrected for VPG2 around 550 eV on 2018/06/22
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap = 12.0035701 + 0.01780733*Ep #Corrected for VPG3 on 2018/06/22
                
            else:
                raise ValueError("Unknown Grating select in LV polarisationMode")
        elif (Ep>690 and Ep<820):
            if pgmGratingSelect.getPosition()=="VPG1":
                #gap = 12.1996757 + 0.01755656*Ep #Corrected for VPG1 on 2017/12/01
                gap = 12.1751464 + 0.01759710*Ep #Corrected for VPG1 on 2018/04/23
            elif pgmGratingSelect.getPosition()=="VPG2":
                #gap = 12.2144937 + 0.01746779*Ep  #Corrected for VPG2 on 2017/11/30
                gap = 12.1515345 + 0.01754967*Ep  #Corrected for VPG2 on 2017/04/23
            elif pgmGratingSelect.getPosition()=="VPG3":
                #gap = 12.1109048 + 0.01766378*Ep #Corrected for VPG3 on 2018/03/07
                gap = 12.0099896 + 0.01781198*Ep #Corrected for VPG3 on 2018/04/23
                #raise Exception("No calibration available for VPG1 in LV mode")
            else:
                raise ValueError("Unknown Grating select in LV polarisationMode")
        elif (Ep>=820 and Ep<=915):
            if pgmGratingSelect.getPosition()=="VPG1":
                #gap = 12.1996757 + 0.01755656*Ep #Corrected for VPG1 on 2017/02/15
                raise Exception("No calibration available for VPG1 in LV mode")
            elif pgmGratingSelect.getPosition()=="VPG2":
                gap = 11.8230212 + 0.01793526*Ep  #Corrected for VPG2 on 2018/01/10
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap = 11.7160683 + 0.01814283*Ep #Corrected for VPG3 on 2018/01/11
            else:
                raise ValueError("Unknown Grating select in LV polarisationMode")
        elif (Ep>=1160 and Ep<=1220):
            if pgmGratingSelect.getPosition()=="VPG1":
                gap = 2.89323404 + 0.02633185*Ep  #Corrected for VPG1 on 2018/06/21
            elif pgmGratingSelect.getPosition()=="VPG2":
                gap = 2.51074540 + 0.02653346*Ep  #Corrected for VPG2 on 2018/06/19
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap = 2.82442703 + 0.02637886*Ep #Corrected for VPG3 on 2018/06/19
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")    
        elif (Ep>=460 and Ep<500):
            if pgmGratingSelect.getPosition()=="VPG2":
                gap = 11.0197952 + 0.01953697*Ep #Corrected for VPG2 on 2018/08/03
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")
        elif (Ep>=1380 and Ep<=1430):
            if pgmGratingSelect.getPosition()=="VPG1":
                gap =-40.0707586 + 0.05886600*Ep  #Corrected for VPG1 on 2018/06/21
            elif pgmGratingSelect.getPosition()=="VPG2":
                gap =-45.2788260 + 0.06229816*Ep  #Corrected for VPG2 on 2018/06/19
            elif pgmGratingSelect.getPosition()=="VPG3":
                gap =-43.8399100 + 0.06151759*Ep #Corrected for VPG3 on 2018/06/19
            else:
                raise ValueError("Unknown Grating select in LH polarisationMode")    
        else:
            raise ValueError("Energy demand %feV is outside calibrated ranges") % (Ep)
    # Circular left
    elif polarisation=="CL":
        raise ValueError("CL polarisationMode is not yet implemented")
    
    # Circular right
    elif polarisation=="CR":
        raise ValueError("CR polarisationMode is not yet implemented")
    
    # Linear 
    elif polarisation=="L1":
        raise ValueError("L1 polarisationMode is not yet implemented")
 
    # Unsupported        
    else:
        raise ValueError("Unsupported polarisationMode mode")
       
    if (gap<20 or gap>70):
        raise ValueError("Required Soft X-Ray ID idgap is out side allowable bound (20, 70)!")
    return gap
