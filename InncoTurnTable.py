import turnTable

class InncoTurnTable(turnTable.TurnTable):
    def setCommunicator(self, c):
        self.communicator = c

    def isBusy(self):
        response = self.communicator.query("BU")
        if not response in ["0", "1"]:
            raise Exception
        return response == "1"

    def getIdentification(self):
        response = self.communicator.query("*IDN?")
        return tuple(response.split('/'))

    def getDevices(self):
        response = self.communicator.query("*OPT?")
        cs =  [c.strip() for c in response.split(",")]
        return [c for c in cs if c != '0']

    def getDevicesDict(self):
        "Save comma-separated devices along with their position in the list in a dict. 0 marks 'no device'."
        response = self.communicator.query("*OPT?")
        devices = [c.strip() for c in response.split(",")]
        devdict = {}
        for device in enumerate(devices):
            if device[1] != '0':
                dname = device[1]
                devdict[dname] = device[0]

        return devdict
