from definitions import *
from Calculations import *

# -------------------------------------------------------------------------------------
# PRINT POINTS OF RECHARGE WHEN 100 RIDERS RIDE FROM A->B AND THEN B->A
# -------------------------------------------------------------------------------------
result = Calculate_Points_Of_Recharge()


# -------------------------------------------------------------------------------------
# GENERIC LOGIC TO FILTER STATIONS TO LOCATE BETWEEN 50 - 100
# -------------------------------------------------------------------------------------
list_with_verified_distances = Generate_Verified_Combinations(50, 100)
print(list_with_verified_distances)


# -------------------------------------------------------------------------------------
# FILTER OUT STRANDED RIDERS FROM THE VERIFIED SET
# -------------------------------------------------------------------------------------

# Dataset of topography
# [[elevation0, distance0],[elevation1, distance1],[elevation2, distance2]...]
topography_dataset_distance = [0,12.5,100,112.5,177]            # km
topography_dataset_elevation = [1302,1932,514,1234,309]         # meters

topography_dataset_distance = [round(distance) for distance in topography_dataset_distance]

# Create a list of lists where each sublist corresponds to the elements at the same index
topography_dataset = [[distance, elevation] for distance, elevation in zip(topography_dataset_distance, topography_dataset_elevation)]
print("TOPOGRAPHY DATASET           : ", topography_dataset)
print("-------------------------------------------------------------------\n")
print("-------------------------------------------------------------------")
print("*******************************************************************")

# -----------------------------------
# Simulation Constants
# -----------------------------------
if (simulation_status == 1):
    # initial_SoC = 60
    # station = [20, 101]
    station_list = [[20, 101], [21, 101]]
