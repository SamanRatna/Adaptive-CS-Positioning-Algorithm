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
import operator

# Constant parameters
num_of_bikes = 100                      # Total number of Bikes
total_distance_in_one_trip = 132        # distance in kms
SoC_logging_distance = 1                # distance in kms

# Which Data will I be using from Spreadsheet?
dataColumn = "Random1"
# dataColumn = "Normal1"

# Number of times Bike travels from A to B and viceversa
total_number_of_trips = range(2)
present_SoC = 0

# Distance travelled by that instant in the present trip
distance_travelled = 0
counter = 0
result = {}

checkpoint_1 = 44
checkpoint_2 = 88

checkpoint_1_distances = {}
checkpoint_2_distances = {}

weighted_summation_for_checkpoint = 0
total_frequency_for_checkpoint = 1

weighted_summation_for_checkpoint1 = 0
total_frequency_for_checkpoint1 = 1

weighted_summation_for_checkpoint2 = 0
total_frequency_for_checkpoint2 = 1

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

checkpoint1_charging_frequency = 0
checkpoint2_charging_frequency = 0

anxietyLevels = [1, 2, 3, 4, 5, 6, 7, 8, 9]
anxietyLevelFrequency = [0, 0, 0, 0, 0, 0, 0, 0, 0]

all_charging_SoC = []

AnxietyLevelCollection_setOfTwo = []

# SoC data input for the system
df = pd.read_excel(r'data_collection.xlsx')
initial_values = []

print("Data Column Used:                            ", dataColumn)
for count in range(len(df[dataColumn])):
    initial_values.append(df[dataColumn][count])

# Output Variable define
points_of_recharge = []

# -------------------------------------------------------------------------------------

# PRINT POINTS OF RECHARGE WHEN 100 RIDERS RIDE FROM A->B AND THEN B->A

# -------------------------------------------------------------------------------------

# Begin Logic
for initial_SoC in initial_values:
   
    # present_SoC = initial_SoC

    distance_travelled = 0

    for trip_number in total_number_of_trips:

        if(trip_number % 2 == 0):

            present_SoC = initial_SoC

            while (distance_travelled < total_distance_in_one_trip):

                if (present_SoC <= 50):

                    points_of_recharge.append(distance_travelled)

                    # Bike recharged to full when reached to 50%
                    present_SoC = 100
                
                else:

                    # Bike SoC decreases with increase in travel displacement by 1km
                    present_SoC -= 1

                # Increase distance travelled by 1km
                distance_travelled += 1

        elif (trip_number % 2 == 1):

            present_SoC = initial_SoC

            while (distance_travelled <= total_distance_in_one_trip and distance_travelled > 0):

                if (present_SoC <= 50):

                    points_of_recharge.append(distance_travelled)

                    # Bike recharged to full when reached to 50%
                    present_SoC = 100                           
                
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
    # print('---------------------- SORTED DICTIONARY : KEY as DISTANCE, VALUE as FREQUENCY -----------------------------')
    # print(result)

ctr = collections.Counter(points_of_recharge)
frequency = dict(ctr)
ascendingKeys(frequency)

Distance_x_axis = list(result.keys())
Frequency_y_axis = list(result.values())

print("\n")
print("Points of Recharge")
print(Distance_x_axis)
print("Total number of Points of Recharge : ", len(Distance_x_axis))

# plt.plot(Distance_x_axis, Frequency_y_axis)
# plt.xlabel('Distance')
# plt.ylabel('Frequency')
# plt.show()





# -------------------------------------------------------------------------------------

# DETERMINE SET_OF_TWO (X,Y) SUCH THAT 25KM < (Y-X) < 50KM

# -------------------------------------------------------------------------------------

collection_of_set_of_two = []

for point_head in Distance_x_axis:

    for point_tail in Distance_x_axis:

        if ((point_tail - point_head >= 25) and (point_tail - point_head <= 50)):

            set_of_two = []
            set_of_two.append(point_head)
            set_of_two.append(point_tail)
            collection_of_set_of_two.append(set_of_two)

# -------------------------------------------------------------------------------------

# FILTER OUT STRANDED RIDERS FROM THE COLLECTION_SET_OF_TWO

# -------------------------------------------------------------------------------------

result_setofTwo = {}

_collection_of_set_of_two = []

# print("Count of total number of sets : ", len(collection_of_set_of_two))

copy_collection2 = collection_of_set_of_two

