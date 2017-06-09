import fakeCommunicator
import communicator
import InncoTurnTable
import unittest

from unittest.mock import *


class FakeCommTests(unittest.TestCase):
    def setUp(self):
        self.fc = fakeCommunicator.FakeCommunicator()

    def test_that_commands_are_stored(self):
        fc = self.fc
        fc.query("the command")
        last = fc.getLastCommand()
        self.assertEqual(last, "the command")

    def test_that_next_response_can_be_set(self):
        fc = self.fc
        fc.setNextResponse("the response")
        actual = fc.query("the command")
        self.assertEqual(actual, "the response")

    def test_that_responses_are_queued(self):
        fc = self.fc
        fc.setResponses(["one", "two", "three"])
        actuals = [fc.query("the command") for dummy in [1, 2, 3]]
        self.assertEqual(actuals, ["one", "two", "three"])

    def test_that_commands_can_be_queued(self):
        fc = self.fc
        resps = ["one", "two", "three"]
        fc.setResponses(resps)
        actuals = [fc.query("the command"),
                   fc.query("the command"),
                   fc.query("the command")]
        self.assertEqual(actuals, ["one", "two", "three"])


class InncoDevicesTests(unittest.TestCase):
    def setUp(self):
        self.fc = fakeCommunicator.FakeCommunicator()
        self.tt = InncoTurnTable.InncoTurnTable()
        self.tt.setCommunicator(self.fc)

    def test_that_command_is_opt(self):
        fc = self.fc
        tt = self.tt
        fc.setNextResponse("don't care")

        tt.getDevices()
        command = fc.getLastCommand()
        self.assertEqual(command, "*OPT?")

    def test_that_parts_are_right(self):
        fc = self.fc
        tt = self.tt
        fc.setNextResponse("MA1, DT1, 0, 0, X1")

        response = tt.getDevices()
        expected = ["MA1", "DT1", "X1"]
        self.assertEqual(response, expected)

        # Jag är inte så säker på att det är så här Devices ska behandlas.
        # Kanske vi ska ha ett objekt för varje Device.
        # TODO: förstå devices.

    def test_that_devices_are_stored(self):
        fc = self.fc
        tt = self.tt
        fc.setNextResponse("MA1, DT1, 0, 0, X1")


        response = tt.getDevicesDict()
        expected = {"MA1": 0, "DT1": 1, "X1": 4}
        self.assertEqual(response, expected)


class InncoIdnTests(unittest.TestCase):
    def setUp(self):
        self.fc = fakeCommunicator.FakeCommunicator()
        self.tt = InncoTurnTable.InncoTurnTable()
        self.tt.setCommunicator(self.fc)

    def test_that_command_is_idn(self):
        fc = self.fc
        tt = self.tt
        fc.setNextResponse("don't care")
        tt.getIdentification()
        command = fc.getLastCommand()
        self.assertEqual(command, "*IDN?")

    def test_using_mock(self):
        fc = self.fc
        tt = self.tt
        query = MagicMock()
        fc.query = query
        tt.getIdentification()
        query.assert_called_once_with('*IDN?')

    def test_that_parts_are_right(self):
        fc = self.fc
        tt = self.tt
        fc.setNextResponse("inncoCO3000/serial/version")

        response = tt.getIdentification()
        self.assertEqual(response, ("inncoCO3000", "serial", "version"))


class InncoBUTests(unittest.TestCase):
    def setUp(self):
        self.fc = fakeCommunicator.FakeCommunicator()
        self.tt = InncoTurnTable.InncoTurnTable()
        self.tt.setCommunicator(self.fc)


    def test_that_command_is_BU(self):
        fc = self.fc
        tt = self.tt
        fc.setNextResponse("0")  # to avoid exception
        tt.isBusy()
        command = fc.getLastCommand()
        self.assertEqual(command, "BU")

    def test_that_one_is_on_is_busy(self):
        fc = self.fc
        tt = self.tt
        fc.setNextResponse("1")
        self.assertEqual(tt.isBusy(), True)

    def test_that_zero_is_off_is_non_busy(self):
        fc = self.fc
        tt = self.tt
        fc.setNextResponse("0")
        self.assertEqual(tt.isBusy(), False)

    def test_that_other_responses_raies_exception(self):
        fc = self.fc
        tt = self.tt
        fc.setNextResponse("wrong")
        self.assertRaises(Exception, tt.isBusy)


if __name__ == '__main__':
    unittest.main()
