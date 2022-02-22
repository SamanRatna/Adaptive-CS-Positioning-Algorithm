# ------------------------------------------ CONSIDERATIONS ------------------------------------------
# SoC changes at the rate of 1% per unit km
# ----------------------------------------------------------------------------------------------------

# Libraries
import collections
import pandas as pd
import matplotlib.pyplot as plt

# Constant parameters
num_of_bikes = 100                      # Total number of Bikes
total_distance_in_one_trip = 132        # distance in kms
SoC_logging_distance = 1                # distance in kms
total_number_of_trips = range(100)      # Number of times Bike travels from A to B and viceversa
present_SoC = 0
distance_travelled = 0                  # Distance travelled by that instant in the present trip
counter = 0
result = {}

# SoC data input for the system
df = pd.read_excel(r'.\data_collection.xlsx')
initial_values = []

for count in range(len(df['Normal'])):
    initial_values.append(df['Normal'][count])
print("--------------------------- INITIAL SoC ----------------------------")
print(initial_values)

# Output Variable define
points_of_recharge = []

# Beginv Logic
for initial_SoC in initial_values:
    present_SoC = initial_SoC
    for trip_number in total_number_of_trips:
        if( trip_number % 2 == 0):
            while (distance_travelled < total_distance_in_one_trip):
                if (present_SoC <= 80):
                    points_of_recharge.append(distance_travelled)
                    present_SoC = 100                           # Bike recharged to full when reached to 50%
                else:
                    present_SoC -= 1                            # Bike SoC decreases with increase in travel displacement by 1km
                distance_travelled += 1                         # Increase distance travelled by 1km

        elif ( trip_number % 2 == 1):

            while (distance_travelled <= total_distance_in_one_trip and distance_travelled > 0):
                if (present_SoC <= 80):
                    points_of_recharge.append(distance_travelled)
                    present_SoC = 100                           # Bike recharged to full when reached to 50%
                else:
                    present_SoC -= 1                            # Bike SoC decreases with increase in travel displacement by 1km
                distance_travelled -= 1                         # Increase distance travelled by 1km

# Arrange Dictionary keys in ascending order
def ascendingKeys(frequency_of_occurence):
    for i in sorted (frequency_of_occurence):
        result.update({
            i: frequency_of_occurence[i]
        })
    print("\n")
    print('---------------------- SORTED DICTIONARY : KEY as DISTANCE, VALUE as FREQUENCY -----------------------------')
    print(result)

ctr = collections.Counter(points_of_recharge)
frequency = dict(ctr)
ascendingKeys(frequency)

Distance_x_axis = list(result.keys())
Frequency_y_axis = list(result.values())

print("\n")

plt.plot(Distance_x_axis, Frequency_y_axis)
plt.xlabel('Distance')
plt.ylabel('Frequency')
plt.show()