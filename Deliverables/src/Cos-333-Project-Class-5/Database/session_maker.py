from sqlalchemy.orm import sessionmaker
from Database.configs import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
from sqlalchemy import create_engine

connect_stmt = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(connect_stmt)
Session = sessionmaker(bind=engine)