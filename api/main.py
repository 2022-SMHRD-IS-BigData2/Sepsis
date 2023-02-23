from fastapi import FastAPI,Response
from fastapi.encoders import jsonable_encoder
from DATABASE.schemas import Patient,Record
from typing import List
from starlette.middleware.cors import CORSMiddleware
from db import session,Database
from DATABASE.models import VitalRecordAll,PatientGeneralTable
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import json
import sys
import os

sys.setrecursionlimit(10**7)

app = FastAPI()
db=Database(app)
# 현재 파일(main.py)의 경로에서 상위 경로인 sepsis/까지의 경로를 구합니다.
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# # static 디렉토리의 경로를 구합니다.
# STATIC_DIR = os.path.join(BASE_DIR, "static")

# # static 디렉토리를 정적 파일 서빙 미들웨어에 등록합니다.
# app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")


@app.on_event("startup")
async def startup_event():
    db.connect()

def get_db():
    try:
        db = session()
        yield db
    finally:
        db.close()

app.add_middleware(
  CORSMiddleware,
  allow_origins=['*'],
  allow_credentials=True,
  allow_methods=['*'],
  allow_headers=['mysql://project-db-stu2.ddns.net:3307','*']
)

@app.get('/api/patients')
async def index():
  patients=session.query(PatientGeneralTable).all()

  return patients

@app.get('/api/patients/{p_id}')
async def index(p_id:int):
  one_patient=session.query(PatientGeneralTable).filter(PatientGeneralTable.p_id==p_id).first()
  return one_patient



@app.post('/api/mk_patient')
async def mk_patient(mk_patient:Patient):
  temp=PatientGeneralTable()
  temp.p_id=mk_patient.p_id
  temp.birth_date=mk_patient.birth_date
  temp.sex=mk_patient.sex
  temp.emp_id=mk_patient.emp_id
  temp.admin_date=mk_patient.admin_date
  temp.p_name=mk_patient.p_name
  if mk_patient.disch_date:
    temp.disch_date=None
  else:
    temp.disch_date=mk_patient.disch_date
  session.add(temp)
  session.commit()
  return mk_patient

@app.get('/api/record/{p_id}')
async def p_record_all(p_id:int):
  p_record=session.query(VitalRecordAll).filter(VitalRecordAll.p_id==p_id).all()
  return p_record





@app.get("/api/all_from_view")
async def get_view():
    query = "SELECT * FROM vital_record_now_view"
    result=db.execute(query)

    data = [row for row in result]
    # data_json = json.dumps(data)

    return {"data": data}