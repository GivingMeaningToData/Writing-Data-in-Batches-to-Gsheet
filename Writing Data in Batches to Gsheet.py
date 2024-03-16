#!/usr/bin/env python
# coding: utf-8

# In[1]:

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# Set your credentials and scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/ubuntu/Crons/business-reporting-297220-1bd8456f1dda.json', scope)

# Authorize the client
gc = gspread.authorize(credentials)
client = gspread.authorize(credentials)

# Define the Google Sheets details
spreadsheetId = '19S3VHNKyUqH5zSrZ6wtalpFqMvY45mzDR4H0pL53R1s'  # Please set your spreadsheet ID.
sheetName = "Raw" # Please set the sheet name you want to put the CSV data.

# Define the CSV file details
csvFile = 'MARKETING_DAILY_REPORT_Test_GK.csv'  # Please set the filename and path of the CSV file.

# Open the Google Sheet
sh = client.open_by_key(spreadsheetId)

# Clear data in the specified range
sh.values_clear(f"'{sheetName}'!A:AR")
print("Data cleared")

# Read the CSV file in batches
batch_size = 50000  # Define your batch size (e.g., 10000 rows per batch)
start_row=2

# Read the CSV file and write in a batch
with open(csvFile, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    batch = []
    sheet_index = 1  # Initialize the sheet index
    sheetName = f"Raw!A{sheet_index}"  # Initialize the sheetName
    
    for row in csv_reader:
        batch.append(row)
        if len(batch) >= batch_size:
            sh.values_update(
                sheetName,
                params={'valueInputOption': 'USER_ENTERED'},
                body={'values': batch},
            )
            print(f"Batch of {batch_size} rows written starting from row {start_row}")
            start_row += batch_size
            sheet_index += batch_size  # Increment the sheet index
            sheetName = f"Raw!A{sheet_index}"  # Update the sheetName
            batch = []  # Reset batch
    if batch:
        sh.values_update(
            sheetName,
            params={'valueInputOption': 'USER_ENTERED'},
            body={'values': batch},
        )
        print(f"Remaining rows written starting from row {start_row}")

print("All rows written")

