# Author(s): Nazban Darukhanawalla
"""
"""

import inspect 

class TLDFMX_ERROR_NODATA(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_NODATA"
        super().__init__(self.msg)

class TLDFMX_ERROR_NOTINIT(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_NOTINIT"
        super().__init__(self.msg)

class TLDFMX_ERROR_NOSUP_TARGET(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_NOSUP_TARGET"
        super().__init__(self.msg)

class TLDFMX_ERROR_ITERATION(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_ITERATION"
        super().__init__(self.msg)

class TLDFMX_ERROR_ITER_AMPL(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_ITER_AMPL"
        super().__init__(self.msg)

class TLDFMX_ERROR_ITER_CROSS_AMPL(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_ITER_CROSS_AMPL"
        super().__init__(self.msg)

class TLDFMX_ERROR_ITER_DATA_INV(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_ITER_DATA_INV"
        super().__init__(self.msg)

class TLDFMX_ERROR_AMPL_CONVERT(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_AMPL_CONVERT"
        super().__init__(self.msg)

class TLDFMX_ERROR_AMPL_RANGE(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_AMPL_RANGE. Looks like the input amplitude might be out of range!"
        super().__init__(self.msg)

class TLDFMX_ERROR_UNKNOWN(Exception):
    """
    """

    def __init__(self):
        """
        """
        self.msg = "TLDFMX_ERROR_UNKNOWN, Not like it's missing. It's literally UNKNOWN according to the documentation"
        super().__init__(self.msg)
