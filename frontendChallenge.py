from backend import SmartPlug, SmartFridge, SmartHome
from tkinter import *

def setUpHome() -> SmartHome:
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

def checkDevice(device: str) -> bool:
    validInputs = ["smart plug", "plug", "smart fridge", "fridge"]
    if device.lower() in validInputs:
        return False
    else:
        print("Input is invalid, please choose from the available Smart Devices")
        return True

def isSmartPlug(device: str) -> bool:
    validInputs = ["smart plug", "plug"]
    if device.lower() in validInputs:
        return True
    
def smartPlugRate() -> int:
    while True:
        rate = input("Consumption rate: ")
        if not rate.isdigit():
            print("Input is not a number, please input a rate between 0 and 150")
        elif int(rate) < 0 or int(rate) > 150:
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

        self.homeDevices = homeDevices # SMART HOME OBJ
        self.homeDeviceWidgets = []

        # MAIN SCREEN
        self.deviceLabels = []
        self.consumptionRate = IntVar()
        self.consumptionRate.set(0)
        self.temperature = StringVar()

        # ADD SCREEN
        self.addWidgets = []
        self.newDevice = StringVar()

        # ICONS
        self.plug = PhotoImage(file='Challenge\plug.png')
        # self.plug = PhotoImage(file='plug.png')
        self.imgPlug = self.plug.subsample(15)

        self.fridge = PhotoImage(file=r'Challenge\fridge.png')
        # self.fridge = PhotoImage(file=r'fridge.png')
        self.imgFridge = self.fridge.subsample(15)
        
        self.power = PhotoImage(file='Challenge\power.png')
        # self.power = PhotoImage(file='power.png')
        self.imgPower = self.power.subsample(70)
        
        self.delete = PhotoImage(file='Challenge\delete.png')
        # self.delete = PhotoImage(file='delete.png')
        self.imgDelete = self.delete.subsample(70)

    def createWidgets(self):
        self.deleteAllHomeWidgets()
        self.deviceLabels = []

        deviceList = self.homeDevices.getDevices()

        btnOn = Button (
            self.mainFrame,
            text="Turn on all",
            width=25,
            command=self.turnOnAll
        )
        btnOn.grid(row=0, column=0, columnspan=2, padx=PADDING, pady=PADDING)

        btnOff = Button (
            self.mainFrame,
            text="Turn off all",
            width=25,
            command=self.turnOffAll
        )
        btnOff.grid(row=0, column=2, columnspan=3, padx=PADDING, pady=PADDING)

        for i, device in enumerate(deviceList, start=1):
            # ICONS
            if isinstance(device, SmartPlug):
                deviceIcon = self.imgPlug
            elif isinstance(device, SmartFridge):
                deviceIcon = self.imgFridge

            lblDeviceIcon = Label(
                self.mainFrame,
                image=deviceIcon
            )
            lblDeviceIcon.grid(row=i, column=0, padx=PADDING, pady=PADDING)
            self.homeDeviceWidgets.append(lblDeviceIcon)

            lblDeviceName = StringVar()
            self.setLabel(device, lblDeviceName)
            lblDevice = Label (
                self.mainFrame,
                width=25,
                textvariable=lblDeviceName
            )
            lblDevice.grid(row=i, column=1, padx=PADDING, pady=PADDING)
            self.deviceLabels.append(lblDeviceName)
            self.homeDeviceWidgets.append(lblDevice)

            btnToggle = Button (
                self.mainFrame, 
                text="Toggle", 
                image=self.imgPower,
                command=lambda index=i-1: self.btnToggleStatus(index)
            )
            btnToggle.grid(row=i, column=2, padx=PADDING, pady=PADDING)
            self.homeDeviceWidgets.append(btnToggle)

            if isinstance(device, SmartPlug):
                scaleRate = Scale(
                    self.mainFrame,
                    from_=0, 
                    to=150,
                    orient=HORIZONTAL,
                    variable=IntVar(),
                    length=150, 
                    command=lambda value, i=i-1: self.updateOption(i, value)
                )
                scaleRate.set(device.getConsumptionRate())
                scaleRate.grid(row=i, column=3, padx=PADDING, pady=PADDING) # CREATING SLIDER
                self.homeDeviceWidgets.append(scaleRate)

            elif isinstance(device, SmartFridge):
                deviceTemp = IntVar()
                deviceTemp.set(device.getTemperature())

                temps = [1, 3, 5]
                opmValue = OptionMenu(
                    self.mainFrame,
                    deviceTemp,
                    *temps,
                    command=lambda selected, i=i-1: self.updateOption(i, selected)
                )
                opmValue.grid(row=i, column=3, padx=PADDING, pady=PADDING) # CREATING OPTION MENU
                opmValue.config(width=18)
                self.homeDeviceWidgets.append(opmValue)

            btnDelete = Button (
                self.mainFrame, 
                text="Delete", 
                image=self.imgDelete,
                command=lambda index=i-1: self.deleteDevice(index)
            )
            btnDelete.grid(row=i, column=4, padx=PADDING, pady=PADDING)
            self.homeDeviceWidgets.append(btnDelete)

        btnAdd = Button (
            self.mainFrame,
            text="Add",
            width=25,
            command=self.addWin
        )
        btnAdd.grid(row=len(deviceList)+1, column=0, columnspan=2, padx=PADDING, pady=PADDING)
        self.homeDeviceWidgets.append(btnAdd)
        
    def deleteAllHomeWidgets(self): # RESETS WIDGETS
        for widget in self.homeDeviceWidgets:
            widget.destroy()
        self.homeDeviceWidgets = []

    # ========================================= LABEL =========================================
    def setLabel(self, device: object, label: Label): # SETS LABELS ON ROOT WIDGETS
        onOff = {True:"On", False:"Off"}        
        status = onOff[device.getSwitchedOn()]
        
        if isinstance(device, SmartPlug):
            self.consumptionRate.set(device.getConsumptionRate())
            label.set(f"Plug: {status}, Consumption: {self.consumptionRate.get()}")
        elif isinstance(device, SmartFridge):
            self.temperature.set(device.getTemperature())
            label.set(f"Fridge: {status}, Temperature: {self.temperature.get()}")

    # ========================================= TOGGLE BUTTONS =========================================
    def turnOnAll(self):
        self.homeDevices.turnOnAll()
        for i, device in enumerate(self.homeDevices.getDevices()):
            self.setLabel(device, self.deviceLabels[i])
    
    def turnOffAll(self):
        self.homeDevices.turnOffAll()
        for i, device in enumerate(self.homeDevices.getDevices()):
            self.setLabel(device, self.deviceLabels[i])

    def btnToggleStatus(self, index: int) -> None:
        self.homeDevices.toggleSwitch(index)
        self.setLabel(self.homeDevices.getDevicesAt(index), self.deviceLabels[index])
    
    # ========================================= UPDATE VALUE =========================================
    def updateOption(self, index: int, value: int) -> None:
        device = self.homeDevices.getDevicesAt(index)
        
        newValue = int(value)

        if isinstance(device, SmartPlug):
            device.setConsumptionRate(newValue)
        elif isinstance(device, SmartFridge):
            device.setTemperature(newValue)

        self.setLabel(device, self.deviceLabels[index])

    # ========================================= DELETE BUTTON =========================================
    def deleteDevice(self, index: int) -> None:
        self.homeDevices.removeDeviceAt(index)
        del self.deviceLabels[index]
        self.createWidgets()

    # ========================================= ADD BUTTON =========================================
    def addWin(self):
        newWin = Toplevel(self.win)
        newWin.title("Add Device")

        self.addWidgets = []
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
        
    def addWidgetPicker(self, selected: str, addWin: Toplevel) -> None:
        if isSmartPlug(selected):
            self.plugWidgets(addWin)
        else:
            self.fridgeWidgets(addWin) 

    def plugWidgets(self, addWin: Toplevel) -> None:
        self.deleteAddWidgets()

        addConsumptionRate = IntVar()
        addConsumptionRate.set(0)

        lblRate = Label(addWin, text="Consumption Rate:")
        lblRate.grid(row=1, column=0, padx=PADDING, pady=PADDING)
        self.addWidgets.append(lblRate)

        scaleRate = Scale(
            addWin,
            from_=0, 
            to=150,
            orient=HORIZONTAL,
            variable=addConsumptionRate,
            length=150,
            command=self.getSlider
        )
        scaleRate.grid(row=1, column=1, padx=PADDING, pady=PADDING)
        self.addWidgets.append(scaleRate)

        btnAdd = Button(
            addWin,
            text="Add Device",
            width=25,
            command=lambda addWin=addWin: self.addPlug(addWin)
        )
        btnAdd.grid(row=2, column=0, columnspan=2, padx=PADDING, pady=PADDING)
        self.addWidgets.append(btnAdd)
    
    def getSlider(self, value: IntVar) -> None:
        self.consumptionRate.set(int(value))
        
    def addPlug(self, addWin: Toplevel) -> None:        
        consumptionRate = self.consumptionRate.get()
        self.homeDevices.addDevice(SmartPlug(consumptionRate))

        self.createWidgets()
        addWin.destroy()

    def fridgeWidgets(self, addWin: Toplevel) -> None:
        self.deleteAddWidgets()

        btnAdd = Button(
            addWin,
            text="Add Device",
            command=lambda: self.addFridge(addWin)
        )
        btnAdd.grid(row=1, column=1, columnspan=2, padx=PADDING, pady=PADDING)
        self.addWidgets.append(btnAdd)

    def addFridge(self, addWin: Toplevel) -> None:
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
