import unittest
from unittest.mock import patch

from temp_sentry.__main__ import Contact, Zone


@patch('temp_sentry.__main__.W1ThermSensor')
class ZoneTestCase(unittest.TestCase):

    def setUp(self):
        """Instantiate a zone to test"""
        self.test_zone = Zone('test_zone', '12345', 33, 40)

    def test_temp_high(self, mock_sensor):
        """Test that check_temp_ok() returns false if the temperature is too
        high.

        """
        mock_sensor.return_value.get_temperature.return_value = 200
        self.assertFalse(self.test_zone.check_temp_ok())

    def test_temp_low(self, mock_sensor):
        """Test that check_temp_ok() returns false if the temperature is too
        low.

        """
        mock_sensor.return_value.get_temperature.return_value = -12
        self.assertFalse(self.test_zone.check_temp_ok())

    def test_temp_just_right(self, mock_sensor):
        """Test that check_temp_ok() returns true if the temperatrue is within
        the acceptable range.

        """
        mock_sensor.return_value.get_temperature.return_value = 36
        self.assertTrue(self.test_zone.check_temp_ok())

    def test_range_edge_inclusive(self, mock_sensor):
        """Test that temperatures on the edge of the acceptable range are
        considered ok.

        """
        mock_sensor.return_value.get_temperature.return_value = 33
        self.assertTrue(self.test_zone.check_temp_ok())

        mock_sensor.return_value.get_temperature.return_value = 40
        self.assertTrue(self.test_zone.check_temp_ok())

    def test_set_actual_temp(self, mock_sensor):
        """Test that the zone updates its current actual temp."""
        mock_sensor.return_value.get_temperature.return_value = 33
        self.test_zone.check_temp_ok()
        self.assertEqual(self.test_zone.actual_temp, 33)

        mock_sensor.return_value.get_temperature.return_value = 40
        self.test_zone.check_temp_ok()
        self.assertEqual(self.test_zone.actual_temp, 40)


@patch('temp_sentry.__main__.TwilioRestClient')
class ContactTestCase(unittest.TestCase):

    def setUp(self):
        """Instantiate a contact to test."""
        self.test_contact = Contact('+15553331234')

    def test_send_sms_alert(self, mock_twilio):
        """Test that an alert is sent to the contact's address."""
        self.test_contact.send_sms_alert('Test Zone', -32)

        self.assertEqual(mock_twilio.return_value.messages.create.call_args
                         [1]['to'], '+15553331234')


