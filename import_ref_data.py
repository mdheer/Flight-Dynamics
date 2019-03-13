import numpy as np
import scipy.io as sio

""" =============== PART I: MATLAB DATA =============== """

# Importing matlab file
matlab_data = sio.loadmat('matlab.mat')

# Getting relevant data from matlab file
flight_data = matlab_data['flightdata']

def print_pars_w_index():
    
    """ Function to print each parameter with its 
        corresponding units and index number.      """
    
    for i in range(len(flight_data[0][0])):
        
        if i==13 or i==14 or i==47:
            print(i+1)
            print(flight_data[0][0][i][0][0][2][0])
            print(flight_data[0][0][i][0][0][1][0])
            print()
            
        elif 42<i<47:
            print(i+1)
            print(flight_data[0][0][i][0][0][2][0][0][0])
            print()
        
        else:
            print(i+1)
            print(flight_data[0][0][i][0][0][2][0][0][0])
            print(flight_data[0][0][i][0][0][1][0][0][0])
            print()

# Putting data into handy matrix
ref_data = np.zeros((49,3),dtype='object')

# Titles for ref_data
ref_data[0][0] = 'Name'
ref_data[0][1] = 'Units'
ref_data[0][2] = 'Data'

# Loop to fill ref_data matrix
for i in range(len(flight_data[0][0])):
        
    if i==13 or i==14 or i==47:
        ref_data[i+1][0] = flight_data[0][0][i][0][0][2][0]   # name
        ref_data[i+1][1] = flight_data[0][0][i][0][0][1][0]   #unit
        ref_data[i+1][2] = flight_data[0][0][i][0][0][0]      #data
        
    elif 42<i<47:
        ref_data[i+1][0] = flight_data[0][0][i][0][0][2][0][0][0]   # name
        ref_data[i+1][1] = 'no unit'                                #unit
        ref_data[i+1][2] = flight_data[0][0][i][0][0][0]            #data

    else:
        ref_data[i+1][0] = flight_data[0][0][i][0][0][2][0][0][0]   # name
        ref_data[i+1][1] = flight_data[0][0][i][0][0][1][0][0][0]   #unit
        ref_data[i+1][2] = flight_data[0][0][i][0][0][0]            #data

# Calling a certain line from the ref_data to get its values in an array
def get_data(i):
    print('Parameter =',ref_data[i][0])
    return ref_data[i][2]

# Printing intructions when running
print()
print("\033[1;31;43mINSTRUCTIONS MATLAB:")
print('1. Type "print_pars_w_index()" to get indices of each parameter for next function.')
print('2. Type get_data(i) with desired i from the given indices to get the data of the chosen parameter in an array.')
print('NOTE: must have matlab.mat file in same folder.')
print('NOTE2: matlab units have not been converted to SI units as yet.')



""" =============== PART II: EXCEL DATA =============== """

# Importing excel data from excel file
# NOTE: Please save file as .csv instead of .xlsx
# IMPORTANT: must have Numpy version 1.15+
filename = 'REFERENCE_Post_Flight_Datasheet_Flight.csv'
excel_data = np.genfromtxt(filename,delimiter=',',dtype='str')


# ======= A) Getting weights =======
weights = np.zeros((2,1),dtype='object')

weight_names = []
weight_vals = []

for i in range(9):
    weight_names.append(excel_data[i+7][0][:-1])
    weight_vals.append(float(excel_data[i+7][7]))          # people weights [kg]

weight_names.append(excel_data[17][0][:-7])
weight_names.append('BEM')

weight_vals.append(float(excel_data[17][3])*0.453592)     # fuel weight [kg]
weight_vals.append(0.0)                                    # BEM weight, STILL NEEDS TO BE COMPUTED

weights[0][0] = weight_names
weights[1][0] = weight_vals

total_starting_weight = sum(weights[1][0])                  # [kg]


# ======= B) 1st stationary measurements =======

stat_1 = np.zeros((7,2),dtype='object')
stat_1_conv = np.zeros((7,2),dtype='object')

for i in range(len(stat_1)):
    
    # Measured values
    stat_1[i][0] = excel_data[24][i+3]+' '+excel_data[25][i+3]
    temp = excel_data[27:33,i+3:i+4]
    stat_1[i][1] = temp.astype(dtype='float')
   
# Converted names (to SI units)
stat_1_conv[0][0] = stat_1[0][0][:-4]+'[m]'
stat_1_conv[1][0] = stat_1[1][0][:-5]+'[m/s]'
stat_1_conv[3][0] = stat_1[3][0][:-8]+'[kg/s]'
stat_1_conv[4][0] = stat_1[4][0][:-8]+'[kg/s]'
stat_1_conv[5][0] = stat_1[5][0][:-5]+'[kg]'
stat_1_conv[6][0] = stat_1[6][0][:-4]+'[K]'

# Converted values (to SI units)
stat_1_conv[0][1] = stat_1[0][1]*0.3048             # ft     => m
stat_1_conv[1][1] = stat_1[1][1]*0.514444           # kts    => m/s
stat_1_conv[3][1] = stat_1[3][1]*0.000125998        # lbs/hr => kg/s
stat_1_conv[4][1] = stat_1[4][1]*0.000125998        # lbs/hr => kg/s
stat_1_conv[5][1] = stat_1[5][1]*0.453592           # lbs    => kg
stat_1_conv[6][1] = stat_1[6][1]+273                # °C     => K


