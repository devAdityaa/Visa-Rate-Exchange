import requests
from datetime import datetime, timedelta
import pandas as pd
import logging
import sys
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def browse_initial_sites(session, headers):
    logging.info("Starting initial site browsing.")
    sites = [
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.github.com"
    ]
    for site in sites:
        try:
            session.get(site, headers=headers)
            logging.info(f"Browsed site: {site}")
        except requests.RequestException as e:
            logging.error(f"Error browsing site {site}: {e}")

def get_conversion_rate(fromCurrency, toCurrency, day):
    url = "https://usa.visa.com/cmsapi/fx/rates"
    params = {
        'amount': '1',
        'fee': '2',
        'utcConvertedDate': day,
        'exchangedate': day,
        'fromCurr': fromCurrency,
        'toCurr': toCurrency
    }

    headers.update({
        'Referer': 'https://usa.visa.com/support/consumer/travel-support/exchange-rate-calculator.html',
    })

    try:
        response = session.get(url, headers=headers, params=params)
        response.raise_for_status()
        res = response.json()
        return res["convertedAmount"]
    except requests.RequestException as e:
        logging.error(f"Error fetching conversion rate: {e}")
    return None

def read_excel_file(file_path, sheet_name):
    logging.info(f"Reading Excel file: {file_path}, sheet: {sheet_name}.")
    try:
        return pd.read_excel(file_path, sheet_name=sheet_name)
    except Exception as e:
        logging.error(f"Error reading Excel file: {e}")
        raise

def validate_columns(df, required_columns):
    logging.info("Validating columns in the Excel file.")
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logging.error(f"Missing columns in Excel file: {missing_columns}")
        raise ValueError(f"Missing columns: {missing_columns}")
    return df.astype(str)

def save_rates_to_excel(file_path, rates_df, sheet_name, mode='a'):
    try:
        with pd.ExcelWriter(file_path, mode=mode, engine='openpyxl', if_sheet_exists='replace') as writer:
            rates_df.to_excel(writer, sheet_name=sheet_name, index=False)
    except Exception as e:
        logging.error(f"Error saving to Excel file: {e}")

def update_excel_with_products(file_path, sheet_name, output_sheet_name):
    lead_sheet = read_excel_file(file_path, sheet_name)
    required_columns = ["FromCurrency", "ToCurrency", "FromDate", "ToDate"]
    lead_sheet = validate_columns(lead_sheet, required_columns)

    # Convert dates in the 'FromDate' and 'ToDate' columns
    lead_sheet["FromDate"] = pd.to_datetime(lead_sheet["FromDate"], errors='coerce')
    lead_sheet["ToDate"] = pd.to_datetime(lead_sheet["ToDate"], errors='coerce')

    # Extract the fromDate and toDate from the first row
    fromDate = lead_sheet.at[0, "FromDate"]
    toDate = lead_sheet.at[0, "ToDate"]

    if pd.isna(fromDate) or pd.isna(toDate):
        logging.error("FromDate or ToDate in the first row is invalid.")
        raise ValueError("FromDate or ToDate in the first row is invalid.")

    browse_initial_sites(session, headers)

    rates_data = []

    total_rows = len(lead_sheet)
    with tqdm(total=total_rows, file=sys.stdout, desc="Processing rows") as pbar:
        for index, row in lead_sheet.iterrows():
            try:
                fromCurrency = row["FromCurrency"]
                toCurrency = row["ToCurrency"]

                if fromCurrency and toCurrency and (fromCurrency != toCurrency):
                    logging.info(f"Fetching conversion rates for {fromCurrency} to {toCurrency}")
                    currentDate = fromDate
                    while currentDate <= toDate:
                        rate = get_conversion_rate(fromCurrency, toCurrency, currentDate.strftime('%m/%d/%Y'))
                        if rate is not None:
                            rate_entry = {
                                'FromCurrency': fromCurrency,
                                'ToCurrency': toCurrency,
                                'Date': currentDate.strftime('%Y-%m-%d'),
                                'Rate': rate
                            }
                            rates_data.append(rate_entry)

                            # Save incrementally after every 100 entries
                            if len(rates_data) % 100 == 0:
                                rates_df = pd.DataFrame(rates_data)
                                save_rates_to_excel(file_path, rates_df, output_sheet_name, mode='a')
                    
                        currentDate += timedelta(days=1)
                pbar.update(1)
                rates_df = pd.DataFrame(rates_data)
                save_rates_to_excel(file_path, rates_df, output_sheet_name, mode='a')
            except Exception as e:
                logging.error(f"Error processing row {index}: {e}")

        if rates_data:
            rates_df = pd.DataFrame(rates_data)
            save_rates_to_excel(file_path, rates_df, output_sheet_name, mode='a')
            logging.info(f"Excel file updated successfully. Saved to {file_path}")

if __name__ == "__main__":
    update_excel_with_products(
        file_path='./sheetgit .xlsx',
        sheet_name='Sheet1',
        output_sheet_name='Rates'
    )
