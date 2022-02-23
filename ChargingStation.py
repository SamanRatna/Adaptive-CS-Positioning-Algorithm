# ------------------------------------------ CONSIDERATIONS ------------------------------------------
# SoC changes at the rate of 1% per unit km
# ----------------------------------------------------------------------------------------------------

# Libraries
import collections
from tabnanny import check
from turtle import distance
from numpy import number
import pandas as pd
import matplotlib.pyplot as plt

# Constant parameters
num_of_bikes = 100                      # Total number of Bikes
total_distance_in_one_trip = 132        # distance in kms
SoC_logging_distance = 1                # distance in kms

# Which Data will I be using from Spreadsheet?
dataColumn = "Random1"
# dataColumn = "Normal1"

# Number of times Bike travels from A to B and viceversa
total_number_of_trips = range(1)
present_SoC = 0
# Distance travelled by that instant in the present trip
distance_travelled = 0
counter = 0
result = {}

checkpoint_1 = 44
checkpoint_2 = 88
checkpoint_3 = 132
# checkpoint_4 = 132

checkpoint_1_distances = {}
checkpoint_2_distances = {}
checkpoint_3_distances = {}
checkpoint_4_distances = {}

weighted_summation_for_checkpoint = 0
total_frequency_for_checkpoint = 1

weighted_summation_for_checkpoint1 = 0
total_frequency_for_checkpoint1 = 1

weighted_summation_for_checkpoint2 = 0
total_frequency_for_checkpoint2 = 1

weighted_summation_for_checkpoint3 = 0
total_frequency_for_checkpoint3 = 1

weighted_summation_for_checkpoint4 = 0
total_frequency_for_checkpoint4 = 1

strandedRiderCount = 0
total_strandedRiderCount = 0

leastSoC_before_getting_stranded = 5
checkpoint_charging_frequency = 0
checkpointOccupancy = {}
chargingSoC = {}
checkpointwise_Stranded_Count = {}

total_rider_count = 0

strandedRiderCount_checkpoint1 = 0
strandedRiderCount_checkpoint2 = 0
strandedRiderCount_checkpoint3 = 0
strandedRiderCount_checkpoint4 = 0

checkpoint1_charging_frequency = 0
checkpoint2_charging_frequency = 0
checkpoint3_charging_frequency = 0
checkpoint4_charging_frequency = 0

anxietyLevels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
anxietyLevelFrequency = [0, 0, 0, 0, 0, 0, 0, 0, 0]

all_charging_SoC = []

# SoC data input for the system
df = pd.read_excel(r'data_collection.xlsx')
initial_values = []

print("Data Column Used:                            ", dataColumn)
for count in range(len(df[dataColumn])):
    initial_values.append(df[dataColumn][count])

# Output Variable define
points_of_recharge = []

# print(initial_values)

# Begin Logic
for initial_SoC in initial_values:
   
    present_SoC = initial_SoC

    distance_travelled = 0

    for trip_number in total_number_of_trips:

        if(trip_number % 2 == 0):

            while (distance_travelled < total_distance_in_one_trip):

                if (present_SoC <= 50):

                    points_of_recharge.append(distance_travelled)
                    # print(present_SoC)
                    # print(points_of_recharge)
                    # print("--")
                    present_SoC = 100                           # Bike recharged to full when reached to 50%
                
                else:

                    # Bike SoC decreases with increase in travel displacement by 1km
                    present_SoC -= 1
                    # print("SoC is decreasing")

                # Increase distance travelled by 1km
                distance_travelled += 1
                # print(distance_travelled)

        elif (trip_number % 2 == 1):

            while (distance_travelled <= total_distance_in_one_trip and distance_travelled > 0):

                if (present_SoC <= 50):

                    points_of_recharge.append(distance_travelled)
                    present_SoC = 100                           # Bike recharged to full when reached to 50%
                
                else:
                    
                    # Bike SoC decreases with increase in travel displacement by 1km
                    present_SoC -= 1

                # Increase distance travelled by 1km
                distance_travelled -= 1


# Arrange Dictionary keys in ascending order
def ascendingKeys(frequency_of_occurence):
    for i in sorted(frequency_of_occurence):
        result.update({
            i: frequency_of_occurence[i]
        })
    print('---------------------- SORTED DICTIONARY : KEY as DISTANCE, VALUE as FREQUENCY -----------------------------')
    print(result)

# print("Points of Recharge:")
# print(sorted(points_of_recharge))
ctr = collections.Counter(points_of_recharge)
# print("Values for ctr:")
# print(ctr)
frequency = dict(ctr)
ascendingKeys(frequency)

Distance_x_axis = list(result.keys())
Frequency_y_axis = list(result.values())

print("\n")
print("Points of Recharge")
print(Distance_x_axis)
print(len(Distance_x_axis))

# plt.plot(Distance_x_axis, Frequency_y_axis)
# plt.xlabel('Distance')
# plt.ylabel('Frequency')
# plt.show()

# For sets of 2 such that the distance between those two points(d): 25km < d < 50km

collection_of_set_of_two = []

for point_head in Distance_x_axis:

    for point_tail in Distance_x_axis:

        if ((point_tail - point_head >= 25) and (point_tail - point_head <= 50)):

            set_of_two = []
            set_of_two.append(point_head)
            set_of_two.append(point_tail)
            collection_of_set_of_two.append(set_of_two)

# print(collection_of_set_of_two)
print(len(collection_of_set_of_two))

# For sets of 3 such that the distance between the adjacent 3 points(d): 25km < d < 50km

collection_of_set_of_three = []

for point_head in Distance_x_axis:

    for point_tail1 in Distance_x_axis:

        if ((point_tail1 - point_head >= 25) and (point_tail1 - point_head <= 50)):

            for point_tail2 in Distance_x_axis:

                if ((point_tail2 - point_tail1 >= 25) and (point_tail2 - point_tail1 <= 50)):

                    set_of_three = []
                    set_of_three.append(point_head)
                    set_of_three.append(point_tail1)
                    set_of_three.append(point_tail2)
                    
                    collection_of_set_of_three.append(set_of_three)

# print(collection_of_set_of_three)
print(len(collection_of_set_of_three))