# ======= C) 2nd stationary measurements =======

stat_2 = np.zeros((10,2),dtype='object')
stat_2_conv = np.zeros((10,2),dtype='object')

for i in range(len(stat_2)):
    
    # Measured values
    stat_2[i][0] = excel_data[55][i+3]+' '+excel_data[56][i+3]
    temp = excel_data[58:65,i+3:i+4] 
    stat_2[i][1] = temp.astype(dtype='float')

# Converted names (to SI units)  
stat_2_conv[0][0] = stat_2[0][0][:-4]+'[m]'
stat_2_conv[1][0] = stat_2[1][0][:-5]+'[m/s]'
stat_2_conv[6][0] = stat_2[6][0][:-8]+'[kg/s]'
stat_2_conv[7][0] = stat_2[7][0][:-8]+'[kg/s]'
stat_2_conv[8][0] = stat_2[8][0][:-5]+'[kg]'
stat_2_conv[9][0] = stat_2[9][0][:-4]+'[K]'

# Converted values (to SI units)
stat_2_conv[0][1] = stat_2[0][1]*0.3048             # ft     => m
stat_2_conv[1][1] = stat_2[1][1]*0.514444           # kts    => m/s
stat_2_conv[6][1] = stat_2[6][1]*0.000125998        # lbs/hr => kg/s
stat_2_conv[7][1] = stat_2[7][1]*0.000125998        # lbs/hr => kg/s
stat_2_conv[8][1] = stat_2[8][1]*0.453592           # lbs    => kg
stat_2_conv[9][1] = stat_2[9][1]+273                # °C     => K


# ======= D) Xcg shift =======
    
stat_xcg = np.zeros((10,2),dtype='object')
stat_xcg_conv = np.zeros((10,2),dtype='object')

for i in range(len(stat_xcg)):
    
    # Measured values
    stat_xcg[i][0] = excel_data[72][i+3]+' '+excel_data[73][i+3]
    temp = excel_data[74:76,i+3:i+4] 
    stat_xcg[i][1] = temp.astype(dtype='float')
    
# Converted names (to SI units)  
stat_xcg_conv[0][0] = stat_xcg[0][0][:-4]+'[m]'
stat_xcg_conv[1][0] = stat_xcg[1][0][:-5]+'[m/s]'
stat_xcg_conv[6][0] = stat_xcg[6][0][:-8]+'[kg/s]'
stat_xcg_conv[7][0] = stat_xcg[7][0][:-8]+'[kg/s]'
stat_xcg_conv[8][0] = stat_xcg[8][0][:-5]+'[kg]'
stat_xcg_conv[9][0] = stat_xcg[9][0][:-4]+'[K]'

# Converted values (to SI units)
stat_xcg_conv[0][1] = stat_xcg[0][1]*0.3048             # ft     => m
stat_xcg_conv[1][1] = stat_xcg[1][1]*0.514444           # kts    => m/s
stat_xcg_conv[6][1] = stat_xcg[6][1]*0.000125998        # lbs/hr => kg/s
stat_xcg_conv[7][1] = stat_xcg[7][1]*0.000125998        # lbs/hr => kg/s
stat_xcg_conv[8][1] = stat_xcg[8][1]*0.453592           # lbs    => kg
stat_xcg_conv[9][1] = stat_xcg[9][1]+273                # °C     => K


# ======= E) Eigenmotion times =======
# Can be used as inputs for Matlab data to find relevant time point

eigenmotion_times = np.zeros((6,2),dtype='object')
eigenmotion_times_conv = np.zeros((6,2),dtype='object')

eigenmotion_times[0][0] = excel_data[82][0]
eigenmotion_times[1][0] = excel_data[83][0]
eigenmotion_times[2][0] = excel_data[82][4]
eigenmotion_times[3][0] = excel_data[83][4]
eigenmotion_times[4][0] = excel_data[82][7]
eigenmotion_times[5][0] = excel_data[83][7]

eigenmotion_times[0][1] = excel_data[82][3]
eigenmotion_times[1][1] = excel_data[83][3]
eigenmotion_times[2][1] = excel_data[82][6]
eigenmotion_times[3][1] = excel_data[83][6]
eigenmotion_times[4][1] = excel_data[82][9]
eigenmotion_times[5][1] = excel_data[83][9]

# Printing intructions when running
print()
print()
print()
print('INSTRUCTIONS EXCEL:')
print('NOTE: please have file REFERENCE_Post_Flight_Datasheet_Flight.csv in same folder and saved in .csv format!')
print('Constructed arrrays are (converted to SI units):')
print('1. 1st stationary measurements array = stat_1_conv')
print('2. 2nd stationary measurements array = stat_2_conv')
print('3. Xcg shift array = stat_xcg_conv')
print()
print('How to extract the data: Example for stat_1_conv')
print('a) stat_1_conv[0] gives first measured parameter.')
print('b) stat_1_conv[0][0] gives the name of this parameter.')   
print('c) stat_1_conv[0][1] gives the actual measured data.')
    

print (stat_1_conv[0][0])
