import pandas as pd
import logging


def clean_dataframe(df):
    logging.info("Starting to clean a dataframe")
    try:
        # Convert empty strings to NaN
        df = df.replace(r'^\s*$', pd.NA, regex=True)
        # drop fully empty rows
        df = df.dropna(how='all')  
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.replace("'", "").str.strip()

        for col in df.columns:
            col_lower = col.lower()
            if 'date' in col_lower:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
            if 'id' in col_lower:
                df[col] = df[col].astype(str).str.strip()

        # Convert remaining NaN / NaT / pd.NA values to Python None
        df = df.where(pd.notnull(df), None)

        logging.info("Successfully cleaned dataframe")
        return df
    except Exception as e:
        logging.error(f"Error cleaning dataframe: {e}")
        raise

def transform_data(dfs: dict):
    logging.info("Starting transformation of all dataframes")

    transformed_dataframes = {}

    for sheet_name, df in dfs.items():
        try:
            logging.info(f"Cleaning sheet: {sheet_name} (rows: {len(df)})")
            cleaned_df = clean_dataframe(df)
            transformed_dataframes[sheet_name] = cleaned_df
        except Exception as e:
            logging.error(f"Error processing sheet '{sheet_name}': {e}")
            continue

    logging.info("Completed transformation for all sheets")
    return transformed_dataframes