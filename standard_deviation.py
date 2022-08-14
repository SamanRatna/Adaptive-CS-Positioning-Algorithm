
# Libraries
import pandas as pd
import statistics
import csv

# Constant parameters
num_of_bikes = 100                                          # Total number of Bikes
total_distance_in_one_trip = 132                            # distance in kms
SoC_logging_distance = 1                                    # distance in kms
full_charge_SoC = 100                                        # Upto what SoC to charge?
total_number_of_trips = range(2)                            # 1: A->B, 2: A->B->A, 3: A->B->A->B
charging_station_location = [43, 89]
# charging_station_location = [27, 52, 77, 102]
# charging_station_location = [25, 50, 84]
# charging_station_location = [33, 58, 87]
# charging_station_location = [25, 50, 84]
# charging_station_location = [46, 96, 125]

# Which Data will I be using from Spreadsheet?
data_collection = ["random data 1", "Random Data 2", "Random Data 3", "Random Data 4", "Random Data 5", "Random Data 6", "Random Data 7", "Random Data 8", "Random Data 9", "Random Data 10", "5% change A", "5% change B", "5% change C"]
# data_collection = ["random data 1"]

overall_data = []
# for i in range(len(data_collection))
#     overall_data.append([])

for collection in data_collection:

    dataColumn = collection
    ending_SoC_list = []

    # Number of times Bike travels from A to B and viceversa
    present_SoC = 0
    distance_travelled = 0

    # SoC data input for the system
    # df = pd.read_excel(r'data_collection.xlsx')
    df = pd.read_excel(r'data_collection2.xlsx')
    initial_values = []

    print("Data Column Used:                            ", dataColumn)
    for count in range(len(df[dataColumn])):
        initial_values.append(df[dataColumn][count])

    # -------------------------------------------------------------------------------------

    # Average Ending SoC at each Charging Station of set (33, 58, 87)

    # -------------------------------------------------------------------------------------

    our_current_station = charging_station_location
    station = []
    for i in range(len(our_current_station)):
        station.append([])

    for initial_SoC in initial_values:

        distance_travelled = 0

        for trip_number in total_number_of_trips:

            if(trip_number % 2 == 0):
                
                present_SoC = initial_SoC

                while (distance_travelled < total_distance_in_one_trip):

                    if (present_SoC <= 50):

                        for i in range(len(charging_station_location)):

                            if (distance_travelled == our_current_station[i]):
                                station[i].append(present_SoC)
                                present_SoC = full_charge_SoC

                    distance_travelled += 1
                    present_SoC -= 1

                ending_SoC_list.append(present_SoC)

            elif(trip_number % 2 == 1):
                
                present_SoC = initial_SoC

                while (distance_travelled <= total_distance_in_one_trip and distance_travelled > 0):

                    if (present_SoC <= 50):

                        for i in range(len(charging_station_location)):

                            if (distance_travelled == our_current_station[i]):
                                station[i].append(present_SoC)
                                present_SoC = full_charge_SoC

                    distance_travelled -= 1
                    present_SoC -= 1

                ending_SoC_list.append(present_SoC)

    print("Users charging upto ", full_charge_SoC, "%")

    current_temp_data = []
    current_temp_data.append(dataColumn)

    for i in range(len(charging_station_location)):
        print("Number of users in Station ", i + 1, ": ", len(station[i]))
        current_temp_data.append(len(station[i]))

    for i in range(len(charging_station_location)):
        print("Standard Deviation of Station ", i + 1, ": ", round(statistics.stdev(station[i]), 2))
        current_temp_data.append(round(statistics.stdev(station[i]), 2))

    for i in range(len(charging_station_location)):
        print("Avg Ending SoC in Station ", i + 1, ": ", round(sum(station[i])/len(station[i]), 2))
        current_temp_data.append(round(sum(station[i])/len(station[i]), 2))

    print("Ending SoC Average : ", round(sum(ending_SoC_list)/len(ending_SoC_list), 2))
    current_temp_data.append(round(sum(ending_SoC_list)/len(ending_SoC_list), 2))

    overall_data.append(current_temp_data)

# open the file in the write mode
f = open('generated_csv/soc80_132_2CS.csv', 'w')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
writer.writerows(overall_data)

# close the file
f.close()

print("\n")    

print(overall_data)
