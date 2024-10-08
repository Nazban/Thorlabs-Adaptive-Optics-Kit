# Author(s): Nazban Darukhanawalla

# Errors at Line 106 & Line 115

from ctypes import *
import time

WFS = cdll.LoadLibrary(r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\WFS_64.dll')
DM = cdll.LoadLibrary(r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFM_64.dll')
DMx = cdll.LoadLibrary(r'C:\Program Files\IVI Foundation\VISA\Win64\Bin\TLDFMX_64.dll')

# Initialize DMP40 
instrumentHandle_DM = c_ulong()
IDQuery_DM = True
resetDevice_DM = False
resource_DM = c_char_p(b"")
deviceCount_DM = c_int()
manufacturer_DM = c_char_p(b"")
instrumentName_DM = c_char_p(b"")
serialNumber_DM = c_char_p(b"")
DeviceAvailable_DM = c_bool()
resourceName_DM= c_char_p(b"")
deviceIndex_DM = 0

DM.TLDFM_get_device_information(instrumentHandle_DM, deviceIndex_DM, manufacturer_DM, instrumentName_DM, serialNumber_DM, byref(DeviceAvailable_DM), resource_DM)
DMx.TLDFMX_init(resource_DM.value, IDQuery_DM, resetDevice_DM, byref(instrumentHandle_DM))

segmentCount = c_uint32()
tiltCount = c_uint32()
DM.TLDFM_get_segment_count(instrumentHandle_DM, byref(segmentCount))
DM.TLDFM_get_tilt_count(instrumentHandle_DM, byref(tiltCount))

print ("DM Initialized")

#Initialize WFS20-5C
instrumentHandle_WFS = c_ulong()
instrumentListIndex_WFS = c_int32(0)
deviceID_WFS = c_int32()
inUse_WFS = c_int32()

instrumentName_WFS = create_string_buffer(b"", 20)
instrumentSN_WFS = create_string_buffer(b"", 20)
resourceName_WFS = create_string_buffer(b"", 30)
IDQuery_WFS = False
resetDevice_WFS = False

WFS.WFS_GetInstrumentListInfo(instrumentHandle_WFS,instrumentListIndex_WFS,byref(deviceID_WFS),byref(inUse_WFS),instrumentName_WFS,instrumentSN_WFS,resourceName_WFS)
WFS.WFS_init(resourceName_WFS,IDQuery_WFS,resetDevice_WFS,byref(instrumentHandle_WFS))

spotsX = c_int32()
spotsY = c_int32()
WFS.WFS_ConfigureCam(instrumentHandle_WFS,c_int32(0),c_int32(0),byref(spotsX),byref(spotsY))

WFS.WFS_SetPupil(instrumentHandle_WFS, c_double(0), c_double(0), c_double(4.6), c_double(4.6))

exposureTimeSet = c_double(20)
exposureTimeAct = c_double()
WFS.WFS_SetExposureTime(instrumentHandle_WFS,exposureTimeSet,byref(exposureTimeAct))

print ("WFS Initialized")

'''
--------------------------------------
ISSUE 1: Measure System Parameters - System Calibration - ERROR: -1074001404 TLDFMX_ERROR_ITER_AMPL is thrown at the last remaining step at Line 101
--------------------------------------
'''
remainingSteps = c_int32()
nextMirrorPattern = (c_double * (segmentCount.value))()

dynamicNoiseCut = c_int32(0)
calculateDiameters = c_int32(0)
cancelWavefrontTilt = c_int32(0)

MAX_ZERNIKE_MODES = 66
MAX_ZERNIKE_ORDERS = 10

zernikeOrders = c_int32(4)
arrayZernikeUm = (c_float * (MAX_ZERNIKE_MODES + 1)) ()
arrayZernikeOrdersUm = (c_float * (MAX_ZERNIKE_ORDERS + 1)) ()
roCMm = c_double()


WFS.WFS_TakeSpotfieldImage(instrumentHandle_WFS)
WFS.WFS_CalcSpotsCentrDiaIntens(instrumentHandle_WFS,dynamicNoiseCut,calculateDiameters)
WFS.WFS_CalcSpotToReferenceDeviations(instrumentHandle_WFS,cancelWavefrontTilt)

WFS.WFS_ZernikeLsf(instrumentHandle_WFS,byref(zernikeOrders),arrayZernikeUm,arrayZernikeOrdersUm,byref(roCMm))

error = DMx.TLDFMX_measure_system_parameters(instrumentHandle_DM,c_bool(True),arrayZernikeUm,nextMirrorPattern,byref(remainingSteps))
print ("TLDFMX_measure_system_parameters Error Code = ", error)
DM.TLDFM_set_segment_voltages(instrumentHandle_DM, nextMirrorPattern)

while remainingSteps.value > 0:
    time.sleep(0.05)
    print ("# of remaining steps = {}".format(remainingSteps.value))
        
    WFS.WFS_TakeSpotfieldImage(instrumentHandle_WFS)
    WFS.WFS_CalcSpotsCentrDiaIntens(instrumentHandle_WFS,dynamicNoiseCut,calculateDiameters)
    WFS.WFS_CalcSpotToReferenceDeviations(instrumentHandle_WFS,cancelWavefrontTilt)

    WFS.WFS_ZernikeLsf(instrumentHandle_WFS,byref(zernikeOrders),arrayZernikeUm,arrayZernikeOrdersUm,byref(roCMm))

    # measuredZernikeAmplitudes = (c_double * (len(arrayZernikeUm)))(*arrayZernikeUm)

    error1 = DMx.TLDFMX_measure_system_parameters(instrumentHandle_DM,c_bool(False),arrayZernikeUm,nextMirrorPattern,byref(remainingSteps)) #ERROR: -1074001404 TLDFMX_ERROR_ITER_AMPL is thrown at the last remaining step
    print ("TLDFMX_measure_system_parameters Error Code = {}".format(error1))
    DM.TLDFM_set_segment_voltages(instrumentHandle_DM, nextMirrorPattern)

'''
ISSUE 2: Error code with the Error Message Function TLDFMX_error_message
'''
ErrorCode = c_int32(-1074001404) #Error code from Error1
errorMessage = c_char_p()
error2 = DMx.TLDFMX_error_message(instrumentHandle_DM, ErrorCode, errorMessage) #ERROR: -1074003965 is thrown when trying to run this function
print ("TLDFMX_error_message Error Code = {}".format(error2))