for set_of_two in collection_of_set_of_two:

    total_strandedRiderCount = 0
    chargingStationCheckpoints = set_of_two

    for initial_SoC in initial_values:

        distance_travelled = 0

        for trip_number in total_number_of_trips:

            count += 1

            if(trip_number % 2 == 0):

                present_SoC = initial_SoC

                # When the rider hasn't reached the destination
                while (distance_travelled < total_distance_in_one_trip):

                    if (distance_travelled in chargingStationCheckpoints):

                        checkpointIndex = chargingStationCheckpoints.index(distance_travelled)

                        if (present_SoC > leastSoC_before_getting_stranded and present_SoC <= 50):

                            present_SoC = 100
                            _collection_of_set_of_two.append(set_of_two)

                        elif (present_SoC <= leastSoC_before_getting_stranded):

                            total_strandedRiderCount += 1

                            if (checkpointIndex == 0):
                                strandedRiderCount_checkpoint1 += 1
                            elif (checkpointIndex == 1):
                                strandedRiderCount_checkpoint2 += 1

                            break
                    
                    distance_travelled += 1
                    present_SoC -= 1
            
            elif(trip_number % 2 == 1):

                present_SoC = initial_SoC

                # When the rider hasn't reached the destination
                while (distance_travelled <= total_distance_in_one_trip and distance_travelled > 0):

                    if (distance_travelled in chargingStationCheckpoints):

                        checkpointIndex = chargingStationCheckpoints.index(distance_travelled)

                        if (present_SoC > leastSoC_before_getting_stranded and present_SoC <= 50):

                            present_SoC = 100
                            _collection_of_set_of_two.append(set_of_two)

                        elif (present_SoC <= leastSoC_before_getting_stranded):

                            total_strandedRiderCount += 1

                            if (checkpointIndex == 0):
                                strandedRiderCount_checkpoint1 += 1
                            elif (checkpointIndex == 1):
                                strandedRiderCount_checkpoint2 += 1
                            
                            break
                    
                    distance_travelled -= 1
                    present_SoC -= 1

    result_setofTwo.update({
        tuple(set_of_two) : total_strandedRiderCount
    })

_result_setofTwo = {}

print("Count of total Sets of Two : ", len(result_setofTwo))

for x in result_setofTwo:

    if (result_setofTwo[x] == 0):

        _result_setofTwo.update({
            x : result_setofTwo[x]
        })

setofTwo_list = []

for item in _result_setofTwo.keys():

    setofTwo_list.append(list(item))


setofTwo_list = list(_result_setofTwo.keys())

print("Total number of unstranded riders: ", len(setofTwo_list))


# -------------------------------------------------------------------------------------

# ANXIETY LEVELS AVERAGE

# -------------------------------------------------------------------------------------

Anxiety_Avg_dict = {}


