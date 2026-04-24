from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from include.database import get_session, engine

# 1. IMPORTACIÓN CORREGIDA: Usamos SerieModel que es el nombre real de tu clase
from modelos.SerieModel import SerieModel
from modelos.CapituloModel import CapituloModel 

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- RUTAS DE SERIES ---

@app.get("/series", response_class=HTMLResponse)
def listar_series(request: Request, session: Session = Depends(get_session)):
    # Cambiado Serie por SerieModel
    todas_series = session.exec(select(SerieModel)).all()
    return templates.TemplateResponse("series.html", {
        "request": request, 
        "titulo": "Listado de Series",
        "series": todas_series
    })
@app.post("/series")
def guardar_serie_api(serie: SerieModel, session: Session = Depends(get_session)):
    try:
        session.add(serie)
        session.commit()
        session.refresh(serie)
        return {
            "message": "Serie guardada correctamente",
            "data": {"nombre": serie.ser_nombre}
        }
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Error al guardar en la base de datos")

@app.put("/series")
def mod_serie(serie: SerieModel, session: Session = Depends(get_session)):
    try:
        serie_actualizada = session.merge(serie)
        session.commit()
        session.refresh(serie_actualizada)
        return {
            "message": "Serie modificada correctamente",
            "data": {
                "nombre": serie.ser_nombre
            }
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail="Error al modificar en la base de datos")
@app.get("/agr_serie", response_class=HTMLResponse)
def vista_agregar_serie(request: Request):
    return templates.TemplateResponse("agr_serie.html", {"request": request, "titulo": "Agregar Serie"})

@app.get("/series/edit/{id}", response_class=HTMLResponse)
def agr_serie(id:int,request: Request,session: Session = Depends(get_session)):
    datos_serie = session.exec(select(SerieModel).where(SerieModel.ser_id == id )).one()
    return templates.TemplateResponse("agr_serie.html", {"request": request, "titulo": "Mi Dashboard", "datos": datos_serie})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("default.html", {"request": request, "titulo": "Inicio"})

@app.get("/login", response_class=HTMLResponse)
async def vista_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "titulo": "Login"})

@app.get("/capitulos", response_class=HTMLResponse)
async def listar_capitulos(request: Request):
    return templates.TemplateResponse("default.html", {"request": request, "titulo": "Capítulos"})