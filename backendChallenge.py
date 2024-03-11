onOff = {
    True: "On",
    False: "Off"
}

class SmartDevice:
    def __init__(self) -> None:
        self.switchedOn = False
    
    def toggleSwitch(self) -> None:
        self.switchedOn = not self.switchedOn
    
    def getSwitchedOn(self) -> bool:
        return self.switchedOn


class SmartPlug(SmartDevice):
    def __init__(self, consumptionRate: int) -> None:
        super().__init__()
        self.consumptionRate = consumptionRate

    def getConsumptionRate(self) -> int:
        return self.consumptionRate

    def setConsumptionRate(self, rate: int) -> None:
        if 0 <= rate <= 150:
            self.consumptionRate = rate

    def __str__(self) -> str:        
        output = f"Plug: {onOff[self.switchedOn]}, Consumption: {self.getConsumptionRate()}"
        return output

def testSmartPlug():
    plug = SmartPlug(45)
    plug.toggleSwitch()
    print(plug.getSwitchedOn())

    print(plug.getConsumptionRate())
    plug.setConsumptionRate(30)
    print(plug.getConsumptionRate())
    print(plug)
# testSmartPlug()
    

# student no.1
# smartfridge
# temperatures: 1, 3, 5 (C) -> default = 3

class SmartFridge(SmartDevice):
    def __init__(self) -> None:
        super().__init__()
        self.temperature = 3

    def getTemperature(self) -> int:
        return self.temperature

    def setTemperature(self, temperature: int) -> None:
        temps = [1, 3, 5]
        if temperature in temps:
            self.temperature = temperature

    def __str__(self) -> str:
        output = f"Fridge: {onOff[self.switchedOn]}, Temperature: {self.getTemperature()}"#°C"
        return output

def testDevice():
    fridge = SmartFridge()
    fridge.toggleSwitch()
    print(fridge.getSwitchedOn())

    print(fridge.getTemperature())
    fridge.setTemperature(5)
    print(fridge.getTemperature())

    print(fridge)
# testDevice()

class SmartHome:
    def __init__(self) -> None:
        self.devices = []

    def getDevices(self) -> list:
        return self.devices

    def getDevicesAt(self, index: int) -> str:
        return self.devices[index]
    
    def removeDeviceAt(self, index: int) -> None:
        self.devices.remove(self.devices[index])

    def addDevice(self, device: object) -> None:
        self.devices.append(device)

    def toggleSwitch(self, index: int) -> None:
        device = self.devices[index]
        device.toggleSwitch()

    def turnOnAll(self) -> None:
        for device in self.devices:
            if not device.getSwitchedOn():
                device.toggleSwitch()

    def turnOffAll(self) -> None:
        for device in self.devices:
            if device.getSwitchedOn():
                device.toggleSwitch()

    def __str__(self) -> str:
        output = "Smart Home Devices:\n"
        for device in self.devices:
            output += f"{str(device)}\n"
        return output[:-1]

def testSmartHome():
    smartHome = SmartHome()
    plug1 = SmartPlug(45)
    plug2 = SmartPlug(45)
    fridge = SmartFridge()

    plug1.toggleSwitch()
    plug1.setConsumptionRate(150)
    plug2.setConsumptionRate(25)
    fridge.setTemperature(6) # should not change

    smartHome.addDevice(plug1)
    smartHome.addDevice(plug2)
    smartHome.addDevice(fridge)

    # print(smartHome)

    # print("\n turn all on\n")
    # smartHome.turnOnAll()
    # print(smartHome)

    # print("\n turn all off\n")
    # smartHome.turnOffAll()
    # print(smartHome)

    print(smartHome.getDevicesAt(2))
# testSmartHome()
