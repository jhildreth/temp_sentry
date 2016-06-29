# README #
Temp Sentry is a program designed to run on a Raspberry Pi, with one or more DS18B20 sensors. It can be run periodically via cron, and will notify contacts if a zone registers a temperature that is outside of the acceptable range.

## Requirements ##
* A Raspberry Pi
* One or more attached DS18B20 temperature sensors
* A Twilio account is required for SMS notification

## Setup ##

* Install the package
> sudo python3 setup.py install
* Modify the contacts.sample.json and zones.sample.json files to represent the zones you would like to monitor, and the contacts that should be alerted.
* Set the following environment variables:
    * TWILIO_ACCOUNT_SID - Your Twilio account id
    * TWILIO_AUTH_TOKEN - Your Twilio auth token
    * TS_SENDING_NUMBER - The number Twilio will use to send SMS notifications
    * TS_ZONES_FILE - Location of the file that defines your zones
    * TS_CONTACTS_FILE - Location of the file that defines your contacts
* Configure cron to run temp_sentry periodically, at whatever interval you would like
