# Author(s): Nazban Darukhanawalla
"""
"""
import numpy as np
import DMH40_errors
from ctypes import (windll, Structure, c_char_p, c_short, c_bool, c_char, c_long,
                    c_byte, c_int32, c_int, c_uint32, c_ushort, c_ulong, c_double, pointer, Array,
                    wintypes, byref)

ACCESS_KEY_ARRAY_LENGTH = 16612
SEGMENT_COUNT = 40 
TLDFM_INSTR_ERROR_OFFSET = -int("0x80000000", base = 16) + int("0x3FFC0900", base = 16) #_VI_ERROR + TLDFM_INSTR_WARNING_OFFSET
TLDFMX_ERROR_OFFSET = TLDFM_INSTR_ERROR_OFFSET + int("0xFF", base = 16) # TLDFM_INSTR_ERROR_OFFSET + 0xFF


class func_accessKeyArray(Array):
    """
    This is a c_types array class that contains 16612 bytes
    to store or send settings in batch to the controller.
    """
    _length_ = ACCESS_KEY_ARRAY_LENGTH
    _type_ = c_char
    
def load_dll(dll_path):
    """
    """
    return windll.LoadLibrary(dll_path)


class DMH40dll():
    
    ERRORNO_EXCEPTIONS = {(TLDFMX_ERROR_OFFSET + int("0x01", base = 16)): DMH40_errors.TLDFMX_ERROR_NODATA,
                          (TLDFMX_ERROR_OFFSET + int("0x02", base = 16)): DMH40_errors.TLDFMX_ERROR_NOTINIT,
                          (TLDFMX_ERROR_OFFSET + int("0x03", base = 16)): DMH40_errors.TLDFMX_ERROR_NOSUP_TARGET,
                          (TLDFMX_ERROR_OFFSET + int("0x04", base = 16)): DMH40_errors.TLDFMX_ERROR_ITERATION,
                          (TLDFMX_ERROR_OFFSET + int("0x05", base = 16)): DMH40_errors.TLDFMX_ERROR_ITER_AMPL,
                          (TLDFMX_ERROR_OFFSET + int("0x06", base = 16)): DMH40_errors.TLDFMX_ERROR_ITER_CROSS_AMPL,
                          (TLDFMX_ERROR_OFFSET + int("0x07", base = 16)): DMH40_errors.TLDFMX_ERROR_ITER_DATA_INV,
                          (TLDFMX_ERROR_OFFSET + int("0x08", base = 16)): DMH40_errors.TLDFMX_ERROR_AMPL_CONVERT,
                          (TLDFMX_ERROR_OFFSET + int("0x09", base = 16)): DMH40_errors.TLDFMX_ERROR_AMPL_RANGE,
                          (TLDFMX_ERROR_OFFSET + int("0xFF", base = 16)): DMH40_errors.TLDFMX_ERROR_UNKNOWN


    }

    def __init__(self, dll_path, dll_pathx):
        '''
        '''
           
        self._instrumentHandle = c_ulong()
        self._dll = load_dll(dll_path)
        self._dllx = load_dll(dll_pathx)

        self.IDQuery = True
        self.resetDevice = False
        self.resource = c_char_p(b"")
        self.deviceCount = c_int()
  
        
    def ErrorCode(self, errorno):
        """
        Raises the correct exception for the given error number
        """
        if errorno == 0:
            return
        # TODO: python 3.10 allows for case switches if we standardize on 3.10
        try:
            raise self.ERRORNO_EXCEPTIONS[errorno]()
        except KeyError:
            raise Exception("The follow error number was not listed in the known exceptions"
                            " please look it up in the throlabs C API and add to the kinesis "
                            "exception section. The error number {} {}".format(errorno, type(errorno)))
       

    '''
    -----------------------------------
    Global Functions
    -----------------------------------
    '''
    
    def TLDFM_get_device_count(self):
        '''
        Parameters
        -----------------------------
        ViSession instrumentHandle
        ViPUInt32 pDeviceCount
        '''

        return self.ErrorCode(self._dll.TLDFM_get_device_count(self._instrumentHandle, 
                                                               byref(self.deviceCount)))
        
    def TLDFM_get_device_information(self, deviceIndex):
        '''
        Parameters
        -----------------------------
        ViSession instrumentHandle ,
        ViUInt32 deviceIndex ,
        ViPChar manufacturer ,
        ViPChar instrumentName ,
        ViPChar serialNumber ,
        ViPBoolean pDeviceAvailable ,
        ViPChar resourceName
        '''
        self.manufacturer = c_char_p(b"")
        self.instrumentName = c_char_p(b"")
        self.serialNumber = c_char_p(b"")
        self.DeviceAvailable = c_bool()
        self.resourceName= c_char_p(b"")



        return self.ErrorCode(self._dll.TLDFM_get_device_information(self._instrumentHandle,
                                                                     deviceIndex, 
                                                                     self.manufacturer, 
                                                                     self.instrumentName, 
                                                                     self.serialNumber, 
                                                                     byref(self.DeviceAvailable), 
                                                                     self.resourceName
                                                                    ))
        
    '''
-----------------------------------
    required VXIpnp instrument driver functions
-----------------------------------
    ''' 
    
    def TLDFM_init(self):
        '''
        Parameters
        -----------------------------
        ViRsrc     resourceName ,
        ViBoolean  IDQuery ,
        ViBoolean  resetDevice ,
        ViPSession pInstrumentHandle
        '''
        self.ErrorCode(self._dll.TLDFM_init(self.resourceName.value, 
                                            self.IDQuery, 
                                            self.resetDevice, 
                                            byref(self._instrumentHandle)))
    def TLDFMX_init(self):
        '''
        Parameters
        -----------------------------
        ViRsrc     resourceName ,
        ViBoolean  IDQuery ,
        ViBoolean  resetDevice ,
        ViPSession pInstrumentHandle
        '''
        self.ErrorCode(self._dllx.TLDFMX_init(self.resourceName.value, 
                                            True, 
                                            True, 
                                            byref(self._instrumentHandle)))
    
    def TLDFM_close(self):
        '''
        Parameters
        -----------------------------
        ViSession  instrumentHandle
        '''    
        
        self.ErrorCode(self._dll.TLDFM_close(self._instrumentHandle))
        
    def TLDFM_reset(self):
        '''
        Parameters
        -----------------------------
        ViSession  instrumentHandle
        '''    
        self.ErrorCode(self._dll.TLDFM_reset(self._instrumentHandle))

    def TLDFM_self_test(self):
        '''
        Parameters
        -----------------------------
        ViSession  instrumentHandle,
        ViPInt16   pSelfTestResult,
        ViPChar    selfTestMessage
        '''
        SelfTestResult = c_int()
        selfTestMessage = c_char()
        self.ErrorCode(self._dll.TLDFM_self_test(self._instrumentHandle, 
                                                 byref(SelfTestResult), 
                                                 byref(selfTestMessage)))        
         
    def TLDFM_error_message(self, pErrorCode):
        '''
        Parameters
        -----------------------------
        ViSession  instrumentHandle,
        ViPStatus   pErrorCode,
        ViPChar     errorMessage
        '''
        pErrorCode = c_int32(pErrorCode)
        errorMessage = c_char()
        error = self.ErrorCode(self._dll.TLDFM_error_message(self._instrumentHandle, 
                                             pErrorCode,
                                             errorMessage))    
        if not error:
            return str(errorMessage)

    def TLDFMX_error_message(self, pErrorCode):
        '''
        Parameters
        -----------------------------
        ViSession  instrumentHandle,
        ViPStatus   pErrorCode,
        ViPChar     errorMessage
        '''

        pErrorCode = c_int32(pErrorCode)
        errorMessage = c_char()
        error = self.ErrorCode(self._dllx.TLDFMX_error_message(self._instrumentHandle, 
                                             pErrorCode,
                                             errorMessage))
        if not error:
            return str(errorMessage)   
        
    def TLDFM_revision_query(self, driverRevision: str, firmwareRevision: str):
        '''
        Parameters
        -----------------------------
        ViSession  instrumentHandle,
        ViPChar     driverRevision,
        ViPChar     firmwareRevision    
        '''
        self.ErrorCode(self._dll.TLDFM_revision_query(self._instrumentHandle, 
                                             c_char(driverRevision),
                                             c_char(firmwareRevision)))    
        
    def TLDFM_set_USB_access_mode(self, accessMode: int, requestedKey: str):
        '''
        Parameters
        ----------------------------
        ViSession instrumentHandle,
        ViUInt32  accessMode,
        ViString  requestedKey,
        ViChar    accessKey[]
        '''
        
        accessKeyArray = func_accessKeyArray()
        
        self.ErrorCode(self._dll.TLDFM_set_USB_access_mode(self._instrumentHandle,
                                                           c_int(accessMode),
                                                           c_char(requestedKey),
                                                           accessKeyArray))
    '''
-----------------------------------
    Segment Voltage Functions
-----------------------------------
    '''
    def TLDFM_set_segment_voltages(self, VoltageArray):
        '''
        Sets voltages of all mirrors 
        
        Parameters
        -----------
        '''

        #self.relaxPatternMirror = (c_double * (self.segmentCount.value))()

        return self.ErrorCode(self._dll.TLDFM_set_segment_voltages(self._instrumentHandle, 
                                                   VoltageArray))
                                                
    
       
    def TLDFM_get_segment_voltages(self):
        '''
        Gets voltages of all mirror segments
        Parameters
        -----------

        '''
        self.GetVoltageArray = (c_double * (self.segmentCount.value))()
        #print ("BEFORE Segment Voltages = {}".format(np.ctypeslib.as_array(self.relaxPatternMirror)[0]))
        error =  self.ErrorCode(self._dll.TLDFM_get_segment_voltages(self._instrumentHandle, 
                                                   byref(self.GetVoltageArray))) 
        if not error:
            #print ("AFTER Segment Voltages = {}".format(np.ctypeslib.as_array(self.relaxPatternMirror)[0]))
            return self.GetVoltageArray

    '''
-----------------------------------
    Get Functions (TLDFM)
-----------------------------------
    '''

    def TLDFM_get_segment_count(self):
        self.segmentCount = c_uint32()
        
        
        error = self.ErrorCode(self._dll.TLDFM_get_segment_count(self._instrumentHandle,
                                                                byref(self.segmentCount
                                                                )))
        if not error: 
            self.relaxPatternMirror = (c_double * (self.segmentCount.value))()

    
    def TLDFM_get_tilt_count(self):
        self.tiltCount = c_uint32()

        error = self.ErrorCode(self._dll.TLDFM_get_tilt_count(self._instrumentHandle,
                                                                byref(self.tiltCount
                                                                )))
        if not error: 
            self.relaxPatternArms = (c_double * (self.tiltCount.value))()

    '''
-----------------------------------
    Action/Status Functions (TLDFMX)
-----------------------------------
    '''

    def TLDFMX_measure_system_parameters(self, isFirstStep, measuredZernikeAmplitudes):
        '''
        This function measures the properties of the optical setup between the Deformable Mirror and a Wavefront Sensor.
        Determined parameters are
        - the required rotation and flip option for the Zernike pattern
        - the maximum achievable Zernike amplitudes.
        A successful run of this function is a precondition to perform an adaptive optics control loop using function TLDFMX_get_flat_wavefront.
        The function needs to be called repeatedly within a loop until the 'Remaining Steps' parameter returns 0.
        This function just calculates and returns mirror test pattern which have to be set separately to the physical device by using TLDFM base driver functions like TLDFM_set_segment_voltages.
        The caller needs to commit the resulting Zernike amplitudes measured by a Wavefront Sensor during the next call to this function.
        After all measurement steps were performed without errors, the measured properties of the optical setup are returned by function TLDFMX_get_system_parameters.
        You need to call functions  TLDFMX_set_rotation_mode and TLDFMX_set_flip_mode in order to set the required options active.
        Note:
        (1) Be sure you have the optical setup properly aligned and the beams are centered to the device apertures.
        (2) The pupil of the DMP40 (10 mm diameter) needs to be adapted to the pupil of the Wavefront Sensor by using optical lenses, mirrors or similar means.
        (3) You may need to program a short pause (for instance 5 ms) between setting the test voltage pattern to the device and requesting a new measurement result from the Wavefront Sensor in order to allow the DMP40 electronics and mechanics to settle.
        (4) Be sure to trigger a new Wavefront Sensor measurement and do not use old camera images taken before the new test pattern was applied.
        '''
        isFirstStep = c_bool(isFirstStep)
        measuredZernikeAmplitudes = (c_double * (len(measuredZernikeAmplitudes)))(*measuredZernikeAmplitudes)
        nextMirrorPattern = (c_double*(self.segmentCount.value))()

        if isFirstStep.value == True:
            self.remainingSteps = c_int32()

        error = self.ErrorCode(self._dllx.TLDFMX_measure_system_parameters(self._instrumentHandle,
                                                                           isFirstStep,
                                                                           measuredZernikeAmplitudes,
                                                                           nextMirrorPattern,
                                                                           byref(self.remainingSteps)
                                                                           ))
        if not error:
            return nextMirrorPattern
    
    def TLDFMX_get_system_parameters(self):
        
        rotationMode = c_double()
        flipMode = c_double()

        maxDeviceZernikeAmplitudes = (c_double*(12))()
        isDataValid = c_bool()

        error = self.ErrorCode(self._dllx.TLDFMX_get_system_parameters(self._instrumentHandle,
                                                                    byref(rotationMode),
                                                                    byref(flipMode),
                                                                    byref(maxDeviceZernikeAmplitudes),
                                                                    byref(isDataValid)))    
        return rotationMode, flipMode, np.ctypeslib.as_array(maxDeviceZernikeAmplitudes), isDataValid.value
    
    def TLDFMX_set_rotation_mode(self, rotationMode):

        return self.ErrorCode(self._dllx.TLDFMX_set_rotation_mode(self._instrumentHandle,
                                                                  rotationMode))
    
    def TLDFMX_set_flip_mode(self, flipMode):

        return self.ErrorCode(self._dllx.TLDFMX_set_flip_mode(self._instrumentHandle,
                                                                  flipMode))

    def TLDFMX_convert_measured_zernike_amplitudes(self, measuredZernikeAmplitudes):
        '''
        Converts WFS Zernike Amplitudes to DM Zernike Amplitudes
        '''
        
        measuredZernikeAmplitudes = (c_double * (len(measuredZernikeAmplitudes)))(*measuredZernikeAmplitudes)
        deviceZernikeAmplitudes = (c_double*(12))()

        error = self.ErrorCode(self._dllx.TLDFMX_convert_measured_zernike_amplitudes(self._instrumentHandle,
                                                                                     measuredZernikeAmplitudes,
                                                                                     deviceZernikeAmplitudes))

        if not error:
            return np.ctypeslib.as_array(deviceZernikeAmplitudes)

    def TLDFMX_relax(self, isFirstStep):
        '''
        Relax mirror, requires set voltage to apply output to mirror
        '''
        isFirstStep = c_bool(isFirstStep)
        devicePart = c_uint32(0)
        reload = c_bool(False)
        if isFirstStep.value == True:
            self.remainingSteps = c_int32()
        VoltageArray = self.relaxPatternMirror
        error = self.ErrorCode(self._dllx.TLDFMX_relax(self._instrumentHandle,
                                                    devicePart,
                                                    isFirstStep,
                                                    reload,
                                                    VoltageArray,
                                                    self.relaxPatternArms,
                                                    byref(self.remainingSteps)
        ))
        if not error:
            return VoltageArray
            #print ("Segment Voltages = {}".format(np.ctypeslib.as_array(self.relaxPatternMirror)))
    

    def TLDFMX_calculate_single_zernike_pattern(self, zernike, deviceZernikeAmplitude):
        '''
        Calculates mirror voltages based on single input zernike, requires set voltage to apply to mirror
        '''
        mirrorPattern = (c_double*(self.segmentCount.value))()
        error = self.ErrorCode(self._dllx.TLDFMX_calculate_single_zernike_pattern(self._instrumentHandle,
                                                                                  zernike,
                                                                                  deviceZernikeAmplitude,
                                                                                  mirrorPattern
                                                                                  ))
        if not error:
            return mirrorPattern

    # def TLDFMX_convert_measured_zernike_amplitudes(self, )

    def TLDFMX_calculate_zernike_pattern(self, zernikes, deviceZernikeAmplitudes):
        '''
        Calculates mirror voltages based on input zernike array, requires set voltage to apply to mirror
        '''
        mirrorPattern = (c_double*(self.segmentCount.value))()
        
        cdeviceZernikeAmplitudes =  (c_double*(len(deviceZernikeAmplitudes)))(*deviceZernikeAmplitudes)
        error = self.ErrorCode(self._dllx.TLDFMX_calculate_zernike_pattern(self._instrumentHandle,
                                                                                  zernikes,
                                                                                  cdeviceZernikeAmplitudes,
                                                                                  mirrorPattern
                                                                                  ))
        if not error:
            return mirrorPattern        

    def TLDFMX_get_flat_wavefront(self, zernikes, measuredZernikeAmplitudes):

        measuredZernikeAmplitudes = (c_double * (len(measuredZernikeAmplitudes)))(*measuredZernikeAmplitudes)
        deviceZernikeAmplitudes = (c_double*(12))()
        mirrorPattern = (c_double*(self.segmentCount.value))()

        error = self.ErrorCode(self._dllx.TLDFMX_get_flat_wavefront(self._instrumentHandle,
                                                                    zernikes,
                                                                    measuredZernikeAmplitudes,
                                                                    deviceZernikeAmplitudes,
                                                                    mirrorPattern))
        
        if not error:
            return deviceZernikeAmplitudes, mirrorPattern

'''DATA FUNCTIONS'''

