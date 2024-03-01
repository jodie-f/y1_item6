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
            
    # devices = [SmartPlug(90), SmartPlug(80), SmartPlug(70), SmartFridge(), SmartFridge()] # EDIT OUT LATER

    for device in devices:
        home.addDevice(device)
    
    return home

def checkDevice(device: str):
    validInputs = ["smart plug", "plug", "smart fridge", "fridge"]
    if device.lower() in validInputs:
        return False
    else:
        print("Input is invalid, please choose from the available Smart Devices")
        return True

def isSmartPlug(device: str):
    validInputs = ["smart plug", "plug"]
    if device.lower() in validInputs:
        return True
    
def smartPlugRate():
    while True:
        rate = input("Consumption rate: ")
        if not rate.isdigit():
            print("Input is not a number, please input a rate between 0 and 150")
        elif int(rate) <= 0 or int(rate) >= 150:
            print("Rate must be between 0 and 150. Please try again")
        else:
            return int(rate)

PADDING = 10


# ========================================= GUI =========================================
class SmartHomeSystem:
    def __init__(self, homeDevices: object):
        self.win = Tk()
        self.win.title("Smart Home System")

        self.mainFrame = Frame(self.win)
        self.mainFrame.grid(row=0, column=0, padx=5, pady=5)

        self.homeDevices = homeDevices # smart home obj
        self.homeDeviceWidgets = []
        self.fridgeTemp = StringVar()

        self.editWidgets = []
        self.newValue = IntVar()
        self.newDevice = StringVar()
        self.addWidgets = []
        self.consumptionRate = IntVar() # for added device
        self.consumptionRate.set(0)

    def createWidgets(self):
        self.deleteAllHomeWidgets()

        deviceList = self.homeDevices.getDevices()

        btnOn = Button (
            self.mainFrame,
            text="Turn on all",
            width=25,
            command=self.turnOnAll
        )
        btnOn.grid(row=0, column=0, padx=PADDING, pady=PADDING)

        btnOff = Button (
            self.mainFrame,
            text="Turn off all",
            width=25,
            command=self.turnOffAll
        )
        btnOff.grid(row=0, column=1, columnspan=3, padx=PADDING, pady=PADDING)

        for i, device in enumerate(deviceList, start=1):
            lblDevice = Label (
                self.mainFrame,
                text=device
            )
            lblDevice.grid(row=i, column=0, padx=PADDING, pady=PADDING)
            self.homeDeviceWidgets.append(lblDevice)

            btnToggle = Button (
                self.mainFrame, 
                text="Toggle", 
                width=7,
                command=lambda index=i: self.btnToggleStatus(index)
                )
            btnToggle.grid(row=i, column=1, padx=PADDING, pady=PADDING)
            self.homeDeviceWidgets.append(btnToggle)

            btnEdit = Button (
                self.mainFrame, 
                text="Edit", 
                width=6,
                command=lambda index = i: self.editWin(index)
                )
            btnEdit.grid(row=i, column=2, padx=PADDING, pady=PADDING)
            self.homeDeviceWidgets.append(btnEdit)

            btnDelete = Button (
                self.mainFrame, 
                text="Delete", 
                width=7,
                command=lambda index=i: self.deleteDevice(index)
                )
            btnDelete.grid(row=i, column=3, padx=PADDING, pady=PADDING)
            self.homeDeviceWidgets.append(btnDelete)

        btnAdd = Button (
            self.mainFrame,
            text="Add",
            width=25,
            command=self.addWin
        )
        btnAdd.grid(row=len(deviceList)+1, column=0, padx=PADDING, pady=PADDING)
        self.homeDeviceWidgets.append(btnAdd)
        
    def deleteAllHomeWidgets(self): # RESETS WIDGETS
        for widget in self.homeDeviceWidgets:
            widget.destroy()
        self.homeDeviceWidgets = []

    # ========================================= TOGGLE BUTTONS =========================================
    def turnOnAll(self):
        self.homeDevices.turnOnAll()
        self.createWidgets()
    
    def turnOffAll(self):
        self.homeDevices.turnOffAll()
        self.createWidgets()

    def btnToggleStatus(self, index: int):
        self.homeDevices.toggleSwitch(index-1)
        self.createWidgets()
    
    # ========================================= EDIT BUTTONS =========================================
    def editWin(self, index):
        self.deleteAllEditWidgets()
        device = self.homeDevices.getDevicesAt(index-1)

        newWin = Toplevel(self.win)
        newWin.title("Edit Device")

        # FOR PLUG
        entryValue = Entry(newWin, width=10, textvariable=self.newValue)

        # FOR FRIDGE
        temps = [1, 3, 5]
        opmValue = OptionMenu(
            newWin,
            self.newValue,
            *temps
        )

        btnUpdate = Button(
            newWin, 
            text="Update Device", 
            command=lambda index=index, win=newWin : self.updateOption(index, win))
        btnUpdate.grid(row=1, column=0, columnspan=2, padx=PADDING, pady=PADDING)
        self.editWidgets.append(btnUpdate)

        if isinstance(device, SmartFridge):
            lblText="Temperature:"
            self.newValue.set(device.getTemperature())
            opmValue.grid(row=0, column=1, padx=PADDING, pady=PADDING) # CREATING OPTION MENU
            self.editWidgets.append(opmValue)
        else:
            lblText="Consumption Rate (0-150):"
            self.newValue.set(device.getConsumptionRate())
            entryValue.grid(row=0, column=1, padx=PADDING, pady=PADDING) # CREATING ENTRY
            self.editWidgets.append(entryValue)
        
        lblUpdate = Label(newWin, text=lblText)
        lblUpdate.grid(row=0, column=0, padx=PADDING, pady=PADDING)
        self.editWidgets.append(lblUpdate)

    def updateOption(self, index, win):
        device = self.homeDevices.getDevicesAt(index-1)        
        try:
            newValue = int(self.newValue.get())
        except TclError:
            self.errorMessage("digit")
            return None

        if isinstance(device, SmartFridge):
            device.setTemperature(newValue)
        else:
            if newValue < 0 or newValue > 150:
                self.errorMessage("range")
                return None
            device.setConsumptionRate(newValue)

        self.createWidgets()
        win.destroy()

    def deleteAllEditWidgets(self): # RESETS WIDGETS
        for widget in self.editWidgets:
            widget.destroy()
        self.editWidgets = []

    def errorMessage(self, error):
        msgs = {
            "digit": "Input is not a number!",
            "range": "Input is out of range!"
        }

        errorWin = Toplevel(self.win)
        errorWin.title("ERROR !!!")

        lblError = Label(
            errorWin, 
            text=msgs[error],
        )
        lblError.grid(row=0, column=1, padx=PADDING, pady=PADDING)

        btnError = Button(
            errorWin,
            text="Okay",
            width=10,
            command=errorWin.destroy
        )
        btnError.grid(row=1, column=1, padx=PADDING, pady=PADDING)

    # ========================================= DELETE BUTTON =========================================
    def deleteDevice(self, index):
        self.homeDevices.removeDeviceAt(index-1)
        self.createWidgets()

    # ========================================= ADD BUTTON =========================================
    def addWin(self):
        newWin = Toplevel(self.win)
        newWin.title("Add Device")

        self.plugWidgets(newWin)

        lblNewDevice = Label(newWin, text="Device:")
        lblNewDevice.grid(row=0, column=0, padx=PADDING, pady=PADDING)
        self.newDevice.set("Smart Plug")
        
        opmDevices = OptionMenu(
            newWin,
            self.newDevice,
            "Smart Plug",
            "Smart Fridge",
            command=lambda selected=self.newDevice, addWin=newWin: self.addWidgetPicker(selected, addWin)
        )
        opmDevices.grid(row=0, column=1, padx=PADDING, pady=PADDING)
        
    def addWidgetPicker(self, selected, addWin):
        if isSmartPlug(selected):
            self.plugWidgets(addWin)
        else:
            self.fridgeWidgets(addWin) 

    def plugWidgets(self, addWin):
        self.deleteAddWidgets()
        self.consumptionRate.set(0)

        lblRate = Label(addWin, text="Consumption Rate (0-150):")
        lblRate.grid(row=1, column=0, padx=PADDING, pady=PADDING)
        self.addWidgets.append(lblRate)

        entryRate = Entry(addWin, textvariable=self.consumptionRate)
        entryRate.grid(row=1, column=1, padx=PADDING, pady=PADDING)
        self.addWidgets.append(entryRate)

        btnAdd = Button(
            addWin,
            text="Add Device",
            command=lambda addWin=addWin: self.addPlug(addWin)
        )
        btnAdd.grid(row=2, column=1, padx=PADDING, pady=PADDING, columnspan=2)
        self.addWidgets.append(btnAdd)

    def addPlug(self, addWin):
        try:
            consumptionRate = self.consumptionRate.get()
            if 0 <= consumptionRate <= 150:
                self.homeDevices.addDevice(SmartPlug(consumptionRate))
        except TclError:
            self.errorMessage("digit")
            return None
        else:
            if consumptionRate < 0 or consumptionRate > 150:
                self.errorMessage("range")
                return None

        self.createWidgets()
        addWin.destroy()

    def fridgeWidgets(self, addWin):
        self.deleteAddWidgets()
        btnAdd = Button(
            addWin,
            text="Add Device",
            command=lambda: self.addFridge(addWin)
        )
        btnAdd.grid(row=1, column=1, padx=PADDING, pady=PADDING, columnspan=2)
        self.addWidgets.append(btnAdd)

    def addFridge(self, addWin):
        self.homeDevices.addDevice(SmartFridge())
        self.createWidgets()
        addWin.destroy()
    
    def deleteAddWidgets(self):
        for widget in self.addWidgets:
            widget.destroy()
        self.addWidgets = []

    def run(self):
        self.createWidgets()
        self.win.mainloop()

def main():
    smartHome = setUpHome()

    smartHomeSystem = SmartHomeSystem(smartHome)
    smartHomeSystem.run()

main()
