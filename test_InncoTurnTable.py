import fakeCommunicator
import communicator
import InncoTurnTable
import unittest

from unittest.mock import *

class FakeCommTests(unittest.TestCase):
    def testThatCommandsAreStored(self):
        fc = fakeCommunicator.FakeCommunicator()
        fc.query("the command")
        last = fc.getLastCommand()
        self.assertEqual(last, "the command")

    def testThatNextResponseCanBeSet(self):
        fc = fakeCommunicator.FakeCommunicator()
        fc.setNextResponse("the response")
        actual = fc.query("the command")
        self.assertEqual(actual, "the response")

    def testThatResponsesAreQueued(self):
        fc = fakeCommunicator.FakeCommunicator()
        fc.setResponses(["one", "two", "three"])
        actuals = [fc.query("the command") for dummy in [1, 2, 3]]
        self.assertEqual(actuals, ["one", "two", "three"])
        pass

    def testThatCommandsCanBeQueued(self):
        fc = fakeCommunicator.FakeCommunicator()
        resps = ["one", "two", "three"]
        fc.setResponses(resps)
        actuals = [fc.query("the command") for dummy in resps]
        self.assertEqual(actuals, ["one", "two", "three"])
        pass


class InncoDevicesTests(unittest.TestCase):

    def testThatCommandIsOpt(self):
        fc = fakeCommunicator.FakeCommunicator()
        fc.setNextResponse("don't care")

        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(fc)

        tt.getDevices()
        command = fc.getLastCommand()
        self.assertEqual(command, "*OPT?")

    def testThatPartsAreRight(self):
        fc = fakeCommunicator.FakeCommunicator()
        fc.setNextResponse("MA1, DT1, 0, 0, X1")

        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(fc)

        response = tt.getDevices()
        expected = ["MA1", "DT1", "X1"]
        self.assertEqual(response, expected)

        # Jag är inte så säker på att det är så här Devices ska behandlas.
        # Kanske vi ska ha ett objekt för varje Device.
        # TODO: förstå devices.

    def testThatDevicesAreStored(self):
        fc = fakeCommunicator.FakeCommunicator()
        fc.setNextResponse("MA1, DT1, 0, 0, X1")

        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(fc)

        response = tt.getDevicesDict()
        expected = {"MA1": 0, "DT1": 1, "X1": 4}
        self.assertEqual(response, expected)


class InncoIdnTests(unittest.TestCase):

    def testThatCommandIsIdn(self):
        fc = fakeCommunicator.FakeCommunicator()
        fc.setNextResponse("don't care")
        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(fc)
        tt.getIdentification()
        command = fc.getLastCommand()
        self.assertEqual(command, "*IDN?")

    def testUsingMock(self):
        c = communicator.Communicator()
        c.query = MagicMock(name='query')
        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(c)
        tt.getIdentification()
        c.query.assert_called_once_with(12)

    def testThatPartsAreRight(self):
        fc = fakeCommunicator.FakeCommunicator()
        fc.setNextResponse("inncoCO3000/serial/version")
        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(fc)

        response = tt.getIdentification()
        self.assertEqual(response, ("inncoCO3000", "serial", "version"))


class InncoBUTests(unittest.TestCase):

    def testThatCommandIsBU(self):
        fc = fakeCommunicator.FakeCommunicator()
        fc.setNextResponse("0")  # to avoid exception
        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(fc)
        tt.isBusy()
        command = fc.getLastCommand()
        self.assertEqual(command, "BU")

    def testThatOneIsOnIsBusy(self):
        fc = fakeCommunicator.FakeCommunicator()
        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(fc)
        fc.setNextResponse("1")
        self.assertEqual(tt.isBusy(), True)

    def testThatZeroIsOffIsNonBusy(self):
        fc = fakeCommunicator.FakeCommunicator()
        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(fc)
        fc.setNextResponse("0")
        self.assertEqual(tt.isBusy(), False)

    def testThatOtherResponsesRaiesException(self):
        fc = fakeCommunicator.FakeCommunicator()
        tt = InncoTurnTable.InncoTurnTable()
        tt.setCommunicator(fc)
        fc.setNextResponse("wrong")
        self.assertRaises(Exception, tt.isBusy)


if __name__ == '__main__':
    unittest.main()
