# Author(s): Nazban Darukhanawalla

import numpy as np
import WFS_errors
import pyvisa 
from ctypes import (windll, Structure, c_char_p, c_short, c_bool, c_char, c_long, c_float,
                    c_byte, c_int32, c_int, c_uint32, c_uint8, c_ushort, c_ulong, c_double, pointer, POINTER, Array,
                    wintypes, byref, create_string_buffer)

dll_path = r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\WFS_64.dll'

LENGTH_CHAR_ARRAY = 512
MAX_ZERNIKE_MODES = 66
MAX_ZERNIKE_ORDERS = 10
MAX_SPOTS_Y = 80
MAX_SPOTS_X = 80


ERROR_OFFSET = -int("0x80000000", base = 16) + int("0x3FFC0900", base = 16) # = -1074001664


def load_dll(dll_path):
    """
    """
    return windll.LoadLibrary(dll_path)

class WFS20_5C():
    
    ERRORNO_EXCEPTIONS = {(ERROR_OFFSET + int("0x00", base = 16)): WFS_errors.WFS_ERROR_NO_SENSOR_CONNECTED,
                          (ERROR_OFFSET + int("0x01", base = 16)): WFS_errors.WFS_ERROR_OUT_OF_MEMORY,
                          (ERROR_OFFSET + int("0x02", base = 16)): WFS_errors.WFS_ERROR_INVALID_HANDLE,
                          (ERROR_OFFSET + int("0x03", base = 16)): WFS_errors.WFS_ERROR_CAM_NOT_CONFIGURED,
                          (ERROR_OFFSET + int("0x04", base = 16)): WFS_errors.WFS_ERROR_PIXEL_FORMAT,
                          (ERROR_OFFSET + int("0x05", base = 16)): WFS_errors.WFS_ERROR_EEPROM_CHECKSUM,
                          (ERROR_OFFSET + int("0x06", base = 16)): WFS_errors.WFS_ERROR_EEPROM_CAL_DATA,
                          (ERROR_OFFSET + int("0x07", base = 16)): WFS_errors.WFS_ERROR_OLD_REF_FILE,
                          (ERROR_OFFSET + int("0x08", base = 16)): WFS_errors.WFS_ERROR_NO_REF_FILE,
                          (ERROR_OFFSET + int("0x09", base = 16)): WFS_errors.WFS_ERROR_CORRUPT_REF_FILE,
                          (ERROR_OFFSET + int("0x0a", base = 16)): WFS_errors.WFS_ERROR_WRITE_FILE,
                          (ERROR_OFFSET + int("0x0b", base = 16)): WFS_errors.WFS_ERROR_INSUFF_SPOTS_FOR_ZERNFIT,
                          (ERROR_OFFSET + int("0x0c", base = 16)): WFS_errors.WFS_ERROR_TOO_MANY_SPOTS_FOR_ZERNFIT,
                          (ERROR_OFFSET + int("0x0d", base = 16)): WFS_errors.WFS_ERROR_FOURIER_ORDER,
                          (ERROR_OFFSET + int("0x0e", base = 16)): WFS_errors.WFS_ERROR_NO_RECON_DEVIATIONS,
                          (ERROR_OFFSET + int("0x0f", base = 16)): WFS_errors.WFS_ERROR_NO_PUPIL_DEFINED,
                          (ERROR_OFFSET + int("0x10", base = 16)): WFS_errors.WFS_ERROR_WRONG_PUPIL_DIA,
                          (ERROR_OFFSET + int("0x11", base = 16)): WFS_errors.WFS_ERROR_WRONG_PUPIL_CTR,
                          (ERROR_OFFSET + int("0x12", base = 16)): WFS_errors.WFS_ERROR_INVALID_CAL_DATA,
                          (ERROR_OFFSET + int("0x13", base = 16)): WFS_errors.WFS_ERROR_INTERNAL_REQUIRED,
                          (ERROR_OFFSET + int("0x14", base = 16)): WFS_errors.WFS_ERROR_ROC_RANGE,
                          (ERROR_OFFSET + int("0x15", base = 16)): WFS_errors.WFS_ERROR_NO_USER_REFERENCE,
                          (ERROR_OFFSET + int("0x16", base = 16)): WFS_errors.WFS_ERROR_AWAITING_TRIGGER,
                          (ERROR_OFFSET + int("0x17", base = 16)): WFS_errors.WFS_ERROR_NO_HIGHSPEED,
                          (ERROR_OFFSET + int("0x18", base = 16)): WFS_errors.WFS_ERROR_HIGHSPEED_ACTIVE,
                          (ERROR_OFFSET + int("0x19", base = 16)): WFS_errors.WFS_ERROR_HIGHSPEED_NOT_ACTIVE,
                          (ERROR_OFFSET + int("0x1a", base = 16)): WFS_errors.WFS_ERROR_HIGHSPEED_WINDOW_MISMATCH,
                          (ERROR_OFFSET + int("0x1a", base = 16)): WFS_errors.WFS_ERROR_NOT_SUPPORTED,
                          (ERROR_OFFSET + int("0x1a", base = 16)): WFS_errors.WFS_ERROR_SPOT_TRUNCATED,
                          (ERROR_OFFSET + int("0x1a", base = 16)): WFS_errors.WFS_ERROR_NO_SPOT_DETECTED,
                          (ERROR_OFFSET + int("0x1a", base = 16)): WFS_errors.WFS_ERROR_TILT_CALCULATION,

                          }
    
    STATUS_BITS = {
        'WFS_STATBIT_CON' : [0x00000001, "USB connection lost, set by driver"],
        'WFS_STATBIT_PTH' : [0x00000002, "Power too high (cam saturated)"],
        'WFS_STATBIT_PTL' : [0x00000004, "Power too low (low cam digits)"],
        'WFS_STATBIT_HAL' : [0x00000008, "High ambient light"],
        'WFS_STATBIT_SCL' : [0x00000010, "Spot contrast too low"],
        'WFS_STATBIT_ZFL' : [0x00000020, "Zernike fit failed because of not enough detected spots"],
        'WFS_STATBIT_ZFH' : [0x00000040, "Zernike fit failed because of too much detected spots"],
        'WFS_STATBIT_ATR' : [0x00000080, "Camera is still awaiting a trigger"],
        'WFS_STATBIT_CFG' : [0x00000100, "Camera is configured, ready to use"],
        'WFS_STATBIT_PUD' : [0x00000200, "Pupil is defined"],
        'WFS_STATBIT_SPC' : [0x00000400, "No. of spots or pupil or aoi has been changed"],
        'WFS_STATBIT_RDA' : [0x00000800, "Reconstructed spot deviations available"],
        'WFS_STATBIT_URF' : [0x00001000, "User reference data available"],
        'WFS_STATBIT_HSP' : [0x00002000, "Camera is in Highspeed Mode"],
        'WFS_STATBIT_MIS' : [0x00004000, "Mismatched centroids in Highspeed Mode"],
        'WFS_STATBIT_LOS' : [0x00008000, "low number of detected spots], warning ,reduced Zernike accuracy"],
        'WFS_STATBIT_FIL' : [0x00010000, "pupil is badly filled with spots], warning ,reduced Zernike accuracy"],
    }

    def __init__(self, dll_path):
        self._instrumentHandle = c_ulong()
        self._dll = load_dll(dll_path)

        self.instrumentListIndex = c_int32(0)
        self.deviceID = c_int32()
        self.inUse = c_int32()

        self.instrumentName = create_string_buffer(b"", 20)
        self.instrumentSN = create_string_buffer(b"", 20)
        self.resourceName = create_string_buffer(b"", 30)
        self.IDQuery = False
        self.resetDevice = False

    def ErrorCode(self, errorno):
        """
        Raises the correct exception for the given error number
        """
        if errorno == 0:
            return
        try:
            raise self.ERRORNO_EXCEPTIONS[errorno]()
        except KeyError:
            raise Exception("The follow error number was not listed in the known exceptions"
                            "The error number {}".format(errorno))
    
    # def ErrorCode(self, errorCode):
    #     errorMessage = c_char()
    #     if errorCode == 0:
    #         return

    #     error = self._dll.WFS_error_message(errorCode, errorMessage)
    #     if not error:
    #         raise (errorMessage)

    def decode_status_message(self, msg_int, bit_mask_dict=STATUS_BITS):
        """
        """
        results_dict = {}
        for (name, status_bit_mask) in bit_mask_dict.items():
            shift = (status_bit_mask[0] & -status_bit_mask[0]).bit_length() - 1 # get bit mask shift (number of trailing bits)
            value = (status_bit_mask[0]&msg_int) >> shift # get status bit value by bit-wise and and shifting to remove trailing bits

            results_dict[name] = [value, status_bit_mask[1]] 
        
        return results_dict

    '''
    -----------------------------------
    Utility Functions
    -----------------------------------
    '''
    
    def WFS_GetInstrumentListInfo(self):

        return self.ErrorCode(self._dll.WFS_GetInstrumentListInfo(self._instrumentHandle,
                                                              self.instrumentListIndex,
                                                              byref(self.deviceID),
                                                              byref(self.inUse),
                                                              self.instrumentName,
                                                              self.instrumentSN,
                                                              self.resourceName
                                                                ))
    
    def WFS_init(self):
        
        return self.ErrorCode(self._dll.WFS_init(self.resourceName,
                                                 self.IDQuery,
                                                 self.resetDevice,
                                                 byref(self._instrumentHandle)
                                                 ))
    
    def WFS_close(self):
        return self.ErrorCode(self._dll.WFS_close(self._instrumentHandle))
            
    def WFS_GetStatus(self):

        deviceStatus = c_int32()

        error =  self.ErrorCode(self._dll.WFS_GetStatus(self._instrumentHandle,
                                                      byref(deviceStatus)))
        if not error:
            #print ('device status = {}'.format(deviceStatus))
            return deviceStatus.value
        
    def WFS_error_message(self, errorCode):
        errorCode = c_int32(errorCode)
        errorMessage = (c_char * (LENGTH_CHAR_ARRAY)) ()
        
        error =  self.ErrorCode(self._dll.WFS_error_message(self._instrumentHandle,
                                                        errorCode,
                                                        errorMessage)) 
        if not error:
            return str(errorMessage.value)  
          
    def WFS_error_query(self):
        errorCode = c_int32()
        errorMessage = (c_char * (LENGTH_CHAR_ARRAY)) ()
        
        return self.ErrorCode(self._dll.WFS_error_query(self._instrumentHandle,
                                                        byref(errorCode),
                                                        errorMessage))

    def WFS_GetXYScale(self): 
        arrayScaleX = (c_float * (MAX_SPOTS_X)) ()
        arrayScaleY = (c_float * (MAX_SPOTS_Y)) ()

        error = self.ErrorCode(self._dll.WFS_GetXYScale(self._instrumentHandle,
                                                        arrayScaleX,
                                                        arrayScaleY))
        
        if not error:
            return arrayScaleX, arrayScaleY
        
    '''
    -----------------------------------
    Configuration Functions
    -----------------------------------
    '''   
     
    def WFS_ConfigureCam(self, pixelFormat, camResolIndex):
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
        pixelFormat = c_int32(pixelFormat)
        camResolIndex = c_int32(camResolIndex)
        spotsX = c_int32()
        spotsY = c_int32()
        
        error =  self.ErrorCode(self._dll.WFS_ConfigureCam(self._instrumentHandle,
                                                         pixelFormat,
                                                         camResolIndex,
                                                         byref(spotsX),
                                                         byref(spotsY)))
        
        if not error:
            return spotsX, spotsY
        
    def WFS_SetPupil(self, pupilCenterXMm, pupilCenterYMm, pupilDiameterXMm, pupilDiameterYMm):
        '''
        PupilCenter Valid Range: -5.0...+5.0mm
        PupilDiameter Valid Range: -0.1...+10.0mm
        PUPIL_DIA_MIN_MM = 0.5, PUPIL_DIA_MAX_MM = 12.0
        PUPIL_CTR_MIN_MM = -8, PUPIL_CTR_MAX_MM = 8
        '''
        pupilCenterXMm = c_double(pupilCenterXMm)
        pupilCenterYMm = c_double(pupilCenterYMm)
        pupilDiameterXMm = c_double(pupilDiameterXMm)
        pupilDiameterYMm = c_double(pupilDiameterYMm)
        
        return self.ErrorCode(self._dll.WFS_SetPupil(self._instrumentHandle,
                                                     pupilCenterXMm,
                                                     pupilCenterYMm,
                                                     pupilDiameterXMm,
                                                     pupilDiameterYMm))
    def WFS_SetExposureTime(self, exposureTimeSet):
        '''
        Input: Exposure time (ms)
        Output: Exposure time set by WFS (ms)
        '''
        exposureTimeSet = c_double(exposureTimeSet)
        exposureTimeAct = c_double()
        #print ('ExposureTimeSet in dll file = {}'.format(exposureTimeSet))
        error = self.ErrorCode(self._dll.WFS_SetExposureTime(self._instrumentHandle,
                                                            exposureTimeSet,
                                                            byref(exposureTimeAct)))
        if not error:
            return error, exposureTimeAct
    
    def WFS_SetMasterGain(self, masterGainSet = 1):
        '''
        Input: Master Gain (set to 1 for WFS20)
        Output: Master Gain (set to 1 for WFS20)
        Why did I even make this function
        '''
        
        masterGainSet = c_double(masterGainSet)
        masterGainAct = c_double(masterGainAct)
        
        error = self.ErrorCode(self._dll.WFS_SetMasterGain(self._instrumentHandle,
                                                            masterGainSet,
                                                            masterGainAct))
        if not error:
            return masterGainAct
    
    def WFS_GetExposureTime(self):
        '''
        Output: Exposure time set by WFS (ms)
        '''

        exposureTimeAct = c_double()
        error = self.ErrorCode(self._dll.WFS_GetExposureTime(self._instrumentHandle,
                                                            byref(exposureTimeAct)))
        if not error:
            return exposureTimeAct

    def WFS_SetHighspeedMode(self, highspeedMode, adaptCentroids, substractOffset, allowAutoExposure):
        highspeedMode= c_int32(highspeedMode)
        adaptCentroids = c_int32(adaptCentroids)
        substractOffset = c_int32(substractOffset)
        allowAutoExposure = c_int32(allowAutoExposure)

        return self.ErrorCode(self._dll.WFS_SetHighspeedMode(self._instrumentHandle,
                                                             highspeedMode,
                                                             adaptCentroids,
                                                             substractOffset,
                                                             allowAutoExposure))
    '''
    -----------------------------------
    Data Functions
    -----------------------------------
    '''

    def WFS_TakeSpotfieldImage(self):
        '''
        This function receives a spotfield image from the WFS camera into a driver buffer. 
        The reference to this buffer is provided by function GetSpotfieldImage() and an image copy is returned by function GetSpotfieldImageCopy().
        In case of unsuited image exposure the function sets the appropriate status bits. Use function GetStatus() to check the reason.
        '''
        return self.ErrorCode(self._dll.WFS_TakeSpotfieldImage(self._instrumentHandle))
         
    
    def WFS_TakeSpotfieldImageAutoExpos(self):
        '''
        This function tries to find optimal exposure and gain settings and then it receives a spotfield image from the WFS camera into a driver buffer. 
        The reference to this buffer is provided by function GetSpotfieldImage() and an image copy is returned by function GetSpotfieldImageCopy().
        The exposure and gain settings used for this image are returned.
        In case of still unsuited image exposure the function sets the appropriate status bits. Use function GetStatus() to check the reason.
        output - Exposure Time, Master Gain
        '''
        exposureTimeAct = c_double()
        masterGainAct = c_double()
        
        error =  self.ErrorCode(self._dll.WFS_TakeSpotfieldImageAutoExpos(self._instrumentHandle,
                                                                        byref(exposureTimeAct),
                                                                        byref(masterGainAct)))
        
        if not error:
            return error, float(exposureTimeAct.value), float(masterGainAct.value)

    def WFS_GetSpotfieldImage(self):
        imageBuf = c_uint8()
        self.rows = c_int32()
        self.columns = c_int32()
        
        error = self.ErrorCode(self._dll.WFS_GetSpotfieldImage(self._instrumentHandle,
                                                               byref(imageBuf),
                                                               byref(self.rows),
                                                               byref(self.columns)))
        
        if not error:
            return imageBuf, self.rows.value, self.columns.value
        

    def WFS_GetSpotfieldImageCopy(self):
        imageBuf = (c_uint8 * (self.rows.value * self.columns.value)) ()
        self.rows = c_int32()
        self.columns = c_int32()
        
        error = self.ErrorCode(self._dll.WFS_GetSpotfieldImageCopy(self._instrumentHandle,
                                                               byref(imageBuf),
                                                               byref(self.rows),
                                                               byref(self.columns)))
        
        if not error:
            return imageBuf, self.rows.value, self.columns.value 

    def WFS_CalcBeamCentroidDia(self):
        beamCentroidXMm = c_double()
        beamCentroidYMm = c_double()
        beamDiameterXMm = c_double()
        beamDiameterYMm = c_double()

        error = self.ErrorCode(self._dll.WFS_CalcBeamCentroidDia(self._instrumentHandle,
                                                                byref(beamCentroidXMm),
                                                                byref(beamCentroidYMm),
                                                                byref(beamDiameterXMm),
                                                                byref(beamDiameterYMm)))
        if not error:
            return beamCentroidXMm, beamCentroidYMm, beamDiameterXMm, beamDiameterYMm

    def WFS_CalcSpotsCentrDiaIntens(self, dynamicNoiseCut, calculateDiameters = 0):
        dynamicNoiseCut = c_int32(dynamicNoiseCut)
        calculateDiameters = c_int32(calculateDiameters)
        
        return self.ErrorCode(self._dll.WFS_CalcSpotsCentrDiaIntens(self._instrumentHandle,
                                                                    dynamicNoiseCut,
                                                                    calculateDiameters))

    def WFS_CalcSpotToReferenceDeviations(self, cancelWavefrontTilt):
        '''
        
        '''
        cancelWavefrontTilt = c_int32(cancelWavefrontTilt)
        
        return self.ErrorCode(self._dll.WFS_CalcSpotToReferenceDeviations(self._instrumentHandle,
                                                                          cancelWavefrontTilt))        
          
    def WFS_CalcWavefront(self, wavefrontType, limitToPupil):
        '''
        wavefrontType 
        This parameter defines the type of wavefront to calculate.
        Valid settings:
        0   Measured Wavefront
        1   Reconstructed Wavefront based on Zernike coefficients
        2   Difference between measured and reconstructed Wavefront
        Note: Function WFS_CalcReconstrDeviations needs to be called prior to this function in case of Wavefront type 1 and 2.
        '''
        wavefrontType = c_int32(wavefrontType)
        '''        
        limitToPupil	
        This parameter defines if the Wavefront should be calculated based on all detected spots or only within the defined pupil.
        Valid settings:
        0   Calculate Wavefront for all spots
        1   Limit Wavefront to pupil interior
        '''
        limitToPupil = c_int32(limitToPupil)
        '''
        arrayWavefront
        This parameter returns a two-dimensional array of float containing the wavefront data in µm.
        The required array size is [MAX_SPOTS_Y][MAX_SPOTS_X].
        '''
        #arrayWavefront = np.zeros((MAX_SPOTS_Y,MAX_SPOTS_X),dtype = np.float32)
        arrayWavefront = np.empty(dtype=c_float, shape=(MAX_SPOTS_Y, MAX_SPOTS_X)) 
        
        error = self.ErrorCode(self._dll.WFS_CalcWavefront(self._instrumentHandle,
                                                      wavefrontType,
                                                      limitToPupil,
                                                      (arrayWavefront.ctypes.data_as(POINTER(c_double)))))
        if not error:
            return arrayWavefront
        
    def WFS_GetSpotCentroids(self):
        arrayCentroidX = np.zeros((MAX_SPOTS_Y,MAX_SPOTS_X),dtype = np.float32)
        arrayCentroidY = np.zeros((MAX_SPOTS_Y,MAX_SPOTS_X),dtype = np.float32)
        
        error = self.ErrorCode(self._dll.WFS_GetSpotCentroids(self._instrumentHandle,
                                                             arrayCentroidX.ctypes.data_as(POINTER(c_double))),
                                                             arrayCentroidY.ctypes.data_as(POINTER(c_double)))
        if not error:
            return arrayCentroidX, arrayCentroidY
        
    def WFS_GetSpotDiameters(self):
        arrayCentroidX = np.zeros((MAX_SPOTS_Y,MAX_SPOTS_X),dtype = np.float32)
        arrayCentroidY = np.zeros((MAX_SPOTS_Y,MAX_SPOTS_X),dtype = np.float32)
        
        error = self.ErrorCode(self._dll.WFS_GetSpotDiameters(self._instrumentHandle,
                                                             arrayCentroidX.ctypes.data_as(POINTER(c_double))),
                                                             arrayCentroidY.ctypes.data_as(POINTER(c_double)))
        if not error:
            return arrayCentroidX, arrayCentroidY
                
    def WFS_AverageImage(self, averageCount):
        '''
        This function generates an averaged image from a number of input camera images in ImageBuf. The function returns after each call and the summarized image is stored in ImageBufAveraged.
        As soon as the desired number of averages in AverageCount is reached ImageBuf and ImageBufAveraged return both the averaged image data and AverageDataReady returns 1 instead of 0.
        Note: As soon as the image size is changed by function ConfigureCam the averaging process is re-started. This function is not available in Highspeed Mode!
        '''   
        averageCount = c_int32(averageCount)
        averageDataReady = c_int32()
        
        return self.ErrorCode(self._dll.WFS_AverageImage(self._instrumentHandle,
                                                  averageCount,
                                                  byref(averageDataReady))) 

    
    def WFS_ZernikeLsf(self, zernikeOrders):
        '''
        This function calculates the spot deviations (centroid with respect to its reference) and performs a least square fit to the desired number of Zernike functions.
        Output results are the Zernike coefficients up to the desired number of Zernike modes and an array summarizing these coefficients to rms amplitudes for each Zernike order. 
        '''
        
        self.zernikeOrders = c_int32(zernikeOrders)
        arrayZernikeUm = (c_float * (MAX_ZERNIKE_MODES + 1)) ()
        arrayZernikeOrdersUm = (c_float * (MAX_ZERNIKE_ORDERS + 1)) ()
        roCMm = c_double()
        
        error = self.ErrorCode(self._dll.WFS_ZernikeLsf(self._instrumentHandle,
                                                       byref(self.zernikeOrders),
                                                       arrayZernikeUm,
                                                       arrayZernikeOrdersUm,
                                                       byref(roCMm)))
        if not error:
            return arrayZernikeUm, arrayZernikeOrdersUm, roCMm
    
    def WFS_CalcReconstrDeviations(self, arrayZernikeRoconstruct, doSphericalReference):
        '''
        This function calculates the reconstructed spot deviations based on the calculated Zernike coefficients.
        Note: This function needs to run prior to function WFS_CalcWavefront when the reconstructed or difference Wavefront should be calculated.
        '''
        
        arrayZernikeRoconstruct =  (c_int32) * (MAX_ZERNIKE_MODES + 1) (*arrayZernikeRoconstruct)
        doSphericalReference = c_int32(doSphericalReference)
        
        fitErrMean = c_double()
        fitErrStdev = c_double()
        
        return self.ErrorCode(self._dll.WFS_CalcReconstrDeviations(self._instrumentHandle,
                                                                   self.zernikeOrders,
                                                                   arrayZernikeRoconstruct,
                                                                   doSphericalReference,
                                                                   byref(fitErrMean),
                                                                   byref(fitErrStdev)))
        