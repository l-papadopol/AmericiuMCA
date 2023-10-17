#####################################################################
# Copyright(c) 2023, All rights reserved.
# Author:   Papadopol Lucian Ioan
# Date:     22.01.2023
# Version:  v1.0
# Function: Configuration for the EPICS based MAC Application protocol converter
#####################################################################
INTERFACE = '556AIM'
PV_NAMES = ['mcaTest:AIM_adc1', 'mcaTest:AIM_adc2']
PV_LENGTH = [1024, 1024] 
SPECTRA_SIZE = 1024  # Maximum spectra size
NUM_OF_CHANNELS = 1024
M_ADC = 0
SCHEDULE_UPDATE_SEC = 5.0


