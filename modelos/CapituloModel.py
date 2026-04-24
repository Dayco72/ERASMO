from sqlmodel import Field, SQLModel

class CapituloModel(SQLModel, table=True):
    # Forzamos el nombre de la tabla tal cual aparece en tu Laragon
    __tablename__ = "capitulo"
    
    # Definimos las columnas según tu imagen
    cap_id: int | None = Field(default=None, primary_key=True)
    cap_nombre: str
    cap_duracion_sec: int
    cap_temp_id_fk: int = Field(foreign_key="temporada.temp_id") # Relación con temporada