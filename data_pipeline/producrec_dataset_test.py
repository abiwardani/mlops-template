from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


conn_url = 'postgresql+psycopg2://sifa:sifa#2022!@database/sifa'

engine = create_engine(conn_url)

db = scoped_session(sessionmaker(bind=engine))


query_rows = db.execute(
    "SELECT * FROM nar.producrec_dataset_atl pda limit 10").fetchall()
for register in query_rows:
    print(f"{register.col_1_name}, {register.col_2_name}, ..., {register.col_n_name}")
    # Note that this Python way of printing is available in Python3 or more!!
