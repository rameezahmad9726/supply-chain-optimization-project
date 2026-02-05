import pandas as pd
from sqlalchemy import create_engine

# 1. Setup the connection (Keep your working settings!)
db_connection_str = 'mysql+mysqlconnector://root:1234@127.0.0.1/SupplyChain'
db_connection = create_engine(db_connection_str)

# 2. Read the CSV file
csv_file_path = r"C:\Users\RAMEEZ\Desktop\SqlDataImport\DataCoSupplyChainDataset.csv"
df = pd.read_csv(csv_file_path, encoding='latin-1')

# 3. Clean column names
df.columns = [c.replace(' ', '_').replace('(', '').replace(')', '').lower() for c in df.columns]

# 4. Upload to MySQL in CHUNKS
print(f"Starting upload of {len(df)} rows...")

try:
    with db_connection.begin() as connection:
        # chunksize=1000 means "send 1000 rows, wait for OK, then send next 1000"
        df.to_sql(name='raw_supply_chain_data', con=connection, if_exists='replace', index=False, chunksize=1000)
    print("Upload complete! Check MySQL Workbench now.")
except Exception as e:
    print(f"An error occurred: {e}")