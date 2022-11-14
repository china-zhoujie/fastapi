#!/usr/bin/python3
# -*- coding:utf-8 -*-
# __author__ = '__Jack__'

from typing import List
import requests
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl
from sqlalchemy.orm import Session
from coronavirus import crud, schemas
from coronavirus.database import engine, Base, SessionLocal
from coronavirus.models import City, Data
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

application = APIRouter()

#接口限速
limiter = Limiter(key_func=get_remote_address)

#引入模板
templates = Jinja2Templates(directory='./coronavirus/templates')

#将模型映射到数据库中
Base.metadata.create_all(bind=engine)

#创建数据库依赖
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@application.post("/create_city", response_model = schemas.ReadCity)
async def create_city(city: schemas.CreateCity, db: Session=Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city.province)
    if db_city:
        raise HTTPException(status_code=400, detail="City already registered")
    return crud.create_city(db=db, city=city)
    

@application.get("/get_city/{city_id}", response_model = schemas.ReadCity)
async def get_city(city: str, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db, name=city)
    if db_city is None:
        raise HTTPException(status_code=400, detail="City is found")
    return db_city
    

@application.get("/get_cities", response_model = List[schemas.ReadCity])
async def get_cities(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cities = crud.get_cities(db=db, skip=skip, limit=limit)
    return cities
    
@application.post("/create_data",response_model = schemas.ReadData)
async def create_data_for_city(city: str, data : schemas.CreateData, db: Session = Depends(get_db)):
    db_city = crud.get_city_by_name(db=db,name=city)
    data = crud.create_city_data(db=db, data=data, city_id = db_city.id)
    return data
    
@application.get("/get_data")
@limiter.limit("8/minute")
async def get_data(request: Request, city: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = crud.get_data(db, city=city, skip=skip, limit=limit)
    return data

def bg_task(url: HttpUrl, db: Session):
    city_data = requests.get(url=f"{url}?source=jhu&country_code=CN&timelines=false")
    if city_data.status_code == 200:
        db.execute("SET FOREIGN_KEY_CHECKS = 0")#关闭外键约束
        db.execute("TRUNCATE `city`;")
        db.execute("TRUNCATE `data`;")
        #db.query(City).delete()  # 同步数据前先清空原有的数据
        #db.query(Data).delete()
        db.execute("SET FOREIGN_KEY_CHECKS = 1")#开启外键约束
        for locations in city_data.json()["locations"]:
            city={
                "province": locations["province"],
                "country": locations["country"],
                "country_code": locations["country_code"],
                "country_population": locations["country_population"]
            }
            crud.create_city(db=db,city=schemas.CreateCity(**city))
    coronavirus_data = requests.get(url=f"{url}?source=jhu&country_code=CN&timelines=true")
    if coronavirus_data.status_code == 200:
        for city in coronavirus_data.json()["locations"]:
            db_city = crud.get_city_by_name(db=db, name=city["province"])
            for date, confirmed in city["timelines"]["confirmed"]["timeline"].items():
                data = {
                    "date":date.split("T")[0],
                    "confirmed": confirmed,
                    "deaths": city["timelines"]["deaths"]["timeline"][date],
                    "recovered": 0
                }
                crud.create_city_data(db=db, data=schemas.CreateData(**data),city_id=db_city.id)

@application.get("/sync_coronavirus_data/jhu")
async def sync_coronavirus_data(backguround_task: BackgroundTasks, db: Session = Depends(get_db)):
    """从Johns Hopkins University同步COVID-19数据"""
    backguround_task.add_task(bg_task,"https://coronavirus-tracker-api.herokuapp.com/v2/locations", db)
    return {"message":"正在同步后台数据..."}
    
def count_start(page: int):#计算起始
    return (page-1) * 50
    
  
@application.get("/")
async def coronavirus(request: Request, city: str = None, page: int = 1, limit: int = 50, db: Session = Depends(get_db)):
    data = crud.get_data(db, city=city, skip=count_start(page), limit=limit)
    count = crud.get_data_count(db, city=city, skip=count_start(page), limit=limit)
    city_all = crud.get_city(db)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "data": data,
        "city": city,
        "data_count": count,
        "curr_page": page,
        "city_all": city_all,
        "sync_data_url": "/coronavirus/sync_coronavirus_data/jhu"
    })