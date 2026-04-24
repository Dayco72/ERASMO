from sqlmodel import Field, SQLModel
from datetime import date

class SerieModel(SQLModel, table = True):
    __tablename__ = "serie"
    ser_id: int | None = Field(default=None, primary_key=True)
    ser_nombre: str
    ser_fecha_ini: date
    ser_fecha_fin : date