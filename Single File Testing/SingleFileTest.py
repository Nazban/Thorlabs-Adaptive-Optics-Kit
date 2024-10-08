# Author(s): Nazban Darukhanawalla

# CODE STRUCTURE:
# class DMH40dll() - Wrapper functions for the DMH40 Deformable Mirror
# class WFS20_5C() - Wrapper functions for the WFS20-5C Shack Hartmann
# class AO_Control() - Function that initializes both devices and combines functions for AO use

# Issues to Note:
# Line 285 - MeasureSystemParameter(): Throws an error (TLDFMX_ERROR_ITER_AMPL error -1074001404) via TLDFMX_measure_system_parameters() at the final step
# Line 77 - TLDFMX_error_message(): Throws an error (-1074003965) when inputting an int32 errorcode

import numpy as np
import matplotlib.pyplot as plt
import time
from ctypes import (windll, c_char_p, c_bool, c_int, c_int32, c_uint32, c_ulong, c_double, c_float, c_char, POINTER, byref, create_string_buffer)

MAX_ZERNIKE_MODES = 66
MAX_ZERNIKE_ORDERS = 10
MAX_SPOTS_Y = 80
MAX_SPOTS_X = 80
LENGTH_CHAR_ARRAY = 512

class DMH40dll():
    
    def __init__(self, dll_path, dll_pathx):
        self._instrumentHandleDM = c_ulong()
        self._dll = windll.LoadLibrary(dll_path)
        self._dllx = windll.LoadLibrary(dll_pathx)

        self.IDQuery = True
        self.resetDevice = False
        self.resource = c_char_p(b"")
        self.deviceCount = c_int()
        
    def TLDFM_init(self):
        self._dll.TLDFM_init(self.resourceName.value, 
                                            self.IDQuery, 
                                            self.resetDevice, 
                                            byref(self._instrumentHandleDM))
    def TLDFMX_init(self):
        self._dllx.TLDFMX_init(self.resourceName.value, 
                                            True, 
                                            True, 
                                            byref(self._instrumentHandleDM))
    def TLDFM_close(self):
        self._dll.TLDFM_close(self._instrumentHandleDM)

    def TLDFM_get_segment_count(self):
        self.segmentCount = c_uint32()
        self._dll.TLDFM_get_segment_count(self._instrumentHandleDM,
                                            byref(self.segmentCount))
        
        self.relaxPatternMirror = (c_double * (self.segmentCount.value))()  
        
    def TLDFM_get_tilt_count(self):
        self.tiltCount = c_uint32()
        self._dll.TLDFM_get_tilt_count(self._instrumentHandleDM,
                                        byref(self.tiltCount))
        self.relaxPatternArms = (c_double * (self.tiltCount.value))()

    def TLDFM_get_device_information(self, deviceIndex):
        self.manufacturer = c_char_p(b"")
        self.instrumentName = c_char_p(b"")
        self.serialNumber = c_char_p(b"")
        self.DeviceAvailable = c_bool()
        self.resourceName= c_char_p(b"")
        self._dll.TLDFM_get_device_information(self._instrumentHandleDM,
                                                deviceIndex, 
                                                self.manufacturer, 
                                                self.instrumentName, 
                                                self.serialNumber, 
                                                byref(self.DeviceAvailable), 
                                                self.resourceName)
        
    def TLDFMX_error_message(self, ErrorCode):
        '''
        Thorlabs built in error message function, doesn't seem to recognize int32 inputs
        '''
        ErrorCode = c_int32(ErrorCode)
        errorMessage = c_char()
        error = self._dllx.TLDFMX_error_message(self._instrumentHandleDM, 
                                             ErrorCode,
                                             errorMessage)
        if not error:
            return str(errorMessage)
           
    def TLDFM_set_segment_voltages(self, VoltageArray):
           self._dll.TLDFM_set_segment_voltages(self._instrumentHandleDM, 
                                                   VoltageArray)
    def TLDFMX_relax(self, isFirstStep):
        isFirstStep = c_bool(isFirstStep)
        devicePart = c_uint32(0)
        reload = c_bool(False)
        if isFirstStep.value == True:
            self.remainingSteps = c_int32()

        VoltageArray = self.relaxPatternMirror
        self._dllx.TLDFMX_relax(self._instrumentHandleDM,
                                                    devicePart,
                                                    isFirstStep,
                                                    reload,
                                                    VoltageArray,
                                                    self.relaxPatternArms,
                                                    byref(self.remainingSteps))
        return VoltageArray
      
    def TLDFMX_measure_system_parameters(self, isFirstStep, measuredZernikeAmplitudes):
        isFirstStep = c_bool(isFirstStep)
        measuredZernikeAmplitudes = (c_double * (len(measuredZernikeAmplitudes)))(*measuredZernikeAmplitudes)
        nextMirrorPattern = (c_double*(self.segmentCount.value))()
        if isFirstStep.value == True:
            self.remainingSteps = c_int32()

        error = (self._dllx.TLDFMX_measure_system_parameters(self._instrumentHandleDM,
                                                                           isFirstStep,
                                                                           measuredZernikeAmplitudes,
                                                                           nextMirrorPattern,
                                                                           byref(self.remainingSteps)
                                                                           ))
        print ("TLDFMX_measure_system_parameters Error Code = ", error)
        return nextMirrorPattern
        
