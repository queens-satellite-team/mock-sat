"""
Sean Tedesco October 2020
Communications Team 
Implementation of a Ground Station Control Panel of the QSAT Moc-Sat

The main objective of this module includes: 
    1. To have a GUI to choose from a list of commands 
    2. Easy communication to a connected Transmitting Radio (Arduino and RF24, or STM32 and CC1120)
    3. See progress of incoming data and have a log of previously sent commands and received data. 
"""

"""
Reference Material: 

Widget Class	Description
Label	            A widget used to display text on the screen
Button	            A button that can contain text and can perform an action when clicked
Entry	            A text entry widget that allows only a single line of text
Text	            A text entry widget that allows multiline text entry
Frame	            A rectangular region used to group related widgets or provide padding between widgets
"""

from tkinter import Menu, HORIZONTAL
from tkinter import scrolledtext
from tkinter.ttk import Progressbar
import tkinter as tk
from datetime import datetime
import serial
import sys
import time
import base64

startMarker = "<"
endMarker = ">"
dataStarted = False
newCMD = False
dataBuf = ""
messageComplete = False
pack_size = 32
start = 0
stop = pack_size
# portname = "/dev/cu.usbserial-1420"
portname = "/dev/cu.usbserial-1410"
# portname = "/dev/cu.usbmodem14101"

####################################################################
######################### ARDUINO CONTROL ##########################
####################################################################
def setupSerial(baudRate, serialPortName):

    global serialPort

    serialPort = serial.Serial(
        port=serialPortName, baudrate=baudRate, timeout=0, rtscts=True
    )

    print("Serial port " + serialPortName + " opened  Baudrate " + str(baudRate))

    waitForArduino()


def arduinoACK():
    msg = ""
    while msg.find("success") == -1:
        msg = recvLikeArduino()
        if not (msg == "XXX"):
            print(msg)
            return True


def waitForArduino():

    # wait until the Arduino sends 'Arduino is ready' - allows time for Arduino reset
    # it also ensures that any bytes left over from a previous message are discarded

    print("Waiting for Arduino to Reset...")

    msg = ""
    while msg.find("Arduino is ready") == -1:
        msg = recvLikeArduino()
        if not (msg == "XXX"):
            print(msg)


def recvLikeArduino():

    global startMarker, endMarker, serialPort, dataStarted, dataBuf, messageComplete

    if serialPort.inWaiting() > 0 and messageComplete == False:
        x = serialPort.read().decode("utf-8")  # decode needed for Python3
        x = x.rstrip("\r\n")

        if dataStarted == True:
            if x != endMarker:
                dataBuf = dataBuf + x
            else:
                dataStarted = False
                messageComplete = True
        elif x == startMarker:
            dataBuf = ""
            dataStarted = True

    if messageComplete == True:
        messageComplete = False
        return dataBuf
    else:
        return "XXX"


def sendToArduino(stringToSend):

    # this adds the start- and end-markers before sending
    global startMarker, endMarker, serialPort

    stringWithMarkers = startMarker
    stringWithMarkers += stringToSend
    stringWithMarkers += endMarker

    if serialPort.write(stringWithMarkers.encode("utf-8")):  # encode needed for Python3
        print("Success: Sent a packet to Arduino.")
    else:
        print("Error: Could not write to Arduino.")


def imageToCharacters(file):

    # encode bytes in file to base64 characters
    global img_chars, nchars

    with open(file, mode="rb") as image:
        img_encoded = base64.b64encode(image.read())
        if img_encoded:
            print("Image file successfully encoded.")
        else:
            print("Error: image file did not encode.")

        img_chars = img_encoded.decode("utf-8")
        if img_chars:
            print("Encoded image succefullly converted to utf-8 string.")
        else:
            print("Error: Encoded image did not convert to utf-8 string.")

        nchars = len(img_chars)
        print("Encoded Image is " + str(nchars) + " characters long.")


def createPack():

    global img_chars, start, stop, pack_size

    pack = img_chars[start:stop]

    if pack:
        print("Success: Pack succesfully created.")
        start += pack_size
        stop += pack_size
    else:
        print("Error: pack not created.")
        return

    return pack


