import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from scipy.signal import find_peaks
import numpy as np
import random
import serial

#initialize serial port
ser = serial.Serial()
ser.port = 'COM8' #Arduino serial port
ser.baudrate = 9600
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters
    
# Create figure for plotting
fig, ax = plt.subplots(2, 1)
freq = [] #store trials here (n)
power = [] #store relative frequency here
adjusted = []

# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    #Aquire and parse data from serial port
    freq = []
    power = []
    adjusted = []
    line = ser.readline()
    line = line.decode("ascii")
    line = line.split(",")
    for i in line:
        entry = i.split(":")
        try:
            freq.append(entry[0])
            power.append(float(entry[1]))
        except:
            continue

    freq.pop()
    adjusted = [power[i]*i for i in range(len(power))]
	# Add x and y to lists
    # Limit x and y lists to 20 items
    freq = freq[:100]
    power = power[:100]
    adjusted = adjusted[:100]
    adjusted = np.array(adjusted)
    norm_adjusted = np.linalg.norm(adjusted)
    adjusted = adjusted/norm_adjusted
    
    trough = find_peaks(-adjusted)[0]
    cycle = 0
    for i in trough:
        if i % trough[0] != 0:
            cycle = "undefined"
        else:
            cycle = 1/trough[0] * 100

    print(cycle)
    # Draw x and y lists
    ax[0].clear()
    ax[1].clear()
    
    ax[0].bar(freq, power, label="Raw")
    ax[0].set_title("Raw Power")
    ax[0].set_xticklabels([])
        
    ax[1].bar(freq, adjusted, label="Adjusted")
    ax[1].set_title("Adjusted")
    ax[1].set_xticklabels([])
    # Format plot
    #plt.xticks(rotation=45, ha='right')
    #plt.subplots_adjust(bottom=0.30)
    plt.legend()
    #plt.axis([1, None, 0, 1.1]) #Use for arbitrary number of trials
    #plt.axis([1, 100, 0, 1.1]) #Use for 100 trial demo

# # Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(freq, adjusted), interval=500)
plt.show()