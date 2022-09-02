from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import experiment.ml_pipeline_config as config

conn_url = 'postgresql+psycopg2://sifa:sifa#2022!@database/sifa'
host_engine = create_engine(conn_url)
host_db = scoped_session(sessionmaker(bind=host_engine))

postgres_engine = config.params["db_engine"]
postgres_schema = config.params["db_schema"]

query_rows = host_db.execute("SELECT entry_value")

query_rows = host_db.execute(
    "SELECT * FROM nar.producrec_dataset_atl pda limit 10").fetchall()
for register in query_rows:
    print(f"{register.col_1_name}, {register.col_2_name}, ..., {register.col_n_name}")
    # Note that this Python way of printing is available in Python3 or more!!
