from definitions import *
# from ChargingStation import *


def Calculate_Points_Of_Recharge():

    # Which Data will I be using from Spreadsheet?
    dataColumn = "Random1"
    # dataColumn = "random data 1"
    # dataColumn = "5% change C"

    # SoC data input for the system
    df = pd.read_excel(r'data_collection2.xlsx')
    # initial_values = []


    print("Data Column Used             : ", dataColumn)
    for count in range(len(df[dataColumn])):
        initial_values[0].append(df[dataColumn][count])
    
    print(initial_values[0])

    # # Output Variable define
    points_of_recharge = []

    for initial_SoC in initial_values[0]:

        distance_travelled = 0

        for trip_number in total_number_of_trips:

            if(trip_number % 2 == 0):

                present_SoC = initial_SoC

                while (distance_travelled < total_distance_in_one_trip):

                    if (present_SoC <= distance_where_charging_starts):

                        points_of_recharge.append(distance_travelled)

                        # Bike recharged to full when reached to 50%
                        present_SoC = full_charge_value
                    
                    else:

                        # Bike SoC decreases with increase in travel displacement by 1km
                        present_SoC -= 1
    
                    # Increase distance travelled by 1km
                    distance_travelled += 1

            elif (trip_number % 2 == 1):

                present_SoC = initial_SoC

                while (distance_travelled <= total_distance_in_one_trip and distance_travelled > 0):

                    if (present_SoC <= distance_where_charging_starts):

                        points_of_recharge.append(distance_travelled)

                        # Bike recharged to full when reached to 50%
                        present_SoC = full_charge_value                           
                    
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

    ctr = collections.Counter(points_of_recharge)
    frequency = dict(ctr)
    ascendingKeys(frequency)

    return result

    # print("\n")
    # print("Points of Recharge")
    # print(Distance_x_axis)
    # print("TOTAL POINTS OF RECHARGE     : ", len(Distance_x_axis))


def Generate_Verified_Combinations(min_distance, max_distance):

    # least_number_of_charging_stations = math.floor(total_distance_in_one_trip/80)
    # most_number_of_charging_stations = math.ceil(total_distance_in_one_trip/25)

    Distance_x_axis = list(result.keys())
    all_possible_combinations = itertools.combinations(Distance_x_axis, number_of_charging_stations)
    list_with_verified_distances = []
    counter_exception = 0
    combination_count = 0

    for every_combination in all_possible_combinations:

        combination_count += 1
        last_checkpoint = 0
        validity_counter = 0

        for station_position in range(number_of_charging_stations+1):

            if (station_position == number_of_charging_stations):

                # When accounting for distance between last charging station and total distance in a trip
                if ((total_distance_in_one_trip - every_combination[station_position - 1] >= min_distance) and (total_distance_in_one_trip - every_combination[station_position - 1] <= max_distance)):

                    validity_counter += 1
                    last_checkpoint = total_distance_in_one_trip
                
                else:
                    last_checkpoint = 0
                    break
                
            elif ((every_combination[station_position] - last_checkpoint >= min_distance) and (every_combination[station_position] - last_checkpoint <= max_distance)):

                validity_counter += 1
                last_checkpoint = every_combination[station_position]
            
            else:
                last_checkpoint = 0
                counter_exception += 1
                break

        if (validity_counter == number_of_charging_stations + 1):
            list_with_verified_distances.append(every_combination)

    print("-------------------------------------------------------------------")
    print("VERIFIED COMBINATIONS OF SETS OF STATION LOCATIONS")
    print(list_with_verified_distances)
    print("-------------------------------------------------------------------")

    print("NUMBER OF TOTAL COMBINATIONS : ", combination_count)
    print("NUMBER OF VERIFIED DISTANCES : ", len(list_with_verified_distances))


def Calculate_Anxiety_Level(present_SoC):

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

    elif (present_SoC >= 5 and present_SoC <= 10):
        anxietyLevelFrequency[8] += 1

