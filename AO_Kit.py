# Author(s): Nazban Darukhanawalla

import numpy as np
import matplotlib.pyplot as plt
import time
import enum
from ctypes import *
from Thorlabs_DM_dll import DMH40dll
from WFSdll import WFS20_5C

WFS_dll_path = r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\WFS_64.dll'

DM_dll_path =  r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFM_64.dll'
DM_dll_pathx =  r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFMX_64.dll'

class ZernikeCoeff(enum.Enum):
    Z_NULL = 0

    Z3 = 1
    Z4 = 2
    Z5 = 4
    Z6 = 8
    Z7 = 16
    Z8 = 32
    Z9 = 64
    Z10 = 128
    Z11 = 256
    Z12 = 512
    Z13 = 1024
    Z14 = 2048

    Z_All = int('0xFFFFFFFF', 0)

    
class DMH40():
        
    def __init__(self, DM_dll_path, DM_dll_pathx):
        self.device = DMH40dll(dll_path = DM_dll_path, dll_pathx = DM_dll_pathx)
        deviceIndex = 0

        self.device.TLDFM_get_device_information(deviceIndex)

        print ("DeviceIndex = {} \n Device Available = {}".format(deviceIndex, self.device.DeviceAvailable))

        self.device.TLDFMX_init()
        self.device.TLDFM_get_segment_count()
        self.device.TLDFM_get_tilt_count()

        print ("Device Initialized")
        self.WFS = WFS20(WFS_dll_path) #Encapsulate WFS class to run MeasureSystemParameters()
    
    def Close(self):
        self.device.TLDFM_close()

    def Relax(self):
        '''
        Relax Mirror
        '''
        #print ("# of segments = {} & # of tilt = {}".format(self.device.segmentCount.value, self.device.tiltCount.value))
        VoltageArray = self.device.TLDFMX_relax(True)
        self.device.TLDFM_set_segment_voltages(VoltageArray)
        # print ("# of remaining steps = {}".format(self.device.remainingSteps))

        while self.device.remainingSteps.value > 0:
            #self.device.TLDFM_get_segment_voltages()
            #print ("# of remaining steps = {}".format(self.device.remainingSteps))
            #print ("Segment Voltages = {}".format(np.ctypeslib.as_array(VoltageArray)[0]))
            time.sleep(0.01)
            VoltageArray = self.device.TLDFMX_relax(False)
            self.device.TLDFM_set_segment_voltages(VoltageArray)
        print ('Mirror Reset Complete')
    
    def MeasureSystemParameters(self, show=False, autoexposure=True):
        
        # self.Relax()
        # if autoexposure==True:
        #     self.WFS.TakeImageAutoExposure()
        #     isFirstStep = True
        #     arrayZernikeUm, arrayZernikeOrdersUm, roCMm = self.WFS.ZernikeLsf(cancelWavefrontTilt=0, zernikeOrders=4)
        #     VoltageArray, remainingSteps = self.device.TLDFMX_measure_system_parameters(isFirstStep, arrayZernikeUm)
        #     print ('Input DM = {}\n remaining steps = {}'.format(np.ctypeslib.as_array(VoltageArray), remainingSteps))
        #     self.device.TLDFM_set_segment_voltages(VoltageArray)
        #     WF, arrayScaleX, arrayScaleY = self.WFS.GetWavefrontfromSpotfield(cancelWavefrontTilt=0)

        #     if show == True:
        #         fig, ax = plt.subplots(6,6)
        #         fig.set_figheight(10)
        #         fig.set_figwidth(13)
        #         fig.subplots_adjust(hspace=.5)
        #         ax = np.ravel(ax)
        #         ax[0].imshow(WF, origin='lower', extent = [arrayScaleX[0],arrayScaleX[-1], arrayScaleY[0], arrayScaleY[-1]])
        #         ax[0].set_title('Step #0')
        #     isFirstStep = False
            
        #     for i in range(self.device.remainingSteps):
        #         time.sleep(0.05)
        #         self.WFS.TakeImageAutoExposure()
        #         arrayZernikeUm, arrayZernikeOrdersUm, roCMm = self.WFS.ZernikeLsf(cancelWavefrontTilt=0, zernikeOrders=4)
        #         VoltageArray, remainingSteps = self.device.TLDFMX_measure_system_parameters(isFirstStep, arrayZernikeUm)
        #         print ('Input DM = {}\n remaining steps = {}'.format(np.ctypeslib.as_array(VoltageArray), self.device.remainingSteps))
        #         self.device.TLDFM_set_segment_voltages(VoltageArray)
        #         if show == True:
        #             WF, arrayScaleX, arrayScaleY = self.WFS.GetWavefrontfromSpotfield(cancelWavefrontTilt=0)
        #             ax[i+1].imshow(WF, origin='lower', extent = [arrayScaleX[0],arrayScaleX[-1], arrayScaleY[0], arrayScaleY[-1]])
        #             # if i % 2 == 0:
        #             #     j = (-1 * ((i + 2) // 2))
        #             # else:
        #             #     j = ((i + 2) // 2)
        #             ax[i+1].set_title('Step #{}'.format(i+1))
        #         #c+=1
        if autoexposure == False:
            self.WFS.TakeImage(exposureTimeSet=20)
            arrayZernikeUm, arrayZernikeOrdersUm, roCMm = self.WFS.ZernikeLsf(cancelWavefrontTilt=0, zernikeOrders=4)
            VoltageArray = self.device.TLDFMX_measure_system_parameters(True, [])
            self.device.TLDFM_set_segment_voltages(VoltageArray)
            if show == True:
                    fig, ax = plt.subplots(6,6)
                    fig.set_figheight(10)
                    fig.set_figwidth(13)
                    fig.subplots_adjust(hspace=.5)
                    ax = np.ravel(ax)
                    i=0

            while self.device.remainingSteps.value > 0:
                time.sleep(0.05)
                if show == True:
                    WF, arrayScaleX, arrayScaleY = self.WFS.GetWavefrontfromSpotfield(cancelWavefrontTilt=0)
                    ax[i].imshow(WF, origin='lower', extent = [arrayScaleX[0],arrayScaleX[-1], arrayScaleY[0], arrayScaleY[-1]])
                    ax[i].set_title('Step #{}'.format(i+1))
                    i+=1
                print ('Input DM = {}\n remaining steps = {}'.format(np.ctypeslib.as_array(VoltageArray), self.device.remainingSteps.value))
                self.WFS.TakeImage(exposureTimeSet=20)
                arrayZernikeUm, arrayZernikeOrdersUm, roCMm = self.WFS.ZernikeLsf(cancelWavefrontTilt=0, zernikeOrders=4)
                VoltageArray = self.device.TLDFMX_measure_system_parameters(False, arrayZernikeUm)
                self.device.TLDFM_set_segment_voltages(VoltageArray)
        if show == True:
            plt.show()
    
    def Calibrate(self, show = False, autoexposure = True):
        '''Combined MeasureSystemParameters and GetSystemParameters'''
        self.MeasureSystemParameters(show, autoexposure)
        rotationMode, flipMode, maxDeviceZernikeAmplitudes, isDataValid = self.device.TLDFMX_get_system_parameters()
        self.device.TLDFMX_set_rotation_mode(rotationMode)
        self.device.TLDFMX_set_flip_mode(flipMode)
        self.MeasureSystemParameters(show, autoexposure)
        self.GetSystemParameters()


    def GetSystemParameters(self):
        rotationMode, flipMode, maxDeviceZernikeAmplitudes, isDataValid = self.device.TLDFMX_get_system_parameters()
        if isDataValid == True:
            print ('Device Max Z Amplitudes = {}'.format(maxDeviceZernikeAmplitudes))
        if isDataValid == False:
            print ('Invalid System Parameters')
            print ('Device Max Z Amplitudes = {}'.format(maxDeviceZernikeAmplitudes))

    def ConvertZernikeAmp(self):
            self.WFS.TakeImageAutoExposure()
            arrayZernikeUm, arrayZernikeOrdersUm, roCMm = self.WFS.ZernikeLsf(cancelWavefrontTilt=0, zernikeOrders=4)       

            deviceZernikeAmplitudes = self.device.TLDFMX_convert_measured_zernike_amplitudes(arrayZernikeUm)
            
            return deviceZernikeAmplitudes
    
    def GetFlatWavefront(self, zernikes = ZernikeCoeff.Z_All):
            zernikes = c_uint32(zernikes.value)
            for i in range(0, 10, 1):
                print ('i={}'.format(i))
                self.WFS.TakeImageAutoExposure()
                arrayZernikeUm, arrayZernikeOrdersUm, roCMm = self.WFS.ZernikeLsf(cancelWavefrontTilt=0, zernikeOrders=4)       
                deviceZernikeAmplitudes, VoltageArray = self.device.TLDFMX_get_flat_wavefront(zernikes, arrayZernikeUm)

                self.device.TLDFM_set_segment_voltages(VoltageArray)
            

    def SetZernike(self, zernike = ZernikeCoeff.Z_All, zernikeAmplitude = 0):
        print (zernike.value)
        zernike = c_uint32(zernike.value)
        print (zernike)
        zernikeAmplitude = c_double(zernikeAmplitude)
        VoltageArray = self.device.TLDFMX_calculate_single_zernike_pattern(zernike, zernikeAmplitude)
        self.device.TLDFM_set_segment_voltages(VoltageArray)
        print("Example pattern is set.")

        #print ("Input Zernike Segment Voltages = {}".format(np.ctypeslib.as_array(VoltageArray)))

        GetVoltageArray = self.device.TLDFM_get_segment_voltages()
        #print ("Confirmed Segment Voltages = {}".format(np.ctypeslib.as_array(GetVoltageArray)))

    def SetZernikeArray(self, zernikes = ZernikeCoeff.Z_All, zernikeAmplitudes = np.zeros(12)):
        zernikes = c_uint32(zernikes.value)
        VoltageArray = self.device.TLDFMX_calculate_zernike_pattern(zernikes, zernikeAmplitudes)
        self.device.TLDFM_set_segment_voltages(VoltageArray)
        print("Example pattern is set.")

        #print ("Input Zernike Segment Voltages = {}".format(np.ctypeslib.as_array(VoltageArray)))

        GetVoltageArray = self.device.TLDFM_get_segment_voltages()
        #print ("Confirmed Segment Voltages = {}".format(np.ctypeslib.as_array(GetVoltageArray)))    


