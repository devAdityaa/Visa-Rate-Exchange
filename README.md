# Visa-Rate-Exchange
A repo for converting currency rates from US Exchange Rate Calculator. 
***A project under Upwork, for Client: Albert***. 
# Exchange Rate Converter Script

This script reads currency exchange rates from an Excel sheet and fetches the corresponding conversion rates from US Exchange Rate Visa's Website, saving the results in a new sheet within the same Excel file.

## Features

- Reads an Excel file and extracts currency conversion details.
- Fetches the exchange rates from Visa's Website for the given date range.
- Mimics browser requests to bypass anti-bots and request blocking mechanisms.
- Saves the fetched rates into a new sheet within the same Excel file.
- Ensures that the original sheet remains unmodified.

## Prerequisites

- Python 3.x
- The following Python packages:
  - `requests`
  - `pandas`
  - `decouple`
  - `tqdm`
  - `openpyxl`

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/devAdityaa/Visa-Rate-Exchange.git
   cd Visa-Rate-Exchange

2. **Install Requirements**

   ```bash
   pip3 install -r requirements.txt

###Run the script
```bash
python3 WebRequest.py
```
Update the excelsheet with your own intended conversions. The outputs are saved in a different sheet in the same file ( default sheetname is Rates ).
