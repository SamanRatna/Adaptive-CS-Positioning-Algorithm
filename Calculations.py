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

    # Initialize an empty nested list
    initial_values = [[] for _ in range(len(topography_dataset_distance))]

    print("Data Column Used             : ", dataColumn)
    for count in range(len(df[dataColumn])):
        initial_values[0].append(df[dataColumn][count])

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
