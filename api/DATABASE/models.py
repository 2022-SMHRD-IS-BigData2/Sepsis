from sqlalchemy import Boolean, Column, INT, FLOAT,String, DateTime, BigInteger, ForeignKey,DATE,DATETIME,INT
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from db import Base
from db import ENGINE

import datetime


class PatientGeneralTable(Base):
  __tablename__='patient_general'
  pid = Column(INT, primary_key=True, autoincrement=True)
  birth_date = Column(DATE,nullable=False)
  sex=Column(INT,nullable=False)
  age=Column(INT,nullable=False)
  name=Column(String(50),nullable=False)
  emp_id=Column(INT,nullable=False)
  admin_date=Column(DATETIME, nullable=False)
  disch_date=Column(DATETIME,nullable=True)

  vital_record_all = relationship("VitalRecordAll", back_populates="patient_general")
  vital_record_normal = relationship("VitalRecordNormal", back_populates="patient_general")


class VitalRecordNormal(Base):
  __tablename__ = 'vital_record_normal'
  pid=Column(INT,ForeignKey('patient_general.pid'),primary_key=True)
  p_record_seq = Column(INT, primary_key=True)
  birth_date=Column(DATE,nullable=False)
  input_time=Column(DATETIME,nullable=False)
  sex=Column(INT,nullable=False)
  age=Column(INT,nullable=False)
  hr=Column(INT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOC=Column(INT,nullable=False)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)
  
  patient_general = relationship("PatientGeneralTable", back_populates="vital_record_normal")
  lab_data_record = relationship("LabDataRecord", primaryjoin="VitalRecordNormal.pid == LabDataRecord.pid")

class VitalRecordAll(Base):
  __tablename__ = 'vital_record_all'
  pid=Column(INT,ForeignKey('patient_general.pid'),primary_key=True)
  p_record_seq = Column(INT, primary_key=True)
  birth_date=Column(DATE,nullable=False)
  input_time=Column(DATETIME,nullable=False)
  sex=Column(INT,nullable=False)
  age=Column(INT,nullable=False)
  hr=Column(INT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOC=Column(INT,nullable=False)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Bilirubin_direct=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  TroponinI=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)
  
  patient_general = relationship("PatientGeneralTable", back_populates="vital_record_all")


class LabDataRecord(Base):
  __tablename__='lab_data_record'
  pid=Column(INT,ForeignKey('vital_record_normal.pid'),primary_key=True,)
  p_record_seq = Column(INT,ForeignKey('vital_record_normal.p_record_seq'),primary_key=True)
  lab_record_seq=Column(INT,primary_key=True)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Bilirubin_direct=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  TroponinI=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)

  vital_record_normal=relationship('VitalRecordNormal', back_populates='lab_data_record', primaryjoin="and_(LabDataRecord.pid==VitalRecordNormal.pid, LabDataRecord.p_record_seq==VitalRecordNormal.p_record_seq)")



class VitalRecordAllView(Base):
  __tablename__='vital_record_all_view'
  pid = Column(INT)
  birth_date = Column(DATE,nullable=False)
  sex=Column(INT,nullable=False,)
  name=Column(String(50),nullable=False)
  age=Column(INT,nullable=False)
  emp_id=Column(INT,nullable=False)
  admin_date=Column(DATETIME, nullable=False)
  disch_date=Column(DATETIME,nullable=True)
  p_record_seq = Column(INT, primary_key=True)
  input_time=Column(DATETIME,nullable=False)
  hr=Column(INT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOC=Column(INT,nullable=False)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Bilirubin_direct=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  TroponinI=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)

# 모든 환자의 최근 데이터 view
class VitalRecordNowView(Base):
  __tablename__='vital_record_now_view'
  pid = Column(INT)
  birth_date = Column(DATE,nullable=False)
  sex=Column(INT,nullable=False,)
  age=Column(INT,nullable=False)
  name=Column(String(50),nullable=False)
  emp_id=Column(INT,nullable=False)
  admin_date=Column(DATETIME, nullable=False)
  disch_date=Column(DATETIME,nullable=True)
  p_record_seq = Column(INT, primary_key=True)
  input_time=Column(DATETIME,nullable=False)
  hr=Column(INT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOC=Column(INT,nullable=False)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Bilirubin_direct=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  TroponinI=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)

  # 모든 패혈증 환자의 view
class NowViewSepsis(Base):
  __tablename__='now_view_sepsis'
  pid = Column(INT)
  birth_date = Column(DATE,nullable=False)
  sex=Column(INT,nullable=False,)
  age=Column(INT,nullable=False)
  name=Column(String(50),nullable=False)
  emp_id=Column(INT,nullable=False)
  admin_date=Column(DATETIME, nullable=False)
  disch_date=Column(DATETIME,nullable=True)
  p_record_seq = Column(INT, primary_key=True)
  input_time=Column(DATETIME,nullable=False)
  hr=Column(INT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOC=Column(INT,nullable=False)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Bilirubin_direct=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  TroponinI=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)


class AllPatientRecordView(Base):
  __tablename__='all_patients_vital_record_view'
  pid = Column(INT)
  birth_date = Column(DATE,nullable=False)
  sex=Column(INT,nullable=False,)
  age=Column(INT,nullable=False)
  name=Column(String(50),nullable=False)
  emp_id=Column(INT,nullable=False)
  admin_date=Column(DATETIME, nullable=False)
  disch_date=Column(DATETIME,nullable=True)
  p_record_seq = Column(INT, primary_key=True)
  input_time=Column(DATETIME,nullable=False)
  hr=Column(INT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOC=Column(INT,nullable=False)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Bilirubin_direct=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  TroponinI=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)