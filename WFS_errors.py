# Author(s): Nazban Darukhanawalla
"""
"""

import inspect 


# class ERRORLIST(Exception):
    
#     def WFS_ERROR_NO_SENSOR_CONNECTED(self):
#         """
#         """
#         self.msg = "{}: WFS_ERROR_NO_SENSOR_CONNECTED".format(__name__)
#         super().__init__(self.msg)
          
    
class WFS_ERROR_NO_SENSOR_CONNECTED(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_NO_SENSOR_CONNECTED"
        super().__init__(self.msg)
        
        
class WFS_ERROR_OUT_OF_MEMORY(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_OUT_OF_MEMORY"
        super().__init__(self.msg)
        
class WFS_ERROR_INVALID_HANDLE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_INVALID_HANDLE"
        super().__init__(self.msg)

class WFS_ERROR_CAM_NOT_CONFIGURED(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_CAM_NOT_CONFIGURED"
        super().__init__(self.msg)
        
class WFS_ERROR_PIXEL_FORMAT(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_PIXEL_FORMAT"
        super().__init__(self.msg)
        
class WFS_ERROR_EEPROM_CHECKSUM(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_EEPROM_CHECKSUM"
        super().__init__(self.msg)
        
class WFS_ERROR_EEPROM_CAL_DATA(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_EEPROM_CAL_DATA"
        super().__init__(self.msg)

class WFS_ERROR_OLD_REF_FILE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_OLD_REF_FILE"
        super().__init__(self.msg)

class WFS_ERROR_NO_REF_FILE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_NO_REF_FILE"
        super().__init__(self.msg)

class WFS_ERROR_CORRUPT_REF_FILE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_CORRUPT_REF_FILE"
        super().__init__(self.msg)

class WFS_ERROR_WRITE_FILE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_WRITE_FILE"
        super().__init__(self.msg)

class WFS_ERROR_INSUFF_SPOTS_FOR_ZERNFIT(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_INSUFF_SPOTS_FOR_ZERNFIT"
        super().__init__(self.msg)

class WFS_ERROR_TOO_MANY_SPOTS_FOR_ZERNFIT(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_TOO_MANY_SPOTS_FOR_ZERNFIT"
        super().__init__(self.msg)

class WFS_ERROR_FOURIER_ORDER(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_FOURIER_ORDER"
        super().__init__(self.msg)

class WFS_ERROR_NO_RECON_DEVIATIONS(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_NO_RECON_DEVIATIONS"
        super().__init__(self.msg)

class WFS_ERROR_NO_PUPIL_DEFINED(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_NO_PUPIL_DEFINED"
        super().__init__(self.msg)

class WFS_ERROR_WRONG_PUPIL_DIA(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_WRONG_PUPIL_DIA"
        super().__init__(self.msg)

class WFS_ERROR_WRONG_PUPIL_CTR(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_WRONG_PUPIL_CTR"
        super().__init__(self.msg)

class WFS_ERROR_INVALID_CAL_DATA(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_INVALID_CAL_DATA"
        super().__init__(self.msg)

class WFS_ERROR_INTERNAL_REQUIRED(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_INTERNAL_REQUIRED"
        super().__init__(self.msg)

class WFS_ERROR_ROC_RANGE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_ROC_RANGE"
        super().__init__(self.msg)

class WFS_ERROR_NO_USER_REFERENCE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_NO_USER_REFERENCE"
        super().__init__(self.msg)

class WFS_ERROR_AWAITING_TRIGGER(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_AWAITING_TRIGGER"
        super().__init__(self.msg)

class WFS_ERROR_NO_HIGHSPEED(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_NO_HIGHSPEED"
        super().__init__(self.msg)

class WFS_ERROR_HIGHSPEED_ACTIVE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_HIGHSPEED_ACTIVE"
        super().__init__(self.msg)

class WFS_ERROR_HIGHSPEED_NOT_ACTIVE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_HIGHSPEED_NOT_ACTIVE"
        super().__init__(self.msg)

class WFS_ERROR_HIGHSPEED_WINDOW_MISMATCH(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_HIGHSPEED_WINDOW_MISMATCH"
        super().__init__(self.msg)

class WFS_ERROR_NOT_SUPPORTED(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_NOT_SUPPORTED"
        super().__init__(self.msg)

class WFS_ERROR_SPOT_TRUNCATED(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_SPOT_TRUNCATED"
        super().__init__(self.msg)

class WFS_ERROR_NO_SPOT_DETECTED(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_NO_SPOT_DETECTED"
        super().__init__(self.msg)

class WFS_ERROR_TILT_CALCULATION(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "WFS_ERROR_TILT_CALCULATION"
        super().__init__(self.msg)
