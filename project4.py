##########################
# Project - 4 
# Name: Divyesh Rathod
# ASU ID: 1225916954
###########################

import numpy as np               
import subprocess                                 
import re

# Initial values
new_tphl = 100000        # high value for comparison
new_n = 0                # placeholder no. of inverters
new_fan = 0              # placeholder no. of fans

# Loop through odd values of N from 1 to 13
for N in range(1,13,2):           
    # Loop through values of fan from 2 to 7
    for fan_value in range(2,8):   

        # Make a copy of the original netlist and add the fan parameter
        process_1 = subprocess.Popen(["cp","InvChain.sp","temporary_netlist.sp"])    
        process_1.communicate()                 
        file = open("temporary_netlist.sp","a")            
        file.write(".param fan = "+str(fan_value)+"\n")
        
        # Loop through the index values from 1 to N and add the corresponding netlist lines
        for index_value in range(1,N+1):                
            
            if(N==1):          
                file.write("Xinv"+str(index_value)+" a "+"z"+" inv M="+str(index_value)+"\n"+".end")
                            
            elif( (index_value == 1) & (N>1) ):    
                file.write("Xinv"+str(index_value)+" a "+"n"+str(index_value)+" inv M="+str(index_value)+"\n")
            
            elif(index_value == N):                
                file.write("Xinv"+str(index_value)+" n"+str(index_value-1)+" z"+" inv M=fan**"+str(index_value-1)+"\n"+".end")
            
            else:                                   
                file.write("Xinv"+str(index_value)+" n"+str(index_value-1)+" n"+str(index_value)+" inv M=fan**"+str(index_value-1)+"\n")
         
        file.close()                
        
        # Run HSPICE simulation and extract the delay value
        process_2 = subprocess.Popen(["hspice","temporary_netlist.sp"], stdout=subprocess.PIPE,stderr=subprocess.PIPE)    
        output, err = process_2.communicate()    
        data = np.recfromcsv("temporary_netlist.mt0.csv",comments="$",skip_header=3)     
        tphl = data["tphl_inv"]                                                         
        
        # Print the delay value for the current configuration
        print("With", N, "inverters and fan value", fan_value, "delay is", tphl, "seconds")
       

        # Update the values if the current delay is smaller than the previous smallest delay
        if(tphl < new_tphl):     
            new_tphl= tphl      
            new_n = N         
            new_fan = fan_value
        
        # Break the loop if N is 1 (only one inverter)
        if(N == 1):              
            break                     

# Print the final results          
print(" Number of Inverters: ",new_n)
print(" Fan: ",new_fan)
print(" tphl delay: =",new_tphl)