from communicator import Communicator

class FakeCommunicator(Communicator):
    def __init__(self):
        self.nextResponse = None
        self.responses = []
        self.lastCommand = None

    def getLastCommand(self):
        return self.lastCommand

    def query(self, command):
        self.lastCommand = command
        try:
            nr, self.responses = self.responses[0], self.responses[1:]
            return nr
        except IndexError:
            return None

    def setNextResponse(self, text):
        self.nextResponse = text
        self.responses += [text]

    def setResponses(self, responses):
        self.responses = responses
