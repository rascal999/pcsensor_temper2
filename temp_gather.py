#!/usr/bin/env python3

from __future__ import print_function
from oauth2client.client import GoogleCredentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
from googleapiclient import discovery
from evdev import InputDevice, categorize

import argparse
import datetime
import evdev
import pickle
import os
import os.path
import sys

def main():
    parser = argparse.ArgumentParser(description="Take temperature from HID " + 
                                                 "and push to Drive spreadsheet")
    parser.add_argument("--device-id", required=True,
                        help="Device input to read (e.g. input1)")
    parser.add_argument("--spreadsheet-id", required=True,
                        help="Spreadsheet ID to push data to")
    parser.add_argument("--interval", default=900, type=int,
                        help="How often to push data to spreadsheet (seconds)")

    parsed = parser.parse_args()

    read_input(parsed)

def read_input(parsed):
    dev = InputDevice('/dev/input/' + parsed.device_id)

    scancodes = {
            # Scancode: ASCIICode
            0: '', 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
            10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u' ', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
            20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'\n', 29: u'LCTRL',
            30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
            40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
            50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }

    temp = []
    count = 0

    for event in dev.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            data = evdev.categorize(event)  # Save the event temporarily to introspect it
            if data.keystate == 1:  # Down events only
                key_lookup = scancodes.get(data.scancode)
                if key_lookup == None:
                    continue
                # Variable should be values until \n
                if key_lookup == '\n':
                    raw_values = ''.join(temp)
                    # Newline hit, send to process def
                    count = process(raw_values,parsed,count)
                    # Reset list
                    temp = []
                else:
                    # If not newline, then append to list
                    temp.append(key_lookup)

# This def will selectively submit to the spreadsheet
# depending on count, which roughly equates to seconds.
# Most of the data is discarded, but could be averaged in
# future.
def process(raw_values,parsed,count):
    # Sometimes we get garbage, so search string for [C]
    if "[C]" in raw_values:
        temperature = str(raw_values.split()[1])
        temperature_float = temperature.replace("[C]","") # Float only
        count = count + 1 # Device triggers every second
        if count > parsed.interval: # Device hit greater than count?
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Current date
            push_to_spreadsheet(parsed,temperature_float,now) # Push data to spreadsheet
            count = 0
    return count

# Push data to spreadsheet
def push_to_spreadsheet(parsed,temperature,now):
    #print(temperature)

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = parsed.spreadsheet_id # '1TipIc59G52RlfTNR6NqBsMeh_i48_-ITg8fm0bW9qAI'
    SAMPLE_RANGE_NAME = 'Sheet1!A1:B'

    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            # Listens on TCP port on loopback interface
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    list = [[temperature,now]]
    resource = {
        "majorDimension": "ROWS",
        "values": list
    }

    try:
       range = "Sheet1!A1:A";
       service.spreadsheets().values().append(
           spreadsheetId=parsed.spreadsheet_id,
           range=range,
           body=resource,
           valueInputOption="USER_ENTERED"
       ).execute()
    except:
       pass

if __name__ == "__main__":
    main()
