import psycopg2 
from psycopg2.extras import execute_values
import pandas as pd
import logging 

from configs import DB_CONFIG, TABLE_LOAD_ORDER

# Set up logging
# logging.basicConfig(
#     filename='load.log',
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     filemode='w'  
# )

def get_connection():
    try:
        logging.info("Establishing database connection...")
        conn = psycopg2.connect(
            dbname=DB_CONFIG['dbname'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port']
        )
        logging.info("Database connection established.")
        return conn
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        raise

def get_existing_ids(conn, table_name, id_column='id'):
    with conn.cursor() as cur:
        cur.execute(f"SELECT {id_column} FROM {table_name} WHERE is_deleted = FALSE")
        return set(row[0] for row in cur.fetchall())

def mark_as_deleted(conn, table_name, deleted_ids, id_column='id'):
    if not deleted_ids:
        return
    with conn.cursor() as cur:
        cur.executemany(
            f"UPDATE {table_name} SET is_deleted = TRUE WHERE {id_column} = %s",
            [(id_,) for id_ in deleted_ids]
        )
    conn.commit()

def reactivate_existing_records(conn, table_name, reappeared_ids, id_column='id'):
    if not reappeared_ids:
        return
    with conn.cursor() as cur:
        cur.executemany(
            f"UPDATE {table_name} SET is_deleted = FALSE WHERE {id_column} = %s",
            [(id_,) for id_ in reappeared_ids]
        )
    conn.commit()

def upsert_to_postgres(df, table_name, conflict_col, conn):
    try:
        logging.info(f"Starting upsert into table: {table_name} (rows: {len(df)})")

        columns = list(df.columns)
        if 'is_deleted' not in columns:
            df['is_deleted'] = False
            columns.append('is_deleted')

        values = [tuple(x) for x in df.to_numpy()] 

        insert_statement = f""" 
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES %s
        ON CONFLICT ({conflict_col}) DO UPDATE SET 
        {', '.join([f"{col}=EXCLUDED.{col}" for col in columns if col != conflict_col])};
        """ 

        with conn.cursor() as cur:
            execute_values(cur, insert_statement, values)
            conn.commit()

        logging.info(f"Successfully upserted data into table: {table_name}")
    
    except Exception as e:
        conn.rollback()
        logging.error(f"Error while upserting to table {table_name}: {e}")
        raise

def load_all(dfs_dict):
    conn = get_connection()
    logging.info("Database connection established.")

    for table_name in TABLE_LOAD_ORDER:
        if table_name in dfs_dict:
            df = dfs_dict[table_name]
            logging.info(f"Loading sheet: {table_name}")

            # Ensure id is string and cleaned
            if 'id' in df.columns:
                df['id'] = df['id'].astype(str).str.strip()
            else:
                logging.warning(f"Skipping table {table_name}: 'id' column missing.")
                continue

            current_ids = set(df['id'].dropna())
            existing_ids = get_existing_ids(conn, table_name)
            deleted_ids = existing_ids - current_ids
            reappeared_ids = current_ids & existing_ids

            mark_as_deleted(conn, table_name, deleted_ids)
            reactivate_existing_records(conn, table_name, reappeared_ids)
            logging.info(f"Soft-deleted {len(deleted_ids)} rows in table: {table_name}")

            try:
                upsert_to_postgres(df, table_name, conflict_col='id', conn=conn)
                logging.info(f"Finished upsert into table: {table_name}")
            except Exception as e:
                logging.error(f"Error while upserting to table {table_name}: {e}")

    conn.close()
    logging.info("Database connection closed.")
