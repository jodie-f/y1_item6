from backend import SmartPlug, SmartFridge, SmartHome
from tkinter import *

def setUpHome():
    devices = []
    home = SmartHome()
    print("Available Smart Devices:")
    print("- Smart Plug \n- Smart Fridge")
    print("Please input five devices you want in your Smart Home:")

    for i in range(5):
        validDevice = True
        while validDevice:
            device = input(f"{i+1}. ")
            validDevice = checkDevice(device)

        if isSmartPlug(device):
            rate = smartPlugRate()
            devices.append(SmartPlug(rate))
        else:
            devices.append(SmartFridge())
            
    for device in devices:
        home.addDevice(device)
    # print(home)

def checkDevice(device):
    validInputs = ["smart plug", "plug", "smart fridge", "fridge"]
    if device.lower() in validInputs:
        return False
    else:
        print("Input is invalid, please choose from the available Smart Devices")
        return True

def isSmartPlug(device):
    validInputs = ["smart plug", "plug"]
    if device.lower() in validInputs:
        return True
    
def smartPlugRate():
    while True:
        rate = input("Consumption rate: ")
        if not rate.isdigit():
            print("Input is not a number, please input a rate between 0 and 150")
        # elif 0 >= int(rate) >= 150:
        elif int(rate) <= 0 or int(rate) >= 150:
            print("Rate must be between 0 and 150. Please try again")
        else:
            return int(rate)

# GUI
class SmartHomeSystem:
    def __init__(self):
        self.win = Tk()
        self.win.title("Smart Home System")
        self.win.geometry("500x350")

        self.mainFrame = Frame(self.win)
        self.mainFrame.grid(column=0, row=0, padx=5, pady=5)
        # self.userName = StringVar()
        # self.password = StringVar()
        # self.message = StringVar()
        # self.message.set("Enter username and password.")
    
    def createWidgets(self):
        btnOn = Button (
            self.mainFrame,
            text="Turn on all",
            width=25
            # command=
        )
        btnOn.grid(row=0, column=0, padx=10, pady=10)

        btnOff = Button (
            self.mainFrame,
            text="Turn on all",
            width=25
        )
        btnOff.grid(row=0, column=1, columnspan=3, padx=10, pady=10)


        # ------ ROW 1 -------
        lblFridge1 = Label (
            self.mainFrame,
            text="Fridge: off, Temperature: 3"
        )
        lblFridge1.grid(row=1, column=0, padx=10, pady=10)

        btnToggle1 = Button (self.mainFrame, text="Toggle", width=7)
        btnToggle1.grid(row=1, column=1, padx=10, pady=10)
        
        btnEdit1 = Button (self.mainFrame, text="Edit", width=6)
        btnEdit1.grid(row=1, column=2, padx=10, pady=10)
        
        btnDelete1 = Button (self.mainFrame, text="Delete", width=7)
        btnDelete1.grid(row=1, column=3, padx=10, pady=10)


        # ------ ROW 2 -------
        lblFridge2 = Label (
            self.mainFrame, 
            text="Fridge: on, Temperature: 1"
        )
        lblFridge2.grid(row=2, column=0, padx=10, pady=10)

        btnToggle2 = Button (self.mainFrame, text="Toggle", width=7)
        btnToggle2.grid(row=2, column=1, padx=10, pady=10)
        
        btnEdit2 = Button (self.mainFrame, text="Edit", width=6)
        btnEdit2.grid(row=2, column=2, padx=10, pady=10)
        
        btnDelete2 = Button (self.mainFrame, text="Delete", width=7)
        btnDelete2.grid(row=2, column=3, padx=10, pady=10)


        # ------ ROW 3 -------
        lblPlug1 = Label (
            self.mainFrame,
            text="Plug: off, Consumption: 150"
        )
        lblPlug1.grid(row=3, column=0, padx=10, pady=10)
        
        btnToggle3 = Button (self.mainFrame, text="Toggle", width=7)
        btnToggle3.grid(row=3, column=1, padx=10, pady=10)
        
        btnEdit3 = Button (self.mainFrame, text="Edit", width=6)
        btnEdit3.grid(row=3, column=2, padx=10, pady=10)
        
        btnDelete3 = Button (self.mainFrame, text="Delete", width=7)
        btnDelete3.grid(row=3, column=3, padx=10, pady=10)

        
        # ------ ROW 4 -------
        lblPlug2 = Label (
            self.mainFrame,
            text="Plug: on, Consumption: 45"
        )
        lblPlug2.grid(row=4, column=0, padx=10, pady=10)
        
        btnToggle4 = Button (self.mainFrame, text="Toggle", width=7)
        btnToggle4.grid(row=4, column=1, padx=10, pady=10)
        
        btnEdit4 = Button (self.mainFrame, text="Edit", width=6)
        btnEdit4.grid(row=4, column=2, padx=10, pady=10)
        
        btnDelete4 = Button (self.mainFrame, text="Delete", width=7)
        btnDelete4.grid(row=4, column=3, padx=10, pady=10)


        # ------ ROW 5 -------
        lblPlug3 = Label (
            self.mainFrame,
            text="Plug: on, Consumption: 150"
        )
        lblPlug3.grid(row=5, column=0, padx=10, pady=10)

        btnToggle5 = Button (self.mainFrame, text="Toggle", width=7)
        btnToggle5.grid(row=5, column=1, padx=10, pady=10)
        
        btnEdit5 = Button (self.mainFrame, text="Edit", width=6)
        btnEdit5.grid(row=5, column=2, padx=10, pady=10)
        
        btnDelete5 = Button (self.mainFrame, text="Delete", width=7)
        btnDelete5.grid(row=5, column=3, padx=10, pady=10)

        btnAdd = Button (
            self.mainFrame,
            text="Add",
            width=20
        )
        btnAdd.grid(row=6, column=0, padx=10, pady=10)


    def run(self):
        self.createWidgets()
        self.win.mainloop()

def main():
    setUpHome()

    # smartHomeSystem = SmartHomeSystem()
    # smartHomeSystem.run()

main()