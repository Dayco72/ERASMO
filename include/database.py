from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker

sql_url = "mysql+pymysql://root:@localhost:3306/series2"

engine=create_engine(sql_url,pool_recycle=3600,echo=True)

# Esta función es la que usarás en tus rutas
def get_session():
        with Session(engine) as session:
            yield session

