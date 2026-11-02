import pandas as pd
import os
import logging
import time
from sqlalchemy import create_engine

logging.basicConfig(
    filename='ingestion.log',
    # logs.ingestion.db is a log file despite its .db extension. Consider naming it ingestion.log to avoid confusion.
    level=logging.INFO,
    # logging.INFO is the logging threshold; logging.info() writes a message.
    format="%(asctime)s-%(levelname)s-%(message)s",
    filemode='a')

engine=create_engine('sqlite:///sales_customer.db')





def ingest_db(df,table_name,engine):
    df.to_sql(table_name,con=engine,if_exists='replace',index=False)
    # logs.ingestion.db is a log file despite its .db extension. Consider naming it ingestion.log to avoid confusion.
    # replace: Recreates the table and replaces its data.
    # append: Adds rows to an existing table.
    # fail: Raises an error if the table already exists.

def load_raw_data():
    dataset_path=r'F:\Projects\E-commerce Sales and Customer Satisfaction Analysis\dataset'
    files=os.listdir(dataset_path)
    # The r makes it a raw string. coz slashes can be escape characters in some cases

    start=time.time()    
    for file in files:
        if file.lower().endswith('.csv'):
            # file.endswith('.csv') checks that the filename ends with .csv.
            # else people.csv.backup will also allowed

            df=pd.read_csv(os.path.join(dataset_path,file))
            # os.path.join() builds the correct file path.
            
            logging.info(f'ingesting {file} into db')
            ingest_db(df,file[:-4],engine)
    
    end=time.time()
    logging.info('-------------------ingestion completed-------------------')
    total=(end-start)/60
    logging.info(f'total time for ingestion {total} minutes')   
    
if __name__=='__main__':
    load_raw_data() 