for set_of_two in setofTwo_list:

    anxietyLevelFrequency = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    strandedRiderCount_checkpoint1 = 0
    strandedRiderCount_checkpoint2 = 0

    checkpoint1_charging_frequency = 0
    checkpoint2_charging_frequency = 0

    total_strandedRiderCount = 0
    total_number_of_charges = 0

    chargingStationCheckpoints = set_of_two

    ending_SoC_list = []

    for initial_SoC in initial_values:

        distance_travelled = 0

        for trip_number in total_number_of_trips:

            if(trip_number % 2 == 0):

                present_SoC = initial_SoC

                # When the rider hasn't reached the destination
                while (distance_travelled < total_distance_in_one_trip):

                    if (distance_travelled in chargingStationCheckpoints):

                        checkpointIndex = chargingStationCheckpoints.index(distance_travelled)

                        if (present_SoC <= leastSoC_before_getting_stranded):

                            total_strandedRiderCount += 1

                            if (checkpointIndex == 0):
                                strandedRiderCount_checkpoint1 += 1
                            elif (checkpointIndex == 1):
                                strandedRiderCount_checkpoint2 += 1
                          
                            StrandedRiderStatus = 1

                            break

                        elif (present_SoC > leastSoC_before_getting_stranded and present_SoC <= 50):

                            # The rider charged to the nearest charging Station that was in the direction towards his destination

                            # Update frequency of the particular Checkpoint being used
                            if (checkpointIndex == 0):
                                checkpoint1_charging_frequency += 1
                            elif (checkpointIndex == 1):
                                checkpoint2_charging_frequency += 1
                            

                            if (present_SoC > 45 and present_SoC <= 50):
                                anxietyLevelFrequency[0] += 1

                            elif (present_SoC > 40 and present_SoC <= 45):
                                anxietyLevelFrequency[1] += 1

                            elif (present_SoC > 35 and present_SoC <= 40):
                                anxietyLevelFrequency[2] += 1

                            elif (present_SoC > 30 and present_SoC <= 35):
                                anxietyLevelFrequency[3] += 1

                            elif (present_SoC > 25 and present_SoC <= 30):
                                anxietyLevelFrequency[4] += 1

                            elif (present_SoC > 20 and present_SoC <= 25):
                                anxietyLevelFrequency[5] += 1

                            elif (present_SoC > 15 and present_SoC <= 20):
                                anxietyLevelFrequency[6] += 1

                            elif (present_SoC > 10 and present_SoC <= 15):
                                anxietyLevelFrequency[7] += 1

                            elif (present_SoC > 5 and present_SoC <= 10):
                                anxietyLevelFrequency[8] += 1

                            present_SoC = 100

                            strandedRiderCount = 0

                    # Rider just travelled 1 km
                    # Increase distance travelled by 1km
                    distance_travelled += 1

                    # Rider's SoC decreases by 1 %
                    present_SoC -= 1

                ending_SoC_list.append(present_SoC)

            elif(trip_number % 2 == 1):

                present_SoC = initial_SoC

                # When the rider hasn't reached the destination
                while (distance_travelled <= total_distance_in_one_trip and distance_travelled > 0):

                    if (distance_travelled in chargingStationCheckpoints):

                        checkpointIndex = chargingStationCheckpoints.index(distance_travelled)

                        if (present_SoC <= leastSoC_before_getting_stranded):

                            total_strandedRiderCount += 1

                            if (checkpointIndex == 0):
                                strandedRiderCount_checkpoint1 += 1
                            elif (checkpointIndex == 1):
                                strandedRiderCount_checkpoint2 += 1

                            StrandedRiderStatus = 1

                            break

                        elif (present_SoC > leastSoC_before_getting_stranded and present_SoC <= 50):

                            # The rider charged to the nearest charging Station that was in the direction towards his destination

                            # Update frequency of the particular Checkpoint being used
                            if (checkpointIndex == 0):
                                checkpoint1_charging_frequency += 1
                            elif (checkpointIndex == 1):
                                checkpoint2_charging_frequency += 1

                            if (present_SoC > 45 and present_SoC <= 50):
                                anxietyLevelFrequency[0] += 1

                            elif (present_SoC > 40 and present_SoC <= 45):
                                anxietyLevelFrequency[1] += 1

                            elif (present_SoC > 35 and present_SoC <= 40):
                                anxietyLevelFrequency[2] += 1

                            elif (present_SoC > 30 and present_SoC <= 35):
                                anxietyLevelFrequency[3] += 1

                            elif (present_SoC > 25 and present_SoC <= 30):
                                anxietyLevelFrequency[4] += 1

                            elif (present_SoC > 20 and present_SoC <= 25):
                                anxietyLevelFrequency[5] += 1

                            elif (present_SoC > 15 and present_SoC <= 20):
                                anxietyLevelFrequency[6] += 1

                            elif (present_SoC > 10 and present_SoC <= 15):
                                anxietyLevelFrequency[7] += 1

                            elif (present_SoC > 5 and present_SoC <= 10):
                                anxietyLevelFrequency[8] += 1

                            present_SoC = 100

                            strandedRiderCount = 0

                    # Rider just travelled 1 km
                    # Increase distance travelled by 1km
                    distance_travelled -= 1

                    # Rider's SoC decreases by 1 %
                    present_SoC -= 1

                ending_SoC_list.append(present_SoC)
    
    averageEndingSoC = sum(ending_SoC_list) / len(ending_SoC_list)

    total_number_of_charges = checkpoint1_charging_frequency + checkpoint2_charging_frequency

    i = 1
    summ = 0
    for _value in anxietyLevelFrequency:

        summ = summ + _value*i
        i += 1

        Anxiety_Avg_dict.update({
            tuple(set_of_two) : [(summ / total_number_of_charges), averageEndingSoC]
        })

# print(Anxiety_Avg_dict)

# -------------------------------------------------------------------------------------

# TOP 5 SET OF TWO WITH THE LEAST ANXIETY LEVELS

# -------------------------------------------------------------------------------------

data = Anxiety_Avg_dict

anxLevelList = []
sortedDict = {}

for i in range(5):
    minAnxTemp = 100
    for key, val in data.items():
        if val[0] < minAnxTemp:
            minAnxTemp = val[0]
            minKey = key
            minVal = val
    del data[(minKey)]
    sortedDict.update({minKey: minVal})

print("Sorted top 5 sets of Two with least anxiety levels : ")
print(sortedDict)



