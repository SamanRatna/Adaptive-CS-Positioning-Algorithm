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
checkpoint_3 = 132

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

AnxietyLevelCollection_setOfTwo = []
AnxietyLevelCollection_setOfThree = []

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
            # print("distance travelled : ", distance_travelled)

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
            # print("distance travelled : ", distance_travelled)



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
# print(Frequency_y_axis)

# plt.plot(Distance_x_axis, Frequency_y_axis)
# plt.xlabel('Distance')
# plt.ylabel('Frequency')
# plt.show()





# -------------------------------------------------------------------------------------

# DETERMINE SET_OF_TWO (X,Y) SUCH THAT 25KM < (Y-X) < 50KM

# -------------------------------------------------------------------------------------

# collection_of_set_of_two = []

# for point_head in Distance_x_axis:

#     for point_tail in Distance_x_axis:

#         if ((point_tail - point_head >= 25) and (point_tail - point_head <= 50)):

#             set_of_two = []
#             set_of_two.append(point_head)
#             set_of_two.append(point_tail)
#             collection_of_set_of_two.append(set_of_two)

# print(collection_of_set_of_two)
# print(len(collection_of_set_of_two))

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
print("Total number of set of three : ", len(collection_of_set_of_three))



# -------------------------------------------------------------------------------------

# FILTER OUT STRANDED RIDERS FROM THE COLLECTION_SET_OF_THREE

# -------------------------------------------------------------------------------------

result_setofThree = {}

_collection_of_set_of_three = []

# print("Count of total number of sets : ", len(collection_of_set_of_two))

copy_collection2 = collection_of_set_of_three

for set_of_three in collection_of_set_of_three:

    total_strandedRiderCount = 0
    chargingStationCheckpoints = set_of_three

    for initial_SoC in initial_values:

        distance_travelled = 0

        for trip_number in total_number_of_trips:

            if(trip_number % 2 == 0):

                present_SoC = initial_SoC

                # When the rider hasn't reached the destination
                while (distance_travelled < total_distance_in_one_trip):

                    if (distance_travelled in chargingStationCheckpoints):

                        checkpointIndex = chargingStationCheckpoints.index(distance_travelled)

                        if (present_SoC > leastSoC_before_getting_stranded and present_SoC <= 50):

                            present_SoC = 100

                        elif (present_SoC <= leastSoC_before_getting_stranded):

                            total_strandedRiderCount += 1

                            if (checkpointIndex == 0):
                                strandedRiderCount_checkpoint1 += 1
                            elif (checkpointIndex == 1):
                                strandedRiderCount_checkpoint2 += 1
                            elif (checkpointIndex == 2):
                                strandedRiderCount_checkpoint3 += 1
                            
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

                        elif (present_SoC <= leastSoC_before_getting_stranded):

                            total_strandedRiderCount += 1

                            if (checkpointIndex == 0):
                                strandedRiderCount_checkpoint1 += 1
                            elif (checkpointIndex == 1):
                                strandedRiderCount_checkpoint2 += 1
                            elif (checkpointIndex == 2):
                                strandedRiderCount_checkpoint3 += 1
                         
                            break
                    
                    distance_travelled -= 1
                    present_SoC -= 1

    result_setofThree.update({
        tuple(set_of_three) : total_strandedRiderCount
    })

# print(result_setofThree)


_result_setofThree = {}

# Distance_x_axis = list(result.keys())
# Frequency_y_axis = list(result.values())

for x in result_setofThree:

    # print(x)
    # print(result_setofThree[x])

    if (result_setofThree[x] == 0):

        _result_setofThree.update({
            x : result_setofThree[x]
        })

setofThree_list = []

for item in _result_setofThree.keys():

    setofThree_list.append(list(item))


setofThree_list = list(_result_setofThree.keys())

# print(setofThree_list)
# print(type(setofThree_list))
print("Total sets of Three with unstranded riders: ", len(setofThree_list))
print("Total number of set of three : ", len(collection_of_set_of_three))

# -------------------------------------------------------------------------------------

# ANXIETY LEVELS