class WFS20_5C():
    
    def __init__(self, dll_path):
    
        self._instrumentHandleWFS = c_ulong()
        self._dll = windll.LoadLibrary(dll_path)

        self.instrumentListIndex = c_int32(0)
        self.deviceID = c_int32()
        self.inUse = c_int32()

        self.instrumentName = create_string_buffer(b"", 20)
        self.instrumentSN = create_string_buffer(b"", 20)
        self.resourceName = create_string_buffer(b"", 30)
        self.IDQuery = False
        self.resetDevice = False
        
    def WFS_init(self):
        self._dll.WFS_init(self.resourceName,
                            self.IDQuery,
                            self.resetDevice,
                            byref(self._instrumentHandleWFS))  
        
    def WFS_GetInstrumentListInfo(self):
        self._dll.WFS_GetInstrumentListInfo(self._instrumentHandleWFS,
                                                    self.instrumentListIndex,
                                                    byref(self.deviceID),
                                                    byref(self.inUse),
                                                    self.instrumentName,
                                                    self.instrumentSN,
                                                    self.resourceName
                                                    )
    
    def WFS_init(self):
        self._dll.WFS_init(self.resourceName,
                            self.IDQuery,
                            self.resetDevice,
                            byref(self._instrumentHandleWFS)
                            )
    
    def WFS_close(self):
        self._dll.WFS_close(self._instrumentHandleWFS)
    
    def WFS_ConfigureCam(self, pixelFormat, camResolIndex):
        pixelFormat = c_int32(pixelFormat)
        camResolIndex = c_int32(camResolIndex)
        spotsX = c_int32()
        spotsY = c_int32()
        
        self._dll.WFS_ConfigureCam(self._instrumentHandleWFS,
                                                         pixelFormat,
                                                         camResolIndex,
                                                         byref(spotsX),
                                                         byref(spotsY))
        
        return spotsX, spotsY
        
    def WFS_SetPupil(self, pupilCenterXMm, pupilCenterYMm, pupilDiameterXMm, pupilDiameterYMm):
        pupilCenterXMm = c_double(pupilCenterXMm)
        pupilCenterYMm = c_double(pupilCenterYMm)
        pupilDiameterXMm = c_double(pupilDiameterXMm)
        pupilDiameterYMm = c_double(pupilDiameterYMm)
        
        self._dll.WFS_SetPupil(self._instrumentHandleWFS,
                                                     pupilCenterXMm,
                                                     pupilCenterYMm,
                                                     pupilDiameterXMm,
                                                     pupilDiameterYMm)
        
    def WFS_SetExposureTime(self, exposureTimeSet):
        '''
        Input: Exposure time (ms)
        Output: Exposure time set by WFS (ms)
        '''
        exposureTimeSet = c_double(exposureTimeSet)
        exposureTimeAct = c_double()
        #print ('ExposureTimeSet in dll file = {}'.format(exposureTimeSet))
        error = (self._dll.WFS_SetExposureTime(self._instrumentHandleWFS,
                                                            exposureTimeSet,
                                                            byref(exposureTimeAct)))
        if not error:
            return error, exposureTimeAct
    
    def WFS_TakeSpotfieldImage(self):
        return (self._dll.WFS_TakeSpotfieldImage(self._instrumentHandleWFS))

    def WFS_CalcSpotsCentrDiaIntens(self, dynamicNoiseCut, calculateDiameters = 0):
        dynamicNoiseCut = c_int32(dynamicNoiseCut)
        calculateDiameters = c_int32(calculateDiameters)
        
        return (self._dll.WFS_CalcSpotsCentrDiaIntens(self._instrumentHandleWFS,
                                                        dynamicNoiseCut,
                                                        calculateDiameters))

    def WFS_CalcSpotToReferenceDeviations(self, cancelWavefrontTilt):
        cancelWavefrontTilt = c_int32(cancelWavefrontTilt)
        return (self._dll.WFS_CalcSpotToReferenceDeviations(self._instrumentHandleWFS,
                                                            cancelWavefrontTilt))  
   
    def WFS_ZernikeLsf(self, zernikeOrders):
        self.zernikeOrders = c_int32(zernikeOrders)
        arrayZernikeUm = (c_float * (MAX_ZERNIKE_MODES + 1)) ()
        arrayZernikeOrdersUm = (c_float * (MAX_ZERNIKE_ORDERS + 1)) ()
        roCMm = c_double()
        
        (self._dll.WFS_ZernikeLsf(self._instrumentHandleWFS,
                                byref(self.zernikeOrders),
                                arrayZernikeUm,
                                arrayZernikeOrdersUm,
                                byref(roCMm)))
        return arrayZernikeUm, arrayZernikeOrdersUm, roCMm
    
    def WFS_CalcWavefront(self, wavefrontType, limitToPupil):
       
        wavefrontType = c_int32(wavefrontType)
        limitToPupil = c_int32(limitToPupil)
        arrayWavefront = np.empty(dtype=c_float, shape=(MAX_SPOTS_Y, MAX_SPOTS_X)) 
        
        error = self._dll.WFS_CalcWavefront(self._instrumentHandleWFS,
                                            wavefrontType,
                                            limitToPupil,
                                            (arrayWavefront.ctypes.data_as(POINTER(c_double))))
        print ("WFS_CalcWavefront Error: {}".format(error))
        return arrayWavefront

