from w1thermsensor import W1ThermSensor #imports the sensor
from time import sleep, strftime, time
import RPi.GPIO as GPIO
from tkinter import *
import matplotlib.pyplot as plt

# writes data to a csv file and stores it for later viewing
def write_temp(tempF):
    with open("/home/pi/Documents/room_temp.csv", "a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(tempF)))  

# function to graph the data
def graph(tempF, seconds):
    y.append(tempF)
    x.append(seconds)
    plt.clf()
    plt.scatter(x, y)
    plt.plot(x, y)
    plt.title("Room Temperature")
    plt.xlabel("Time (Seconds)")
    plt.ylabel("Temperature (Farenheit)")
    plt.draw()
    

def defaultLitLed(tempF):
    global img
    # when temp is too warm, red led lights up
    if tempF > 80:
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        # red thermometer image displays led is ON in gui
        img = PhotoImage(file="redthermometer.png")
        label.config(image=img)
    # when temp is at a comfortable level, green led lights up 
    elif tempF >= 75 and tempF <= 80:
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        # green thermometer image displays led is ON in gui
        img = PhotoImage(file="greenthermometer.png")
        label.config(image=img)
    # when temp is too cool, blue led lights up
    else:
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        # blue thermometer image displays led is ON in gui
        img = PhotoImage(file="bluethermometer.png")
        label.config(image=img)
    
def userLitLED(tempF, UserTemp):
    global img
    # when temp is too warm, red led lights up
    if tempF > (UserTemp + 5):
        GPIO.output(22, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        # red thermometer image displays led is ON in gui
        img = PhotoImage(file="redthermometer.png")
        label.config(image=img)
    # when temp is at a comfortable level, green led lights up 
    elif tempF <= (UserTemp + 5) and tempF >= (UserTemp - 5):
        GPIO.output(21, GPIO.HIGH)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(20, GPIO.LOW)
        # green thermometer image displays led is ON in gui
        img = PhotoImage(file="greenthermometer.png")
        label.config(image=img)
    # when temp is too cool, blue led lights up
    elif tempF < (UserTemp - 5):
        GPIO.output(20, GPIO.HIGH)
        GPIO.output(21, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        # blue thermometer image displays led is ON in gui
        img = PhotoImage(file="bluethermometer.png")
        label.config(image=img)

def getUserTemp():
    global num
    global UserTemp
    num += 1
    UserTemp = int(entry2.get())
    return num, UserTemp
    
    
#################################################################################
# Main Program
#################################################################################
# set up the leds
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

# sets the sensor (W1ThermSensor) as a variable
sensor = W1ThermSensor()

# set up the tkinter window
root = Tk()
root.geometry("300x420+500+0")
root.configure(background="blue")
root.title("Room Temperature")

# image for tkinter window
img = PhotoImage(file="thermometer.png")
label = Label(root, image=img)
label.grid(row=0, column=0)

# User Specified Temperature
button2 = Button(root, text="User Specified Temp", command=getUserTemp)
button2.grid(row=1, column=0)

# Entry window for User Specified Temp
entry2 = Entry(root)
entry2.grid(row=2, column=0)

# Blank label used as a filler
blankLabel = Label(root, text="", bg="blue")
blankLabel.grid(row=3, column=0)

# Label for Avg Temp of Room
label3 = Label(root, text="Avg recorded temp of room: ")
label3.grid(row=4, column=0)

# Blank label used as a filler
blankLabel2 = Label(root, text="", bg="blue")
blankLabel2.grid(row=5, column=0)

# label for Max Temp of Room
label4 = Label(root, text="Max recorded temp of room: ")
label4.grid(row=6, column=0)

# Blank label used as a filler
blankLabel3 = Label(root, text="", bg="blue")
blankLabel3.grid(row=7, column=0)

# label for Min Temp of Room
label5 = Label(root, text="Min recorded temp of room: ")
label5.grid(row=8, column=0)

# plt.ion function lets matplotlib know graphing will be done interactively
plt.ion()
x = []
y = []
seconds = 0
num = 0
while True:
    tempF = round(sensor.get_temperature() * 9.0 / 5.0 + 32.0, 1)
    write_temp(tempF)
    graph(tempF,seconds)
    # Update Avg Temp Label
    if (len(y)) == 0:
        label3.config(text="Avg recorded temp of room: 0")
    elif (len(y)) >= 1:
        average = round((sum(y)) / (len(y)), 1)
        label3.config(text="Avg recorded temp of room {}".format(average))
    # Update Max Temp Label
    if (len(y)) == 0:
        label4.config(text="Max recorded temp: 0")
    elif (len(y)) >= 1:
        label4.config(text="Max recorded temp: {}".format(max(y)))
    # Update Min Temp Label
    if (len(y)) == 0:
        label5.config(text="Min recorded temp: 0")
    elif (len(y)) >= 1:
        label5.config(text="Min recorded temp: {}".format(min(y)))
    # Chooses which way to run the LEDs, default or user defined
    if num == 0:
        defaultLitLed(tempF)
    elif num >= 1:
        userLitLED(tempF, UserTemp)
    root.update()
    seconds += 1
    plt.pause(1)
    
root.mainloop()
GPIO.cleanup()
    
        
        
        






