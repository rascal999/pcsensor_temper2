# pcsensor_temper2

Script which pushes temperature sensor data to Google spreadsheet

## Getting Started

1. Connect your sensor and find out what input it is (``xinput``)

2. Run spreadsheet push every 15 minutes with:

``./temp_gather.py --device-id event12 --spreadsheet-id 1TipIc59G52RlfTNR6NqBsMeh_i48_-ITg8fm0bW9qAI --interval 900``

You will need the ``credentials.json`` file, which you can generate from https://developers.google.com/sheets/api/quickstart/python

### Installing

```
git clone https://github.com/rascal999/pcsensor_temper2
cd pcsensor_temper2
pip install -r requirements.txt
./temp_gather.py --help
```

You should see something like:

```
usage: temp_gather.py [-h] --device-id DEVICE_ID --spreadsheet-id
                      SPREADSHEET_ID [--interval INTERVAL]

Take temperature from HID and push to Drive spreadsheet

optional arguments:
  -h, --help            show this help message and exit
  --device-id DEVICE_ID
                        Device input to read (e.g. input1)
  --spreadsheet-id SPREADSHEET_ID
                        Spreadsheet ID to push data to
  --interval INTERVAL   How often to push data to spreadsheet (seconds)
```

## Built With

* [Python3](https://www.python.org/) - Python Programming Language.

## Contributing

Subtmit a PR for consideration.

## Authors

* **Aidan Marlin** - *Initial work* - [Rascal999](https://github.com/rascal999)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