# -------------------------------------------------------------------------------------

Anxiety_Avg_dict = {}

for set_of_three in setofThree_list:

    anxietyLevelFrequency = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    strandedRiderCount_checkpoint1 = 0
    strandedRiderCount_checkpoint2 = 0
    strandedRiderCount_checkpoint3 = 0

    checkpoint1_charging_frequency = 0
    checkpoint2_charging_frequency = 0
    checkpoint3_charging_frequency = 0

    total_strandedRiderCount = 0
    total_number_of_charges = 0

    chargingStationCheckpoints = set_of_three

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
                            elif (checkpointIndex == 2):
                                strandedRiderCount_checkpoint3 += 1
                            # elif (checkpointIndex == 3):
                            #     strandedRiderCount_checkpoint4 += 1

                            StrandedRiderStatus = 1

                            break

                        elif (present_SoC > leastSoC_before_getting_stranded and present_SoC <= 50):

                            # The rider charged to the nearest charging Station that was in the direction towards his destination

                            # Update frequency of the particular Checkpoint being used
                            if (checkpointIndex == 0):
                                checkpoint1_charging_frequency += 1
                            elif (checkpointIndex == 1):
                                checkpoint2_charging_frequency += 1
                            elif (checkpointIndex == 2):
                                checkpoint3_charging_frequency += 1
                            # elif (checkpointIndex == 3):
                            #     checkpoint4_charging_frequency += 1

                            # At what SoC values are each riders charging?
                            # chargingSoC_list.append(present_SoC)

                            # all_charging_SoC.append(present_SoC)

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
                            # checkpoint_charging_frequency = 0

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

                    # print("Current distance travelled is ", distance_travelled)

                    if (distance_travelled in chargingStationCheckpoints):

                        checkpointIndex = chargingStationCheckpoints.index(distance_travelled)

                        if (present_SoC <= leastSoC_before_getting_stranded):

                            total_strandedRiderCount += 1

                            if (checkpointIndex == 0):
                                strandedRiderCount_checkpoint1 += 1
                            elif (checkpointIndex == 1):
                                strandedRiderCount_checkpoint2 += 1
                            elif (checkpointIndex == 2):
                                strandedRiderCount_checkpoint3 += 1
                            # elif (checkpointIndex == 3):
                            #     strandedRiderCount_checkpoint4 += 1

                            StrandedRiderStatus = 1

                            break

                        elif (present_SoC > leastSoC_before_getting_stranded and present_SoC <= 50):

                            # The rider charged to the nearest charging Station that was in the direction towards his destination

                            # Update frequency of the particular Checkpoint being used
                            if (checkpointIndex == 0):
                                checkpoint1_charging_frequency += 1
                            elif (checkpointIndex == 1):
                                checkpoint2_charging_frequency += 1
                            elif (checkpointIndex == 2):
                                checkpoint3_charging_frequency += 1
                            # elif (checkpointIndex == 3):
                            #     checkpoint4_charging_frequency += 1

                            # At what SoC values are each riders charging?
                            # chargingSoC_list.append(present_SoC)

                            # all_charging_SoC.append(present_SoC)

                            if (present_SoC > 45 and present_SoC <= 50):
                                anxietyLevelFrequency[0] += 1
                                # A1 += 1

                            elif (present_SoC > 40 and present_SoC <= 45):
                                anxietyLevelFrequency[1] += 1
                                # A2 += 1

                            elif (present_SoC > 35 and present_SoC <= 40):
                                anxietyLevelFrequency[2] += 1
                                # A3 += 2

                            elif (present_SoC > 30 and present_SoC <= 35):
                                anxietyLevelFrequency[3] += 1
                                # A4 += 1

                            elif (present_SoC > 25 and present_SoC <= 30):
                                anxietyLevelFrequency[4] += 1

                            elif (present_SoC > 20 and present_SoC <= 25):
                                anxietyLevelFrequency[5] += 1
                                # A5 += 1

                            elif (present_SoC > 15 and present_SoC <= 20):
                                anxietyLevelFrequency[6] += 1
                                # A6 += 1

                            elif (present_SoC > 10 and present_SoC <= 15):
                                anxietyLevelFrequency[7] += 1
                                # A7 += 1

                            elif (present_SoC > 5 and present_SoC <= 10):
                                anxietyLevelFrequency[8] += 1
                                # A8 += 1

                            present_SoC = 100

                            strandedRiderCount = 0
                            # checkpoint_charging_frequency = 0

                    # Rider just travelled 1 km
                    # Increase distance travelled by 1km
                    distance_travelled -= 1

                    # Rider's SoC decreases by 1 %
                    present_SoC -= 1

                ending_SoC_list.append(present_SoC)
                # distance_travelled = 0

    averageEndingSoC = sum(ending_SoC_list) / len(ending_SoC_list)
    # print("Ending SoC Average : ", averageEndingSoC)

    # chargingSoC.update({initial_SoC: chargingSoC_list})
    # total_rider_count += 1
    # print("Anxiety Level Frequency : ")
    # print(anxietyLevelFrequency)

    # print("Average of Anxiety Level Frequency for " + set_of_two + "is :")

    total_number_of_charges = checkpoint1_charging_frequency + checkpoint2_charging_frequency + checkpoint3_charging_frequency

    # print("total_strandedRiderCount :")
    # print(total_strandedRiderCount)

    # print("checkpoint1_charging_frequency :")
    # print(checkpoint1_charging_frequency)

    # print("checkpoint2_charging_frequency :")
    # print(checkpoint2_charging_frequency)

    # print("total_number_of_charges :")
    # print(total_number_of_charges)



    # checkNumberOfCharges = {}

    # checkNumberOfCharges.update({
    #     tuple(set_of_two) : total_number_of_charges
    # })

    # print(checkNumberOfCharges)

    i = 1
    summ = 0
    for _value in anxietyLevelFrequency:
        # print(_value)
        # print(i)
        summ = summ + _value*i
        i += 1

        # print("Anxiety Level Average : ", sum/total_number_of_charges)
        # AnxietyLevelCollection_setOfTwo.append(sum / len(initial_values))

            # result_setofTwo.update({
            #     (sum / len(initial_values)):set_of_two
            # })
            
        # AnxietyLevelCollection_setOfTwo = sorted(AnxietyLevelCollection_setOfTwo)

        # print(AnxietyLevelCollection_setOfTwo)

    # print(sum)
    # print(len(initial_values))
    # print("Average Anxiety Value is ", sum / total_number_of_charges)

    # Anxiety Average dictionary:

        Anxiety_Avg_dict.update({
            tuple(set_of_three) : [(summ / total_number_of_charges), averageEndingSoC]
        })