####################################################################
############################## GUI #################################
####################################################################
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("MOC SAT Ground Station")
        self.master.geometry("1024x564")  # width x height
        self.create_widgets()

    def enter_cmd(self):
        self.log_text_box.configure(state="normal")
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log_text_box.insert("end", current_time + " Implementing: ")
        self.log_text_box.insert("end", self.cmd_variable.get() + " ")
        if self.cmd_variable.get() == cmd_List[0]:
            self.log_text_box.insert("end", "\n")
            self.log_text_box.insert("end", "LA: " + self.lat_entry.get() + " ")
            self.log_text_box.insert("end", "LO:" + self.long_entry.get() + " ")
            print(self.long_entry.get())
        self.log_text_box.insert("end", "\n")
        self.log_text_box.configure(state="disabled")

        if self.cmd_variable.get() == cmd_List[0]:
            self.cmd_one()
        elif self.cmd_variable.get() == cmd_List[1]:
            self.cmd_two()
        elif self.cmd_variable.get() == cmd_List[2]:
            self.cmd_three()

    def clear_text_cmd(self):
        self.log_text_box.configure(state="normal")
        self.log_text_box.delete("1.0", tk.END)
        self.log_text_box.configure(state="disabled")

    def update_add_frame(self, cmd):
        if self.cmd_variable.get() == cmd_List[0]:

            self.add_data_frame.config(text="Send Data")

            for widget in self.add_data_frame.winfo_children():
                widget.destroy()

            ### ADDITIONAL DATA FRAME -- LATITUDE LABEL ###
            self.lat_label = tk.Label(self.add_data_frame, text="Latitude: ")
            self.lat_label.config(font=("Courier", 12))
            self.lat_label.grid(row=0, column=0, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- ENTRY ###
            self.lat_entry = tk.Entry(self.add_data_frame, width=20)
            self.lat_entry.grid(row=0, column=1, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- LONGNITUDE LABEL ###
            self.lat_label = tk.Label(self.add_data_frame, text="Longitude: ")
            self.lat_label.config(font=("Courier", 12))
            self.lat_label.grid(row=1, column=0, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- LONGNITUDE ENTRY ###
            self.long_entry = tk.Entry(self.add_data_frame, width=20)
            self.long_entry.grid(row=1, column=1, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- ENTER BUTTON ###
            self.enter = tk.Button(
                self.add_data_frame, text="Enter", fg="green", command=self.enter_cmd
            )
            self.enter.grid(row=2, column=0, sticky="W", padx=8, pady=4)

        elif self.cmd_variable.get() == cmd_List[1]:

            self.add_data_frame.config(text="Current Health Status")

            for widget in self.add_data_frame.winfo_children():
                widget.destroy()

            ### ADDITIONAL DATA FRAME -- VOLTAGE LEVEL LABEL ###
            self.voltage_label = tk.Label(self.add_data_frame, text="Battery Voltage: ")
            self.voltage_label.config(font=("Courier", 12))
            self.voltage_label.grid(row=0, column=0, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- VOLTAGE LEVEL ENTRY ###
            self.voltage_text_box = tk.Text(self.add_data_frame)
            self.voltage_text_box.config(
                font=("Courier", 12), width=10, height=1, state="disabled"
            )
            self.voltage_text_box.grid(row=0, column=1, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- CURRENT LEVEL LABEL ###
            self.current_label = tk.Label(self.add_data_frame, text="Battery Current: ")
            self.current_label.config(font=("Courier", 12))
            self.current_label.grid(row=1, column=0, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- CURRENT LEVEL ENTRY ###
            self.current_text_box = tk.Text(self.add_data_frame)
            self.current_text_box.config(
                font=("Courier", 12), width=10, height=1, state="disabled"
            )
            self.current_text_box.grid(row=1, column=1, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- INTERNAL HEAT LABEL ###
            self.temp_label = tk.Label(self.add_data_frame, text="Satellite Temp: ")
            self.temp_label.config(font=("Courier", 12))
            self.temp_label.grid(row=2, column=0, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- INTERNAL HEAT ENTRY ###
            self.temp_text_box = tk.Text(self.add_data_frame)
            self.temp_text_box.config(
                font=("Courier", 12), width=10, height=1, state="disabled"
            )
            self.temp_text_box.grid(row=2, column=1, sticky="W", padx=8, pady=4)

            ### ADDITIONAL DATA FRAME -- UPDATE HEALTH VALUES BUTTON ###
            self.enter = tk.Button(
                self.add_data_frame, text="Update", fg="green", command=self.enter_cmd
            )
            self.enter.grid(row=3, column=0, sticky="W", padx=8, pady=4)

        elif self.cmd_variable.get() == cmd_List[2]:

            self.add_data_frame.config(text="Confirm Reboot")

            for widget in self.add_data_frame.winfo_children():
                widget.destroy()

            ### ADDITIONAL DATA FRAME -- CONFIRM BUTTON ###
            self.enter = tk.Button(
                self.add_data_frame, text="CONFIRM", fg="green", command=self.enter_cmd
            )
            self.enter.grid(row=0, column=0, sticky="N", padx=8, pady=4)

    def create_widgets(self):
        ### TITLE ###
        self.title = tk.Label(text="MOC-SAT Control Panel")
        self.title.config(font=("Courier", 32))
        self.title.grid(row=0, sticky="N", padx=8, pady=4)

        ### COMMAND OPTION FRAME ###
        self.cmd_frame = tk.LabelFrame(self.master, text="Command Options")
        self.cmd_frame.config(font=("Courier", 22))
        self.cmd_frame.grid(row=1, column=0, padx=8, pady=4, sticky="nw")

        ### RECEIVED DATA FRAME ###
        self.recv_frame = tk.LabelFrame(self.master, text="Received Data")
        self.recv_frame.config(font=("Courier", 22))
        self.recv_frame.grid(row=1, column=1, rowspan=2, padx=8, pady=4, sticky="ne")

        ### ADDITIONAL DATA FRAME ###
        self.add_data_frame = tk.LabelFrame(self.master)
        self.add_data_frame.config(font=("Courier", 22))
        self.add_data_frame.grid(row=2, column=0, padx=8, pady=4, sticky="nw")

        ### PROGRESS BAR FRAME ###
        self.progress_bar_frame = tk.LabelFrame(
            self.master, text="Received Data Progress"
        )
        self.progress_bar_frame.config(font=("Courier", 22))
        self.progress_bar_frame.grid(row=3, columnspan=2, padx=8, pady=4, sticky="nw")

        ### COMMAND OPTION FRAME -- HEADER ###
        self.cmd_heading = tk.Label(self.cmd_frame, text="Choose a Command:")
        self.cmd_heading.config(font=("Courier", 16))
        self.cmd_heading.grid(row=0, column=0, sticky="W", padx=8, pady=4)

        ### COMMAND OPTION FRAME -- OPTION MENU ###
        global cmd_List
        cmd_List = ("Retrieve Image", "Retrieve System Health", "Reboot Satellite")
        self.cmd_variable = tk.StringVar()
        self.cmd_variable.set(cmd_List[0])
        self.cmd_option_menu = tk.OptionMenu(
            self.cmd_frame, self.cmd_variable, *cmd_List, command=self.update_add_frame
        )
        self.cmd_option_menu.grid(row=1, column=0, sticky="W", padx=8, pady=4)

        ### RECEIVED DATA FRAME -- HEADER ###
        self.recv_header = tk.Label(self.recv_frame, text="Data Log")
        self.recv_header.config(font=("Courier", 16))
        self.recv_header.grid(row=0, column=0, sticky="W", padx=8, pady=4)

        ### RECEIVED DATA FRAME -- TEXTBOX ###
        self.log_text_box = tk.Text(self.recv_frame)
        self.log_text_box.config(font=("Courier", 14), width=50, height=20)
        self.log_text_box.grid(row=1, column=0, sticky="W", padx=8, pady=4)

        ### RECEIVED DATA FRAME -- CLEAR BUTTON ###
        self.clear_text_button = tk.Button(
            self.recv_frame, text="Clear", command=self.clear_text_cmd
        )
        self.clear_text_button.grid(row=2, column=0, sticky="W", padx=8, pady=4)

        ### PROGRRESS BAR FRAME ###
        self.progress = Progressbar(
            self.progress_bar_frame, orient=HORIZONTAL, length=900, mode="determinate"
        )
        self.progress.grid(row=0, column=0, sticky="N", padx=8, pady=4)

        ### MASTER FRAME -- QUIT BUTTON ###
        self.quit = tk.Button(
            self.master, text="Quit", fg="red", command=self.master.destroy
        )
        self.quit.grid(row=4, column=0, sticky="sw", padx=8, pady=4)

    def console_print(self, msg):
        self.log_text_box.configure(state="normal")
        self.log_text_box.insert("end", msg)
        self.log_text_box.insert("end", "\n")
        self.log_text_box.insert("end", "\n")
        self.log_text_box.configure(state="disabled")

    def cmd_one(self):
        """receive image command"""
        sendToArduino("cmd_1_1234")

        self.console_print("Waiting for Arduino...")
        if arduinoACK():
            self.console_print("Transmitted Successfully.")
        else:
            self.console_print("Failed Transmission.")

    def cmd_two(self):
        """get health values"""
        sendToArduino("cmd_2_5678")

        self.console_print("Waiting for Arduino...")
        if arduinoACK():
            self.console_print("Transmitted Successfully.")
        else:
            self.console_print("Failed Transmission.")

    def cmd_three(self):
        """reboot SAT -- blink some LEDS for now"""
        sendToArduino("cmd_3_9012")

        self.console_print("Waiting for Arduino...")
        if arduinoACK():
            self.console_print("Transmitted Successfully.")
        else:
            self.console_print("Failed Transmission.")


####################################################################
########################## MAIN WINDOW #############################
####################################################################
def main():
    setupSerial(9600, portname)
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()


if __name__ == "__main__":
    main()