class AO_Control(): 
    def __init__(self, DM_dll_path, DM_dll_pathx, WFS_dll_path):      
        self.DM = DMH40dll(dll_path = DM_dll_path, dll_pathx = DM_dll_pathx)
        deviceIndex = 0
        self.DM.TLDFM_get_device_information(deviceIndex)
        self.DM.TLDFMX_init()
        self.DM.TLDFM_get_segment_count()
        self.DM.TLDFM_get_tilt_count()

        print ("DM Initialized")
        
        self.WFS = WFS20_5C(WFS_dll_path)
        self.WFS.WFS_GetInstrumentListInfo()
        self.WFS.WFS_init()
        self.spotsX, self.spotsY = self.WFS.WFS_ConfigureCam(pixelFormat = 0, camResolIndex = 0)
        self.WFS.WFS_SetPupil(pupilCenterXMm=0, pupilCenterYMm=0, pupilDiameterXMm=4.6, pupilDiameterYMm=4.6)
        
        print ("WFS Initialized")
        
    def Relax(self):
        '''
        Relax Mirror looping through all remaining steps stored in self.DM.remainingSteps.value 
        '''
        VoltageArray = self.DM.TLDFMX_relax(True)
        self.DM.TLDFM_set_segment_voltages(VoltageArray)

        while self.DM.remainingSteps.value > 0:
            print ("# of remaining steps = {}".format(self.DM.remainingSteps.value))
            time.sleep(0.01)
            VoltageArray = self.DM.TLDFMX_relax(False)
            self.DM.TLDFM_set_segment_voltages(VoltageArray)
            
        print ('Mirror Reset Complete')
        
    def MeasureSystemParameters(self, show = True):

        '''
        This function iterates through all TLDFMX_measure_system_parameters() along with getting a 
        Spotfield image,  CalcSpotstoReferenceDeviations() & ZernikeLsf() in order to get an input 
        array Zernike to use as an input for the next step in TLDFMX_measure_system_parameters().

        ERROR: -1074001404 TLDFMX_ERROR_ITER_AMPL is thrown at the last remaining step. 

        Set the loop of DM.remainingSteps.value > 1 to see this function run to the end and plot 
        all but the last wavefront step 
        '''

        self.WFS.WFS_TakeSpotfieldImage()
        self.WFS.WFS_CalcSpotsCentrDiaIntens(dynamicNoiseCut = 1)
        self.WFS.WFS_CalcSpotToReferenceDeviations(cancelWavefrontTilt=0)
        arrayZernikeUm, arrayZernikeOrdersUm, roCMm = self.WFS.WFS_ZernikeLsf(zernikeOrders=4)
        VoltageArray = self.DM.TLDFMX_measure_system_parameters(True, [])
        self.DM.TLDFM_set_segment_voltages(VoltageArray)

        if show == True:
            fig, ax = plt.subplots(6,6)
            fig.set_figheight(10)
            fig.set_figwidth(13)
            fig.subplots_adjust(hspace=.5)
            ax = np.ravel(ax)
            i=0

        while self.DM.remainingSteps.value > 0: #Set to 1 to complete the plot up until the last remaining step
            print ('Input DM = {}\n remaining steps = {}'.format(np.ctypeslib.as_array(VoltageArray), self.DM.remainingSteps.value))
            time.sleep(0.05)
  
            self.WFS.WFS_TakeSpotfieldImage()
            self.WFS.WFS_CalcSpotsCentrDiaIntens(dynamicNoiseCut = 0)
            self.WFS.WFS_CalcSpotToReferenceDeviations(cancelWavefrontTilt=0)   
            if show == True:
                arrayWavefront = self.WFS.WFS_CalcWavefront(wavefrontType=0, limitToPupil=1)
                WF = arrayWavefront[:self.spotsY.value,:self.spotsX.value].copy()
                ax[i].imshow(WF, origin='lower')
                ax[i].set_title('Step #{}'.format(i+1))
                i+=1
            arrayZernikeUm, arrayZernikeOrdersUm, roCMm = self.WFS.WFS_ZernikeLsf(zernikeOrders=4)
            VoltageArray = self.DM.TLDFMX_measure_system_parameters(False, arrayZernikeUm)
            self.DM.TLDFM_set_segment_voltages(VoltageArray)

        if show == True:
            plt.show()

if __name__ == "__main__":

    WFS_dll_path = r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\WFS_64.dll'
    DM_dll_path =  r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFM_64.dll'
    DM_dll_pathx =  r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFMX_64.dll'

    AO = AO_Control(DM_dll_path, DM_dll_pathx, WFS_dll_path)

    # AO.Relax()
    AO.WFS.WFS_SetExposureTime(20) #ms
    AO.MeasureSystemParameters()