# -----------------------------------
# # for every pair of Charging Station
# for station in list_with_verified_distances:
for station in station_list:

    print("\n")
    print("----------------------------------------------------------------------------------------------------------------------")
    print(initial_values)

    ending_soc_cumulation   = 0
    anxietyLevelFrequency   = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    charge_count            = 0
    stranded_rider_count    = 0
    unhandled_cases         = 0


    # for every random SoC
    for initial_SoC in initial_values[0]:

        print("*****************")
        print("INITIAL SOC : ", initial_SoC)
        present_SoC = initial_SoC
        total_distance_travelled = 0
        stranded_rider_breakout_flag = 0


        # for every section of the topography
        for i in range(len(topography_dataset) - 1):

            distance_travelled_in_each_section = 0

            # print("-------------------------------------------------------------------")
            # print("Section's Starting Point(km) and Elevation(m)   : ", topography_dataset[i][0], topography_dataset[i][1])
            # print("Section's Ending Point(km) and Elevation(m)     : ", topography_dataset[i+1][0], topography_dataset[i+1][1])
            # print("-------------------------------------------------------------------")

            # Identify if elevation profile is uphill or downhill
            if (topography_dataset[i][1] < topography_dataset[i+1][1]):
                section_elevation_profile = UPHILL
                SoC_degradation_factor = uphill_degradation_factor

            elif (topography_dataset[i][1] > topography_dataset[i+1][1]):
                section_elevation_profile = DOWNHILL
                SoC_degradation_factor = downhill_degradation_factor

            elif (topography_dataset[i][1] == topography_dataset[i+1][1]):
                section_elevation_profile = PLAIN
                SoC_degradation_factor = plain_terrain_degradation_factor

            # Distance of the route section
            section_distance = topography_dataset[i+1][0] - topography_dataset[i][0]
            # print("Section_distance             : ", section_distance)
            # print("Elevation difference         : ", topography_dataset[i+1][1] - topography_dataset[i][1])
            # print("SoC_degradation_factor       : ", SoC_degradation_factor, "UPHILL" if(SoC_degradation_factor == uphill_degradation_factor) else "DOWNHILL" if(SoC_degradation_factor == downhill_degradation_factor) else "PLAIN")
            # print("-------------------------------------------------------------------")

            # When the rider hasn't reached the section_destination
            while (distance_travelled_in_each_section < section_distance):

                if ((total_distance_travelled in station) and (present_SoC <= threshold_SoC_where_charging_starts) and (present_SoC >= stranded_threshold_SoC)):

                    # Vehicle charged to 100%
                    print("-------------------------")
                    print(f"<< Recharged at distance {total_distance_travelled} km with SoC {present_SoC}!! >>")
                    print("-------------------------")

                    # Calculate Anxiety Level
                    print(present_SoC)
                    anxietyLevelFrequency = Calculate_Anxiety_Level(present_SoC)
                    
                    present_SoC = 100
                    charge_count += 1
                
                elif (present_SoC < stranded_threshold_SoC):

                    # User is stranded here
                    stranded_rider_count += 1
                    # print("-------------------------")
                    # print(f"<< User stranded at distance {total_distance_travelled} km with SoC {present_SoC}!! >>")
                    # print("-------------------------")

                    stranded_rider_breakout_flag = 1
                    break

                else:
                    unhandled_cases += 1

                present_SoC += SoC_degradation_factor

                distance_travelled_in_each_section += 1
                total_distance_travelled += 1

                # print("---------------")
                # print("AT SOC                   : ", present_SoC)
                # print("TOTAL DISTANCE           : ", total_distance_travelled)
                # print("DISTANCE IN THE SECTION  : ", distance_travelled_in_each_section)
            if (stranded_rider_breakout_flag):
                break
                
            # present_SoC at every end of the section
            # print("Ending SoC at the end of the section : ", present_SoC)

        # ending_SoC at the end of one way trip
        if (stranded_rider_breakout_flag == 0):
            ending_soc_cumulation += present_SoC

        print("Final ending SoC at the end of the whole trip : ", present_SoC)
        print("Anxiety levels in a list : ", anxietyLevelFrequency)
        print("CHARGE COUNT             : ", charge_count)
        print("STRANDED RIDER COUNT     : ", stranded_rider_count)
        print("*****************")
        print("\n")

    i = 1
    summ = 0
    for _value in anxietyLevelFrequency:
        summ = summ + _value * i
        i += 1


    if (charge_count != 0):

        average_anxiety_level = summ / charge_count
        average_ending_soc = ending_soc_cumulation / charge_count

        print("CHARGE COUNT             : ", charge_count)
        print("STRANDED RIDER COUNT     : ", stranded_rider_count)
        # print("UNHANDLED CASES          : ", unhandled_cases)
        # print("TOTAL CASES              : ", charge_count + stranded_rider_count + unhandled_cases)
        print("Average Anxiety Level    : ", average_anxiety_level)
        print("Average Ending SoC       : ", average_ending_soc)

        # Anxiety Average dictionary:
        Anxiety_Avg_dict.update({
            tuple(station) : [average_anxiety_level, average_ending_soc]
        })

    else:
        print("Average Anxiety Level    : ALL USERS STRANDED")

    # anxietyLevelFrequency   = [0, 0, 0, 0, 0, 0, 0, 0, 0]





    print(Anxiety_Avg_dict)



    #             if (present_SoC > leastSoC_before_getting_stranded and present_SoC <= distance_where_charging_starts):
                    
    #                 for i in range(number_of_charging_stations):
    #                     if (checkpointIndex == i):
    #                         checkpointBased_Charging_Number_Count[i] += 1

    #                 if (present_SoC > 45 and present_SoC <= 50):
    #                     anxietyLevelFrequency[0] += 1

    #                 elif (present_SoC > 40 and present_SoC <= 45):
    #                     anxietyLevelFrequency[1] += 1

    #                 elif (present_SoC > 35 and present_SoC <= 40):
    #                     anxietyLevelFrequency[2] += 1

    #                 elif (present_SoC > 30 and present_SoC <= 35):
    #                     anxietyLevelFrequency[3] += 1

    #                 elif (present_SoC > 25 and present_SoC <= 30):
    #                     anxietyLevelFrequency[4] += 1

    #                 elif (present_SoC > 20 and present_SoC <= 25):
    #                     anxietyLevelFrequency[5] += 1

    #                 elif (present_SoC > 15 and present_SoC <= 20):
    #                     anxietyLevelFrequency[6] += 1

    #                 elif (present_SoC > 10 and present_SoC <= 15):
    #                     anxietyLevelFrequency[7] += 1

    #                 elif (present_SoC > 5 and present_SoC <= 10):
    #                     anxietyLevelFrequency[8] += 1

    #                 present_SoC = full_charge_value

    #             elif (present_SoC <= leastSoC_before_getting_stranded):                        

    #                 total_strandedRiderCount += 1

    #                 for i in range(number_of_charging_stations):

    #                     if (checkpointIndex == i):
    #                         checkpointBased_strandedRiderCount[i] += 1

    #                 discard_set = 1
    #                 break
            
    #         distance_travelled += 1
    #         present_SoC -= 1 

    #     if (discard_set == 1):
    #         break
    #     ending_SoC_list.append(present_SoC)










