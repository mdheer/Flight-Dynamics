import numpy as np
import scipy.io as sio
from StationaryValues import *


""" =============== PART I: MATLAB DATA =============== """

# Importing reference matlab file 'matlab.mat'
# Importing flight data file 'FTISxprt-20190308_152811.mat'
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
ref_data = np.zeros((50,3),dtype='object')

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
        
#ref_data = np.delete(ref_data,10,0)

# Calling a certain line from the ref_data to get its values in an array
def get_data(i):
    return ref_data[i][2]

# Printing intructions when running
#print()
#print("\033[1;31;43mINSTRUCTIONS MATLAB:")
#print('1. Type "print_pars_w_index()" to get indices of each parameter for next function.')
#print('2. Type get_data(i) with desired i from the given indices to get the data of the chosen parameter in an array.')
#print('NOTE: must have matlab.mat file in same folder.')
#print('NOTE2: matlab units have not been converted to SI units as yet.')



""" =============== PART II: EXCEL DATA =============== """

# Importing excel data from excel file reference case: 'REFERENCE_Post_Flight_Datasheet_Flight.csv'
# Importing excel data from excel file reference case: 'Post_Flight_Datasheet_08_03_V4.csv'
# NOTE: Please save file as .csv instead of .xlsx
# IMPORTANT: must have Numpy version 1.15+
filename = 'Post_Flight_Datasheet_08_03_V4.csv'
excel_data = np.genfromtxt(filename,delimiter=',',dtype='str',encoding='bytes')

if filename == 'REFERENCE_Post_Flight_Datasheet_Flight.csv':
    second_length = 65
elif filename == 'Post_Flight_Datasheet_08_03_V4.csv':
    second_length = 63

    
    
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
startfuelmass = float(excel_data[17][3])
weight_vals.append(4157.17)                                    # BEM weight [kg]

weights[0][0] = weight_names
weights[1][0] = weight_vals

total_starting_mass = sum(weights[1][0])                  # [kg]


# ======= B) 1st stationary measurements =======

stat_1 = np.zeros((7,2),dtype='object')
stat_1_conv = np.zeros((7,2),dtype='object')

for i in range(len(stat_1)):
    
    # Measured values
    stat_1[i][0] = excel_data[24][i+3]+' '+excel_data[25][i+3]
    temp = excel_data[27:33,i+3:i+4]
    stat_1[i][1] = temp.astype(dtype='float')
    
    stat_1_conv[i][0] = stat_1[i][0]
    stat_1_conv[i][1] = stat_1[i][1]
   
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
stat_1_conv[6][1] = stat_1[6][1]+273.15             # °C     => K


# ======= C) 2nd stationary measurements =======

stat_2 = np.zeros((10,2),dtype='object')
stat_2_conv = np.zeros((10,2),dtype='object')

for i in range(len(stat_2)):
    
    # Measured values
    stat_2[i][0] = excel_data[55][i+3]+' '+excel_data[56][i+3]
    temp = excel_data[58:second_length,i+3:i+4]
    stat_2[i][1] = temp.astype(dtype='float')
    
    stat_2_conv[i][0] = stat_2[i][0]
    stat_2_conv[i][1] = stat_2[i][1]

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
stat_2_conv[9][1] = stat_2[9][1]+273.15             # °C     => K


# ======= D) Xcg shift =======
    
stat_xcg = np.zeros((10,2),dtype='object')
stat_xcg_conv = np.zeros((10,2),dtype='object')

for i in range(len(stat_xcg)):
    
    # Measured values
    stat_xcg[i][0] = excel_data[72][i+3]+' '+excel_data[73][i+3]
    temp = excel_data[74:76,i+3:i+4] 
    stat_xcg[i][1] = temp.astype(dtype='float')
    
    stat_xcg_conv[i][0] = stat_xcg[i][0]
    stat_xcg_conv[i][1] = stat_xcg[i][1]
    
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
stat_xcg_conv[9][1] = stat_xcg[9][1]+273.15             # °C     => K


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
#print()
#print()
#print()
#print('INSTRUCTIONS EXCEL:')
#print('NOTE: please have file REFERENCE_Post_Flight_Datasheet_Flight.csv in same folder and saved in .csv format!')
#print('Constructed arrrays are (converted to SI units):')
#print('1. 1st stationary measurements array = stat_1_conv')
#print('2. 2nd stationary measurements array = stat_2_conv')
#print('3. Xcg shift array = stat_xcg_conv')
#print()
#print('How to extract the data: Example for stat_1_conv')
#print('a) stat_1_conv[0] gives first measured parameter.')
#print('b) stat_1_conv[0][0] gives the name of this parameter.')   
#print('c) stat_1_conv[0][1] gives the actual measured data.')
#print('You can remove these print statements once you have read the instructions :)')
#print()
#print('\033[0;30m')
    