class WFS20():
    
    def __init__(self, WFS_dll_path):
        self.device = WFS20_5C(dll_path=WFS_dll_path)

        #Select a device and get its info
        devStatus = self.device.WFS_GetInstrumentListInfo()

        if devStatus is not None:
            print ("error in WFS initialization" + self.device.WFS_error_message(devStatus))
        else:
            print('WFS deviceID: ' + str(self.device.deviceID.value))
            print('in use? ' + str(self.device.inUse.value))
            print('instrumentName: ' + str(self.device.instrumentName.value.decode('ascii')))
            print('instrumentSN: ' + str(self.device.instrumentSN.value.decode('ascii')))
            print('resourceName: ' + str(self.device.resourceName.value))

        self.device.WFS_init()

        self.spotsX, self.spotsY = self.device.WFS_ConfigureCam(pixelFormat = 0, camResolIndex = 0)
        '''
        Returns spotsX, spotsY
        Input: CamResolIndex
        For WFS20 instruments:
        Index  Resolution
        0    1440x1080            
        1    1080x1080            
        2     768x768              
        3     512x512              
        4     360x360              
        5     720x540, bin2
        6     540x540, bin2
        7     384x384, bin2
        8     256x256, bin2
        9     180x180, bin2
        '''
        print('WFS camera configured')
        print('SpotsX:' + str(self.spotsX.value))
        print('SpotsY:' + str(self.spotsY.value))
        
        #Set Pupil to max as the device doesn't work without a pupil definition
        self.device.WFS_SetPupil(pupilCenterXMm=0, pupilCenterYMm=0, pupilDiameterXMm=12, pupilDiameterYMm=12)
   
    def Close(self):
        self.device.WFS_close()    

   
    def GetStatus(self, show = True):
        '''
        Gets the status of the device. 
        Parameters:
        Show: True prints all the flagged statuses
        Show: False returns the entire status dict to be used by another function (eg: auto exposure)
        '''
        deviceStatus = self.device.WFS_GetStatus()

        status_dict = self.device.decode_status_message(deviceStatus)
        if show == True:
            for (name, (value, bit_mask_dict)) in status_dict.items():
                if value == 1:
                    print('{}: {}: {}'.format(name, value, bit_mask_dict))
        else:
            return status_dict
        
    def SetHighspeed(self, highspeedMode = 0, adaptCentroids = 0, subractOffset = 0, allowAutoExposure = 0):
        self.device.WFS_SetHighspeedMode(highspeedMode, adaptCentroids, subractOffset, allowAutoExposure)

    def SetPupil(self, pupilCenterXMm = 0, pupilCenterYMm = 0, pupilDiameterXMm = 4.60, pupilDiameterYMm = 4.60):
        '''
        DEFAULT VALUES ARE BASED ON HOE4 (DM) SETUP AND ALINGMENT. DO NOT CHANGE UNLESS SETUP MOVES
        PupilCenter Valid Range: -5.0...+5.0mm
        PupilDiameter Valid Range: -0.1...+10.0mm
        PUPIL_DIA_MIN_MM = 0.5, PUPIL_DIA_MAX_MM = 12.0
        PUPIL_CTR_MIN_MM = -8, PUPIL_CTR_MAX_MM = 8
        '''
        self.device.WFS_SetPupil(pupilCenterXMm, pupilCenterYMm, pupilDiameterXMm, pupilDiameterYMm)

    def AutoSetPupil(self):
        '''Get Pupil parameters'''
        pupilCenterXMm, pupilCenterYMm, pupilDiameterXMm, pupilDiameterYMm = self.device.WFS_CalcBeamCentroidDia()
        '''Apply Pupil parameters'''
        self.device.WFS_SetPupil(pupilCenterXMm, pupilCenterYMm, pupilDiameterXMm, pupilDiameterYMm)

    def TakeImage(self, exposureTimeSet):
        error, self.exposure = self.device.WFS_SetExposureTime(exposureTimeSet)
        print('exposureTimeAct in SetExposureTime, ms: ' + str(self.exposure))
        self.exposure = self.device.WFS_GetExposureTime()
        print ('exposure time via GetExposureTime = {}'.format(self.exposure))
        if error is not None:
            errormessage = self.device.WFS_error_message(error)
            print ("error = {}".format(errormessage))
        self.device.WFS_TakeSpotfieldImage()

    def TakeImageAutoExposure(self):
        '''
        Need to create a loop with the get status functions 
        '''
        error, exposure, gain = self.device.WFS_TakeSpotfieldImageAutoExpos()
        status = self.device.WFS_GetStatus()
       
        '''Should eventually be this way once GetStatus is working'''
        # while status is not None:
        #     error, exposure, gain = self.device.WFS_TakeSpotfieldImageAutoExpos()
        
        for i in range(0, 20, 1):
            error, self.exposure, self.gain = self.device.WFS_TakeSpotfieldImageAutoExpos()
        
        print('Took spotfield image, auto exposure')
        print('exposureTimeAct, ms: ' + str(exposure))
        print('masterGainAct: ' + str(gain))

    def ShowSpotfield(self):
        #Show Image Buffer
        imageBuf, rows, columns = self.device.WFS_GetSpotfieldImage()
        imageBuf1, rows1, columns1 = self.device.WFS_GetSpotfieldImageCopy()
        #print ('ImageBuffer = {}, rows = {}, cols = {}'.format(np.ctypeslib.as_array(imageBuf1), rows, columns))
        imageBufnp = np.ctypeslib.as_array(imageBuf1, shape = ((rows-1, columns-1)))
        imageBufnp = imageBufnp.reshape((rows, columns))
        print (np.shape(imageBufnp))
        plt.imshow(imageBufnp)
        plt.title('Spotfield from {}; SN:{} \n Exposure Time = {} ms'.format(str(self.device.instrumentName.value.decode('ascii')), str(self.device.instrumentSN.value.decode('ascii')), self.exposure))
        plt.show()
        
    def GetWavefrontfromSpotfield(self, cancelWavefrontTilt=0, show = False):
        '''
        Inputs: 
        cancelWavefrontTilt = 0   calculate deviations normal
        cancelWavefrontTilt = 1   subtract mean deviation in pupil from all spot deviations
        '''
        #Calculate centroids, diameters, intensity (requires GetSpotCentroids() to output)
        self.device.WFS_CalcSpotsCentrDiaIntens(dynamicNoiseCut = 0)

        #calculate deviation from centroids
        self.device.WFS_CalcSpotToReferenceDeviations(cancelWavefrontTilt)
        #print ('WFS spot to reference deviations calculated')

        #Plot reference spots & deviations
        # arrayCentroidX, arrayCentroidY = device.WFS_GetSpotCentroids()
        # print ('array Centroid X = {}'.format(arrayCentroidX))

        #Get XYScale, remove trailing 0s from arrayScaleX and array 
        arrayScaleX, arrayScaleY = self.device.WFS_GetXYScale()
        arrayScaleX = (np.ctypeslib.as_array(arrayScaleX))
        arrayScaleY = (np.ctypeslib.as_array(arrayScaleY))
        non_zero_indices = np.nonzero(arrayScaleX)[0]
        arrayScaleX = arrayScaleX[:non_zero_indices[-1]+1]
        non_zero_indices = np.nonzero(arrayScaleY)[0]
        arrayScaleY = arrayScaleY[:non_zero_indices[-1]+1]

        # #Calculate wavefront
        arrayWavefront = self.device.WFS_CalcWavefront(wavefrontType=0, limitToPupil=1)
        #print (arrayWavefront)
        WF = arrayWavefront[:self.spotsY.value,:self.spotsX.value].copy()
    
        if show == True:
            plt.imshow(WF, origin='lower', extent = [arrayScaleX[0],arrayScaleX[-1], arrayScaleY[0], arrayScaleY[-1]])

            plt.title('Wavefront phase, um')
            plt.xlabel('X spots')
            plt.xlabel('Y spots')
            plt.colorbar()
            plt.show()
        return WF, arrayScaleX, arrayScaleY
    
    def ZernikeLsf(self, cancelWavefrontTilt, zernikeOrders):
        #Calculate centroids, diameters, intensity (requires GetSpotCentroids() to output)
        self.device.WFS_CalcSpotsCentrDiaIntens(dynamicNoiseCut = 1)

        #calculate deviation from centroids
        self.device.WFS_CalcSpotToReferenceDeviations(cancelWavefrontTilt)
        #print ('WFS spot to reference deviations calculated')
        
        arrayZernikeUm, arrayZernikeOrdersUm, roCMm = self.device.WFS_ZernikeLsf(zernikeOrders)
        # print ("Array of Zernike Coefficients = {}, \n Array of Zernike summarized to RMS amplitudes for each order = {} \
        #         \n Radius of Curvature ofr a spherical wavefront (defocus Z4 (Z[5])) = {}mm"\
        #         .format(np.ctypeslib.as_array(arrayZernikeUm)[0:9], np.ctypeslib.as_array(arrayZernikeOrdersUm), roCMm.value))
        
        return np.ctypeslib.as_array(arrayZernikeUm), np.ctypeslib.as_array(arrayZernikeOrdersUm), roCMm.value
    