# for elevation_variation_distance, topography_dataset_elevation in topography_dataset:
#     print(elevation_variation_distance, topography_dataset_elevation)
    

# # # -------------------------------------------------------------------------------------

# # # FILTER OUT STRANDED RIDERS FROM THE VERIFIED SET

# # # -------------------------------------------------------------------------------------

# result_setofThree = {}
# Anxiety_Avg_dict = {}
# counter = 0
# # list_with_verified_distances = [[25, 6, 114, 158]]
# # 25	64	114	158
# for _set_of_three in list_with_verified_distances:

#     discarded_list_count = 0
#     anxietyLevelFrequency = [0, 0, 0, 0, 0, 0, 0, 0, 0]
#     total_strandedRiderCount = 0
#     ending_SoC_list = []
#     total_number_of_charges = 0
#     discard_set = 0
#     checkpointBased_Charging_Number_Count = []

#     for i in range(number_of_charging_stations):
#         checkpointBased_Charging_Number_Count.append(0)

#     checkpointBased_strandedRiderCount = []

#     for i in range(number_of_charging_stations):
#         checkpointBased_strandedRiderCount.append(0)

#     chargingStationCheckpoints = _set_of_three

#     counter = 0

#     for initial_SoC in initial_values:

#         distance_travelled = 0
#         counter += 1

#         for trip_number in total_number_of_trips:

#             if(trip_number % 2 == 0):

#                 present_SoC = initial_SoC

#                 # When the rider hasn't reached the destination
#                 while (distance_travelled < total_distance_in_one_trip):

#                     if (distance_travelled in chargingStationCheckpoints):

#                         checkpointIndex = chargingStationCheckpoints.index(distance_travelled)

#                         if (present_SoC > leastSoC_before_getting_stranded and present_SoC <= distance_where_charging_starts):
                            
#                             for i in range(number_of_charging_stations):
#                                 if (checkpointIndex == i):
#                                     checkpointBased_Charging_Number_Count[i] += 1

#                             if (present_SoC > 45 and present_SoC <= 50):
#                                 anxietyLevelFrequency[0] += 1

#                             elif (present_SoC > 40 and present_SoC <= 45):
#                                 anxietyLevelFrequency[1] += 1

#                             elif (present_SoC > 35 and present_SoC <= 40):
#                                 anxietyLevelFrequency[2] += 1

#                             elif (present_SoC > 30 and present_SoC <= 35):
#                                 anxietyLevelFrequency[3] += 1

#                             elif (present_SoC > 25 and present_SoC <= 30):
#                                 anxietyLevelFrequency[4] += 1

#                             elif (present_SoC > 20 and present_SoC <= 25):
#                                 anxietyLevelFrequency[5] += 1

#                             elif (present_SoC > 15 and present_SoC <= 20):
#                                 anxietyLevelFrequency[6] += 1

#                             elif (present_SoC > 10 and present_SoC <= 15):
#                                 anxietyLevelFrequency[7] += 1

#                             elif (present_SoC > 5 and present_SoC <= 10):
#                                 anxietyLevelFrequency[8] += 1

#                             present_SoC = full_charge_value

#                         elif (present_SoC <= leastSoC_before_getting_stranded):                        

#                             total_strandedRiderCount += 1

#                             for i in range(number_of_charging_stations):

#                                 if (checkpointIndex == i):
#                                     checkpointBased_strandedRiderCount[i] += 1

#                             discard_set = 1
#                             break
                    
#                     distance_travelled += 1
#                     present_SoC -= 1 

#                 if (discard_set == 1):
#                     break
#                 ending_SoC_list.append(present_SoC)

#             elif(trip_number % 2 == 1):

#                 present_SoC = initial_SoC
#                 distance_travelled = total_distance_in_one_trip

#                 # When the rider hasn't reached the destination
#                 while (distance_travelled <= total_distance_in_one_trip and distance_travelled > 0):

#                     if (distance_travelled in chargingStationCheckpoints):

#                         checkpointIndex = chargingStationCheckpoints.index(distance_travelled)

#                         if (present_SoC > leastSoC_before_getting_stranded and present_SoC <= 50):

