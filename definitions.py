
# Libraries
import collections
from tabnanny import check
from turtle import distance
from unittest import case, findTestCases
from numpy import number
import pandas as pd
import matplotlib.pyplot as plt
import operator
import math
import itertools
import csv

# Simulation flag
simulation_status = 1


#Constants
UPHILL   = 1
DOWNHILL = 2
PLAIN    = 3


# Constant parameters
num_of_bikes                            = 100                           # Total number of Bikes
total_distance_in_one_trip              = 177                           # in km
SoC_logging_distance                    = 1                             # in km
full_charge_value                       = 100
number_of_charging_stations             = 2
distance_where_charging_starts          = 50
SoC_degradation_factor                  = 0
uphill_degradation_factor               = -2
downhill_degradation_factor             = -0.5
plain_terrain_degradation_factor        = -1
topography_dataset_distance             = [0, 12.5, 100, 112.5, 177]    # in km
threshold_SoC_where_charging_starts     = 50                            # in percentage
stranded_threshold_SoC                  = 5                             # in percentage
total_number_of_trips                   = range(2)                      # Number of times Bike travels from A to B and viceversa
leastSoC_before_getting_stranded        = 5                             # in percentage


# Variable initialization
x_axis_distance_in_a_trip               = []
y_axis_number_of_unstranded_riders      = []
filtered_list                           = []
discarded_list_count                    = 0
discarded_number_of_sets                = 0
present_SoC                             = 0
distance_travelled                      = 0
counter                                 = 0
result                                  = {}
strandedRiderCount                      = 0
checkpoint_charging_frequency           = 0
checkpointOccupancy                     = {}
chargingSoC                             = {}
checkpointwise_Stranded_Count           = {}
total_rider_count                       = 0
stranded_rider_count                    = 0
all_charging_SoC                        = []
AnxietyLevelCollection_setOfTwo         = []
AnxietyLevelCollection_setOfThree       = []
anxietyLevels                           = [1, 2, 3, 4, 5, 6, 7, 8, 9]
anxietyLevelFrequency                   = [0, 0, 0, 0, 0, 0, 0, 0, 0]
Distance_x_axis                         = 0
charge_count                            = 0
initial_values                          = [[] for _ in range(len(topography_dataset_distance))]
unhandled_cases                         = 0
stranded_rider_breakout_flag            = 0