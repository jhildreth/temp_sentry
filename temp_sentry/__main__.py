import json
import os

from twilio.rest import TwilioRestClient
from w1thermsensor import W1ThermSensor


class Zone:

    def __init__(self, name, sensor_id, min_temp, max_temp):
        self.name = name
        self.actual_temp = None
        self._sensor_id = sensor_id
        self._min_temp = min_temp
        self._max_temp = max_temp

    def check_temp_ok(self):
        """Check if the temperature is within the acceptable range."""
        sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20,
                               self._sensor_id)
        self.actual_temp = sensor.get_temperature(W1ThermSensor.DEGREES_F)
        self.actual_temp = round(self.actual_temp, 2)

        if not self._min_temp <= self.actual_temp <= self._max_temp:
            return False

        return True


class Contact:

    def __init__(self, phone):
        self._phone = phone

    def send_sms_alert(self, zone, temp):
        """Send a text message alert to the contact."""
        message = '{} temp of {} is outside the acceptable range.'.format(zone,
                                                                          temp)

        twilio_client = TwilioRestClient()
        twilio_client.messages.create(to=self._phone,
                                      from_='+{}'.format(
                                          os.environ.get('TS_SENDING_NUMBER')),
                                      body=message)


def main():
    zones_file = os.environ.get('TS_ZONES_FILE')
    with open(zones_file, 'r') as zf:
        zones = json.load(zf)

    contacts_file = os.environ.get('TS_CONTACTS_FILE')
    with open(contacts_file, 'r') as cf:
        contacts = json.load(cf)

    for zone in zones:
        checked_zone = Zone(zone['name'], zone['sensor_id'],
                            zone['min_temp'], zone['max_temp'])
        if not checked_zone.check_temp_ok():
            for contact in contacts:
                Contact(
                    contact['phone']).send_sms_alert(checked_zone.name,
                                                     checked_zone.actual_temp)


if __name__ == '__main__':
    main()
