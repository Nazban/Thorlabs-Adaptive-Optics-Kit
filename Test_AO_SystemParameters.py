# Author(s): Nazban Darukhanawalla

from AO_Kit import DMH40, ZernikeCoeff, WFS20
import numpy as np

WFS_dll_path = r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\WFS_64.dll'
WFS = WFS20(WFS_dll_path=WFS_dll_path)
DM_dll_path =  r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFM_64.dll'
DM_dll_pathx =  r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFMX_64.dll'
DM = DMH40(DM_dll_path, DM_dll_pathx)


#device.Relax()
WFS.SetPupil(pupilCenterXMm = 0.0, pupilCenterYMm = 0.0, pupilDiameterXMm = 4.6, pupilDiameterYMm = 4.6)

WFS.TakeImage(exposureTimeSet=20.0)
WFS.ShowSpotfield()
# DM.Calibrate(show=True, autoexposure=False)
DM.MeasureSystemParameters(show = True, autoexposure = False)
WFS.GetStatus()
# DM.GetSystemParameters()    

# WFS.TakeImageAutoExposure()
# WFS.ShowSpotfield()
# WFS.GetWavefrontfromSpotfield(show=True, cancelWavefrontTilt=0)
WFS.GetStatus()

zernikeAmp = DM.ConvertZernikeAmp()
print (zernikeAmp)
DM.GetFlatWavefront()

# WFS.TakeImageAutoExposure()
# WFS.GetWavefrontfromSpotfield(show=True, cancelWavefrontTilt=0)

WFS.GetStatus()

DM.Close()
WFS.Close()