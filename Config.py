#!/usr/bin/env python3

### AUTOCLICKER SCRIPT ###

import Utils
import ctypes
from inspect import getmembers, isfunction

UtilsFunctions = getmembers(Utils, isfunction)
Delimeter = ','

def AutoRun(ConfigTxt):
    for lineNumb, lineText in enumerate(ConfigTxt.splitlines()):
        # Skip commented lines and blank lines
        if not lineText.startswith('#') and lineText != '':
            # Call the function from unit "Utils" that matches the first word of the
            # "ConfigTxt" lines and give the next words of that line as parameters.
            lineElem = lineText.split(Delimeter)
            funcName = lineElem[0]
            funcParams = lineElem[1:]
            try:
                callFunc = [item[1] for item in UtilsFunctions if item[0]==funcName][0]
                if callFunc:
                    callFunc(*funcParams)
            except IndexError as e:
                raise ctypes.windll.user32.MessageBoxW(0, f'Error on line {lineNumb} of the configuration file.'+
                                                          f'\n\nPlease ensure that the function name "{funcName}" is spelled correctly and that the capitalization is correct.'+
                                                          f'\n\nException raised: {e}',
                                                          'Configuration error', 0x00000010)
            except TypeError as e:
                raise ctypes.windll.user32.MessageBoxW(0, f'Error on line {lineNumb} of the configuration file.'+
                                                          f'\n\nPlease ensure that all the parameters for the function "{funcName}" are included.'+
                                                          f'\n\nException raised: {e}',
                                                          'Configuration error', 0x00000010)
