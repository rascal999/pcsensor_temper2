# pcsensor_temper2
Script which pushes temperature sensor data to spreadsheet

Connect your sensor and find out what input it is (``xinput``)

Run spreadsheet push every 15 minutes with:

``./temp_gather.py --device-id event12 --interval 900``
