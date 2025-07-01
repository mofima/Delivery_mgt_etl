import pandas as pd
import gspread 
import logging

from configs import GOOGLE_SHEET_NAME, SERVICE_ACCOUNT_PATH, SHEET_INDICES


# Set up logging
logging.basicConfig(
    filename='etl_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filemode='w'
)


def extract_data():
    logging.info("Starting data extraction")

    try:
        client = gspread.service_account(filename=SERVICE_ACCOUNT_PATH) 
        spreadsheet = client.open(GOOGLE_SHEET_NAME) 
        logging.info(f"Connected to Google Sheet: {GOOGLE_SHEET_NAME}")
    except Exception as e:
        logging.error(f"Failed to connect to Google Sheet: {e}")
        raise

    dataframes = {}
    for index in SHEET_INDICES:
        try:
            worksheet = spreadsheet.get_worksheet(index)
            data = worksheet.get_all_values()
            headers = data[0]
            rows = data[1:]
            df = pd.DataFrame(rows, columns=headers)
            sheet_name = worksheet.title.lower().replace(" ", "_")
            dataframes[sheet_name] = df
            logging.info(f"Extracted data from sheet: {worksheet.title} (rows: {len(df)})")
        except Exception as e:
            logging.error(f"Error extracting sheet at index {index}: {e}")
            continue

    logging.info("Data extraction completed")
    return dataframes