#                             for i in range(number_of_charging_stations):
#                                 if (checkpointIndex == i):
#                                     checkpointBased_Charging_Number_Count[i] += 1

#                             if (present_SoC > 45 and present_SoC <= 50):
#                                 anxietyLevelFrequency[0] += 1

#                             elif (present_SoC > 40 and present_SoC <= 45):
#                                 anxietyLevelFrequency[1] += 1

#                             elif (present_SoC > 35 and present_SoC <= 40):
#                                 anxietyLevelFrequency[2] += 1

#                             elif (present_SoC > 30 and present_SoC <= 35):
#                                 anxietyLevelFrequency[3] += 1

#                             elif (present_SoC > 25 and present_SoC <= 30):
#                                 anxietyLevelFrequency[4] += 1

#                             elif (present_SoC > 20 and present_SoC <= 25):
#                                 anxietyLevelFrequency[5] += 1

#                             elif (present_SoC > 15 and present_SoC <= 20):
#                                 anxietyLevelFrequency[6] += 1

#                             elif (present_SoC > 10 and present_SoC <= 15):
#                                 anxietyLevelFrequency[7] += 1

#                             elif (present_SoC > 5 and present_SoC <= 10):
#                                 anxietyLevelFrequency[8] += 1

#                             present_SoC = full_charge_value

#                         elif (present_SoC <= leastSoC_before_getting_stranded):                        

#                             total_strandedRiderCount += 1

#                             for i in range(number_of_charging_stations):
#                                 if (checkpointIndex == i):
#                                     checkpointBased_strandedRiderCount[i] += 1

#                             break
                    
#                     distance_travelled -= 1
#                     present_SoC -= 1
                
#                 ending_SoC_list.append(present_SoC)


#         if (discard_set == 1):
#             break

#     for i in range(number_of_charging_stations):
#         total_number_of_charges = total_number_of_charges + checkpointBased_Charging_Number_Count[i]
    
#     for i in range(number_of_charging_stations):
#         if (checkpointBased_Charging_Number_Count[i] == 0):
#             discarded_list_count += 1
           
#     # if (total_strandedRiderCount == 0 and discarded_list_count == 0):
#     if (discarded_list_count == 0):

#         averageEndingSoC = sum(ending_SoC_list) / len(ending_SoC_list)

#         i = 1
#         summ = 0
#         for _value in anxietyLevelFrequency:
#             summ = summ + _value*i
#             i += 1

#             # Anxiety Average dictionary:
#             Anxiety_Avg_dict.update({
#                 tuple(_set_of_three) : [(summ / total_number_of_charges), averageEndingSoC]
#             })

# print("List before filtration : ", len(list_with_verified_distances))
# print("List after filtration  : ", len(Anxiety_Avg_dict))
# # print("List after filtration : ", (Anxiety_Avg_dict))


# # # # -------------------------------------------------------------------------------------

# # # # TOP 10 SETS OF THREE WITH LEAST AVERAGE ANXIETY LEVELS

# # # # -------------------------------------------------------------------------------------
# print("AnxietyLevelFrequency ", anxietyLevelFrequency)

# data = Anxiety_Avg_dict

# anxLevelList = []
# sortedDict = {}
# minKey = 0

# for i in range(10):
#     minAnxTemp = 200
#     for key, val in data.items():
#         # print(key,val)
#         if val[0] < minAnxTemp:
#             minAnxTemp = val[0]
#             minKey = key
#             minVal = val
#     del data[(minKey)]
#     minVal[0] = round(minVal[0], 2)
#     minVal[1] = round(minVal[1], 2)
#     sortedDict.update({minKey: minVal})

# print("Sorted Top 10: ")
# print(sortedDict)



# overall_data = []

# for value1, value2 in sortedDict.items():

#     current_temp_list = []

#     for i in range(len(value1)):
#         print(value1[i])
#         current_temp_list.append(value1[i])
    
#     current_temp_list.append(value2[0])
#     current_temp_list.append(value2[1])

#     overall_data.append(current_temp_list)

# print(overall_data)


# # open the file in the write mode
# f = open('ChargingStation_csv/test_output.csv', 'w')

# # create the csv writer
# writer = csv.writer(f)

# # write a row to the csv file
# writer.writerows(overall_data)

# # close the file
# f.close()

# print("\n")    

# print(overall_data)


                # checkpointIndex = station.index(distance_travelled)