# print(Anxiety_Avg_dict)

# -------------------------------------------------------------------------------------

# TOP 5 SETS OF THREE WITH LEAST AVERAGE ANXIETY LEVELS

# -------------------------------------------------------------------------------------

data = Anxiety_Avg_dict

# data = {(29, 74): [5.605, 26.125], (30, 74): [5.51, 25.64], (30, 75): [5.415, 25.45], (31, 74): [5.45, 25.4], (31, 75): [5.355, 25.2], (31, 76): [5.31, 25.0], (32, 74): [5.29, 24.55], (32, 75): [5.195, 24.325], (32, 76): [5.15, 24.1], (32, 77): [5.1, 23.875], (33, 74): [5.17, 23.955], (33, 75): [5.075, 23.71], (33, 76): [5.03, 23.465], (33, 77): [4.98, 23.22], (33, 78): [4.975, 22.975], (34, 74): [5.02, 23.2], (34, 75): [4.925, 22.93], (34, 76): [4.88, 22.66], (34, 77): [4.83, 22.39], (34, 78): [4.825, 22.12], (34, 79): [4.75, 21.85], (35, 74): [4.955, 22.885], (35, 75): [4.845, 22.6], (35, 76): [4.8, 22.315], (35, 77): [4.75, 22.03], (35, 78): [4.745, 21.745], (35, 79): [4.67, 21.46], (35, 80): [4.56, 21.175], (36, 74): [4.81, 22.22], (36, 75): [4.7, 21.91], (36, 76): [4.63, 21.6], (36, 77): [4.58, 21.29], (36, 78): [4.575, 20.98], (36, 79): [4.5, 20.67], (36, 80): [4.39, 20.36], (36, 81): [4.32, 20.05], (37, 74): [4.77, 21.975], (37, 75): [4.66, 21.65], (37, 76): [4.59, 21.325], (37, 77): [4.525, 21.0], (37, 78): [4.52, 20.675], (37, 79): [4.445, 20.35], (37, 80): [4.335, 20.025], (37, 81): [4.265, 19.7], (37, 82): [4.2, 19.375], (38, 74): [4.41, 20.14], (38, 75): [4.3, 19.755], (38, 76): [4.23, 19.37], (38, 77): [4.165, 18.985], (38, 78): [4.1, 18.6], (38, 79): [4.025, 18.215], (38, 80): [3.915, 17.83], (38, 81): [3.845, 17.445], (38, 82): [3.78, 17.06], (38, 83): [3.715, 16.675], (39, 74): [4.45, 20.35], (39, 75): [4.34, 19.96], (39, 76): [4.27, 19.57], (39, 77): [4.205, 19.18], (39, 78): [4.14, 18.79], (39, 79): [4.06, 18.4], (39, 80): [3.95, 18.01], (39, 81): [3.88, 17.62], (39, 82): [3.815, 17.23], (39, 83): [3.75, 16.84], (39, 84): [3.67, 16.45], (40, 74): [4.385, 20.06], (40, 75): [4.255, 19.65], (40, 76): [4.185, 19.24], (40, 77): [4.12, 18.83], (40, 78): [4.055, 18.42], (40, 79): [3.975, 18.01], (40, 80): [3.845, 17.6], (40, 81): [3.775, 17.19], (40, 82): [3.71, 16.78], (40, 83): [3.645, 16.37], (40, 84): [3.565, 15.96], (40, 85): [3.435, 15.55], (41, 74): [4.17, 18.985], (41, 75): [4.04, 18.53], (41, 76): [3.925, 18.075], (41, 77): [3.86, 17.62], (41, 78): [3.795, 17.165], (41, 79): [3.715, 16.71], (41, 80): [3.585, 16.255], (41, 81): [3.47, 15.8], (41, 82): [3.405, 15.345], (41, 83): [3.34, 14.89], (41, 84): [3.26, 14.435], (41, 85): [3.13, 13.98], (41, 86): [3.015, 13.525], (42, 74): [4.04, 18.32], (42, 75): [3.91, 17.83], (42, 76): [3.795, 17.34], (42, 77): [3.695, 16.85], (42, 78): [3.63, 16.36], (42, 79): [3.55, 15.87], (42, 80): [3.42, 15.38], (42, 81): [3.305, 14.89], (42, 82): [3.205, 14.4], (42, 83): [3.14, 13.91], (42, 84): [3.06, 13.42], (42, 85): [2.93, 12.93], (42, 86): [2.815, 12.44], (42, 87): [2.715, 11.95], (43, 74): [4.1, 18.5], (43, 75): [3.97, 18.0], (43, 76): [3.855, 17.5], (43, 77): [3.755, 17.0], (43, 78): [3.68, 16.5], (43, 79): [3.6, 16.0], (43, 80): [3.47, 15.5], (43, 81): [3.355, 15.0], (43, 82): [3.255, 14.5], (43, 83): [3.18, 14.0], (43, 84): [3.1, 13.5], (43, 85): [2.97, 13.0], (43, 86): [2.855, 12.5], (43, 87): [2.755, 12.0], (43, 88): [2.68, 11.5], (43, 89): [2.6, 11.0], (44, 74): [4.18, 19.0], (44, 75): [4.05, 18.5], (44, 76): [3.935, 18.0], (44, 77): [3.835, 17.5], (44, 78): [3.76, 17.0], (44, 79): [3.68, 16.5], (44, 80): [3.55, 16.0], (44, 81): [3.435, 15.5], (44, 82): [3.335, 15.0], (44, 83): [3.26, 14.5], (44, 84): [3.18, 14.0], (44, 85): [3.05, 13.5], (44, 86): [2.935, 13.0], (44, 87): [2.835, 12.5], (44, 88): [2.76, 12.0], (44, 89): [2.68, 11.5], (45, 74): [4.255, 19.5], (45, 75): [4.125, 19.0], (45, 76): [4.01, 18.5], (45, 77): [3.91, 18.0], (45, 78): [3.835, 17.5], (45, 79): [3.755, 17.0], (45, 80): [3.625, 16.5], (45, 81): [3.51, 16.0], (45, 82): [3.41, 15.5], (45, 83): [3.335, 15.0], (45, 84): [3.255, 14.5], (45, 85): [3.125, 14.0], (45, 86): [3.01, 13.5], (45, 87): [2.91, 13.0], (45, 88): [2.835, 12.5], (45, 89): [2.755, 12.0], (45, 90): [2.715, 11.95], (46, 74): [4.355, 20.0], (46, 75): [4.225, 19.5], (46, 76): [4.11, 19.0], (46, 77): [4.01, 18.5], (46, 78): [3.935, 18.0], (46, 79): [3.855, 17.5], (46, 80): [3.725, 17.0], (46, 81): [3.61, 16.5], (46, 82): [3.51, 16.0], (46, 83): [3.435, 15.5], (46, 84): [3.355, 15.0], (46, 85): [3.225, 14.5], (46, 86): [3.11, 14.0], (46, 87): [3.01, 13.5], (46, 88): [2.935, 13.0], (46, 89): [2.855, 12.5], (46, 90): [2.815, 12.44], (46, 91): [3.015, 13.525], (47, 74): [4.47, 20.5], (47, 75): [4.34, 20.0], (47, 76): [4.225, 19.5], (47, 77): [4.125, 19.0], (47, 78): [4.05, 18.5], (47, 79): [3.97, 18.0], (47, 80): [3.84, 17.5], (47, 81): [3.725, 17.0], (47, 82): [3.625, 16.5], (47, 83): [3.55, 16.0], (47, 84): [3.47, 15.5], (47, 85): [3.34, 15.0], (47, 86): [3.225, 14.5], (47, 87): [3.125, 14.0], (47, 88): [3.05, 13.5], (47, 89): [2.97, 13.0], (47, 90): [2.93, 12.93], (47, 91): [3.13, 13.98], (47, 92): [3.435, 15.55], (48, 74): [4.6, 21.0], (48, 75): [4.47, 20.5], (48, 76): [4.355, 20.0], (48, 77): [4.255, 19.5], (48, 78): [4.18, 19.0], (48, 79): [4.1, 18.5], (48, 80): [3.97, 18.0], (48, 81): [3.855, 17.5], (48, 82): [3.755, 17.0], (48, 83): [3.68, 16.5], (48, 84): [3.6, 16.0], (48, 85): [3.47, 15.5], (48, 86): [3.355, 15.0], (48, 87): [3.255, 14.5], (48, 88): [3.18, 14.0], (48, 89): [3.1, 13.5], (48, 90): [3.06, 13.42], (48, 91): [3.26, 14.435], (48, 92): [3.565, 15.96], (48, 93): [3.67, 16.45], (49, 74): [4.68, 21.5], (49, 75): [4.55, 21.0], (49, 76): [4.435, 20.5], (49, 77): [4.335, 20.0], (49, 78): [4.26, 19.5], (49, 79): [4.18, 19.0], (49, 80): [4.05, 18.5], (49, 81): [3.935, 18.0], (49, 82): [3.835, 17.5], (49, 83): [3.76, 17.0], (49, 84): [3.68, 16.5], (49, 85): [3.55, 16.0], (49, 86): [3.435, 15.5], (49, 87): [3.335, 15.0], (49, 88): [3.26, 14.5], (49, 89): [3.18, 14.0], (49, 90): [3.14, 13.91], (49, 91): [3.34, 14.89], (49, 92): [3.645, 16.37], (49, 93): [3.75, 16.84], (49, 94): [3.715, 16.675], (50, 75): [4.625, 21.5], (50, 76): [4.51, 21.0], (50, 77): [4.41, 20.5], (50, 78): [4.335, 20.0], (50, 79): [4.255, 19.5], (50, 80): [4.125, 19.0], (50, 81): [4.01, 18.5], (50, 82): [3.91, 18.0], (50, 83): [3.835, 17.5], (50, 84): [3.755, 17.0], (50, 85): [3.625, 16.5], (50, 86): [3.51, 16.0], (50, 87): [3.41, 15.5], (50, 88): [3.335, 15.0], (50, 89): [3.255, 14.5], (50, 90): [3.205, 14.4], (50, 91): [3.405, 15.345], (50, 92): [3.71, 16.78], (50, 93): [3.815, 17.23], (50, 94): [3.78, 17.06], (50, 95): [4.2, 19.375], (51, 76): [4.61, 21.5], (51, 77): [4.51, 21.0], (51, 78): [4.435, 20.5], (51, 79): [4.355, 20.0], (51, 80): [4.225, 19.5], (51, 81): [4.11, 19.0], (51, 82): [4.01, 18.5], (51, 83): [3.935, 18.0], (51, 84): [3.855, 17.5], (51, 85): [3.725, 17.0], (51, 86): [3.61, 16.5], (51, 87): [3.51, 16.0], (51, 88): [3.435, 15.5], (51, 89): [3.355, 15.0], (51, 90): [3.305, 14.89], (51, 91): [3.47, 15.8], (51, 92): [3.775, 17.19], (51, 93): [3.88, 17.62], (51, 94): [3.845, 17.445], (51, 95): [4.265, 19.7], (51, 96): [4.32, 20.05], (52, 77): [4.625, 21.5], (52, 78): [4.55, 21.0], (52, 79): [4.47, 20.5], (52, 80): [4.34, 20.0], (52, 81): [4.225, 19.5], (52, 82): [4.125, 19.0], (52, 83): [4.05, 18.5], (52, 84): [3.97, 18.0], (52, 85): [3.84, 17.5], (52, 86): [3.725, 17.0], (52, 87): [3.625, 16.5], (52, 88): [3.55, 16.0], (52, 89): [3.47, 15.5], (52, 90): [3.42, 15.38], (52, 91): [3.585, 16.255], (52, 92): [3.845, 17.6], (52, 93): [3.95, 18.01], (52, 94): [3.915, 17.83], (52, 95): [4.335, 20.025], (52, 96): [4.39, 20.36], (52, 97): [4.56, 21.175], (53, 78): [4.68, 21.5], (53, 79): [4.6, 21.0], (53, 80): [4.47, 20.5], (53, 81): [4.355, 20.0], (53, 82): [4.255, 19.5], (53, 83): [4.18, 19.0], (53, 84): [4.1, 18.5], (53, 85): [3.97, 18.0], (53, 86): [3.855, 17.5], (53, 87): [3.755, 17.0], (53, 88): [3.68, 16.5], (53, 89): [3.6, 16.0], (53, 90): [3.55, 15.87], (53, 91): [3.715, 16.71], (53, 92): [3.975, 18.01], (53, 93): [4.06, 18.4], (53, 94): [4.025, 18.215], (53, 95): [4.445, 20.35], (53, 96): [4.5, 20.67], (53, 97): [4.67, 21.46], (53, 98): [4.75, 21.85], (54, 79): [4.68, 21.5], (54, 80): [4.55, 21.0], (54, 81): [4.435, 20.5], (54, 82): [4.335, 20.0], (54, 83): [4.26, 19.5], (54, 84): [4.18, 19.0], (54, 85): [4.05, 18.5], (54, 86): [3.935, 18.0], (54, 87): [3.835, 17.5], (54, 88): [3.76, 17.0], (54, 89): [3.68, 16.5], (54, 90): [3.63, 16.36], (54, 91): [3.795, 17.165], (54, 92): [4.055, 18.42], (54, 93): [4.14, 18.79], (54, 94): [4.1, 18.6], (54, 95): [4.52, 20.675], (54, 96): [4.575, 20.98], (54, 97): [4.745, 21.745], (54, 98): [4.825, 22.12], (54, 99): [4.975, 22.975], (55, 80): [4.625, 21.5], (55, 81): [4.51, 21.0], (55, 82): [4.41, 20.5], (55, 83): [4.335, 20.0], (55, 84): [4.255, 19.5], (55, 85): [4.125, 19.0], (55, 86): [4.01, 18.5], (55, 87): [3.91, 18.0], (55, 88): [3.835, 17.5], (55, 89): [3.755, 17.0], (55, 90): [3.695, 16.85], (55, 91): [3.86, 17.62], (55, 92): [4.12, 18.83], (55, 93): [4.205, 19.18], (55, 94): [4.165, 18.985], (55, 95): [4.525, 21.0], (55, 96): [4.58, 21.29], (55, 97): [4.75, 22.03], (55, 98): [4.83, 22.39], (55, 99): [4.98, 23.22], (55, 100): [5.1, 23.875], (56, 81): [4.61, 21.5], (56, 82): [4.51, 21.0], (56, 83): [4.435, 20.5], (56, 84): [4.355, 20.0], (56, 85): [4.225, 19.5], (56, 86): [4.11, 19.0], (56, 87): [4.01, 18.5], (56, 88): [3.935, 18.0], (56, 89): [3.855, 17.5], (56, 90): [3.795, 17.34], (56, 91): [3.925, 18.075], (56, 92): [4.185, 19.24], (56, 93): [4.27, 19.57], (56, 94): [4.23, 19.37], (56, 95): [4.59, 21.325], (56, 96): [4.63, 21.6], (56, 97): [4.8, 22.315], (56, 98): [4.88, 22.66], (56, 99): [5.03, 23.465], (56, 100): [5.15, 24.1], (56, 101): [5.31, 25.0], (57, 82): [4.625, 21.5], (57, 83): [4.55, 21.0], (57, 84): [4.47, 20.5], (57, 85): [4.34, 20.0], (57, 86): [4.225, 19.5], (57, 87): [4.125, 19.0], (57, 88): [4.05, 18.5], (57, 89): [3.97, 18.0], (57, 90): [3.91, 17.83], (57, 91): [4.04, 18.53], (57, 92): [4.255, 19.65], (57, 93): [4.34, 19.96], (57, 94): [4.3, 19.755], (57, 95): [4.66, 21.65], (57, 96): [4.7, 21.91], (57, 97): [4.845, 22.6], (57, 98): [4.925, 22.93], (57, 99): [5.075, 23.71], (57, 100): [5.195, 24.325], (57, 101): [5.355, 25.2], (57, 102): [5.415, 25.45], (58, 83): [4.68, 21.5], (58, 84): [4.6, 21.0], (58, 85): [4.47, 20.5], (58, 86): [4.355, 20.0], (58, 87): [4.255, 19.5], (58, 88): [4.18, 19.0], (58, 89): [4.1, 18.5], (58, 90): [4.04, 18.32], (58, 91): [4.17, 18.985], (58, 92): [4.385, 20.06], (58, 93): [4.45, 20.35], (58, 94): [4.41, 20.14], (58, 95): [4.77, 21.975], (58, 96): [4.81, 22.22], (58, 97): [4.955, 22.885], (58, 98): [5.02, 23.2], (58, 99): [5.17, 23.955], (58, 100): [5.29, 24.55], (58, 101): [5.45, 25.4], (58, 102): [5.51, 25.64], (58, 103): [5.605, 26.125]}

anxLevelList = []
sortedDict = {}


for i in range(10):
    minAnxTemp = 100
    for key, val in data.items():
        if val[0] < minAnxTemp:
            minAnxTemp = val[0]
            minKey = key
            minVal = val
    del data[(minKey)]
    sortedDict.update({minKey: minVal})



print("Sorted: ")

print(sortedDict)