""" =============== PART III: THRUST DATA =============== """
filethrust = open("thrust.dat", "r") 
lines=filethrust.readlines()
Thrustresult=[]
for x in lines:
    Thrustresult.append(x.split()[0])
    Thrustresult.append(x.split()[1])
filethrust.close()



""" =============== PART IV: SOME FUNCTIONS =============== """

def show_eigmot_names():
    for i in range(len(eigenmotion_times)):
        print(eigenmotion_times[i][0])

def get_eigmot(name):
    
    for i in range(len(eigenmotion_times)):
        if name == eigenmotion_times[i][0]:
            print(name)
            index = i
    
    time = eigenmotion_times[index][1]
    #print(time)
    
    seconds = float(time[-2:])
    minutes = float(time[-5:-3])
    
    if len(time)>5:
        hours = float(time[-7:-6])
    else:
        hours = 0.
    
    total_time = seconds+minutes*60+hours*3600
    
    time_data = get_data(48)[0]
    
    for j,t in enumerate(time_data):
        if t == total_time:
            jndex = j
    
    #print(jndex)    
    
    V_TAS = get_data(42)[jndex][0]*0.514444         # [m/s]
    
    mass = total_starting_mass - get_data(14)[jndex][0]*0.000125998 - get_data(15)[jndex][0]*0.000125998    # [kg/s]
    
    hp = get_data(37)[jndex][0]
    Tm = get_data(36)[jndex][0]
    V_IAS = get_data(41)[jndex][0]
    rho = DynamicValues(hp,Tm,V_IAS)[2]
    
    # Initial values SYMM
    pitch = radians(get_data(22)[jndex][0])
    alpha_0 = radians(get_data(1)[jndex][0])
    q_0 = radians(get_data(27)[jndex][0])
    el_defl = radians(get_data(17)[jndex][0])
    
    # Checking which motion to determine alpha interval
    if name == 'Phugoid' or name == 'Spiral':
        time_int = 150
    elif name == 'Short period':
        time_int = 10
    else:
        time_int = 15
    
    alpha_int = []
    el_defl_int = []
    V_TAS_int = []
    pitch_int = []
    q_int = []
    
    # Initial values ASYMM
    roll_0 = radians(get_data(21)[jndex][0])
    p_0 = radians(get_data(26)[jndex][0]) # roll rate
    r_0 = radians(get_data(28)[jndex][0]) # yaw rate
    
    rud_defl_int = []
    ail_defl_int = []
    roll_int = []
    p_int = []
    r_int = []
    
    
    for t in range(time_int*10):
        alpha_int.append(get_data(1)[jndex+t][0])
        el_defl_int.append(radians(get_data(17)[jndex+t][0]))
        V_TAS_int.append(get_data(42)[jndex+t][0]*0.514444)
        pitch_int.append(get_data(22)[jndex+t][0])
        q_int.append(get_data(27)[jndex+t][0])
        
        rud_defl_int.append(radians(get_data(18)[jndex+t][0]))
        ail_defl_int.append(radians(get_data(16)[jndex+t][0]))
        roll_int.append(get_data(21)[jndex+t][0])
        p_int.append(get_data(26)[jndex+t][0]) # roll rate
        r_int.append(get_data(28)[jndex+t][0]) # yaw rate

    return V_TAS,mass,rho,pitch,alpha_0,q_0,el_defl,alpha_int,el_defl_int,\
           V_TAS_int,pitch_int,q_int,roll_0,p_0,r_0,rud_defl_int,ail_defl_int,\
           roll_int,p_int,r_int,jndex

def eigmot_ret_ind():
    names = ['V_TAS [m/s]','mass [kg]','rho [kg/m3]','pitch [deg]','alpha_0 [deg]','q_0 [deg/s]',\
             'el_defl [deg]','alpha_int [list][deg]','el_defl_int [list][deg]','V_TAS_int [list][m/s]',\
             'pitch_int [list][deg]','q_int [list][deg/s]','roll_0 [deg]','p_0 [deg/s]','r_0 [deg/s]',\
             'rud_defl_int [list][deg]','ail_defl_int [list][deg]','roll_int [list][deg]','p_int [list][deg/s]',\
             'r_int [list][deg/s]','index']
    for i in range(len(get_eigmot('Phugoid'))):
        print(i,'=',names[i])

def stat_mass(Fused):
    """ Fused = the array with fuel used, of the desired measurement. """
    """ Returns an array for total mass at that measurement moment.   """
    return (total_starting_mass - Fused)

