from sqlalchemy import Boolean, Column, INT, FLOAT,String, DateTime, BigInteger, ForeignKey,DATE,DATETIME,INT
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from ..core.database import Base
import datetime

# vital_record_normal(일반 데이터:lab data 없음) 테이블
class VitalRecordNormal(Base):
  __tablename__ = 'vital_record_normal'
  pid=Column(INT,ForeignKey('patient_general.pid'),primary_key=True)
  p_record_seq = Column(INT, primary_key=True)
  birth_date=Column(DATE,nullable=False)
  input_time=Column(DATETIME,nullable=False)
  sex=Column(INT,nullable=False)
  age=Column(INT,nullable=False)
  hr=Column(INT,nullable=False)
  O2Sat=Column(FLOAT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOS=Column(INT,nullable=False)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)
  
  patient_general = relationship("PatientGeneralTable", back_populates="vital_record_normal")
  lab_data_record = relationship("LabDataRecord", primaryjoin="VitalRecordNormal.pid == LabDataRecord.pid")

# vital_record_all(모든 데이터:lab data 포함) 테이블 - 사용중임
class VitalRecordAll(Base):
  __tablename__ = 'vital_record_all'
  pid=Column(INT,ForeignKey('patient_general.pid'),primary_key=True)
  p_record_seq = Column(INT, primary_key=True)
  birth_date=Column(DATE,nullable=False)
  input_time=Column(DATETIME,nullable=False)
  sex=Column(INT,nullable=False)
  age=Column(INT,nullable=False)
  hr=Column(INT,nullable=False)
  O2Sat=Column(FLOAT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOS=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,defalut=None)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  AST=Column(FLOAT,nullable=True,default=None)
  BUN=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)
  
  patient_general = relationship("PatientGeneralTable", back_populates="vital_record_all")

# lab_data_table(lab data만 따로) 테이블
class LabDataRecord(Base):
  __tablename__='lab_data_record'
  pid=Column(INT,ForeignKey('vital_record_normal.pid'),primary_key=True,)
  p_record_seq = Column(INT,ForeignKey('vital_record_normal.p_record_seq'),primary_key=True)
  lab_record_seq=Column(INT,primary_key=True)
  EtCO2=Column(FLOAT,nullable=True,defalut=None)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  AST=Column(FLOAT,nullable=True,default=None)
  BUN=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)

  vital_record_normal=relationship('VitalRecordNormal', back_populates='lab_data_record', primaryjoin="and_(LabDataRecord.pid==VitalRecordNormal.pid, LabDataRecord.p_record_seq==VitalRecordNormal.p_record_seq)")

# vital_record_all_view 모든 환자 현재 정보 뷰(겹치는것같네)
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
  O2Sat=Column(FLOAT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOS=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,defalut=None)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  AST=Column(FLOAT,nullable=True,default=None)
  BUN=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)

# vital_record_now_view 모든 환자 현재 정보 뷰
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
  O2Sat=Column(FLOAT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOS=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,defalut=None)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  AST=Column(FLOAT,nullable=True,default=None)
  BUN=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)

# now_view_sepsis 모든 패혈증 환자의 view
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
  O2Sat=Column(FLOAT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOS=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,defalut=None)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  AST=Column(FLOAT,nullable=True,default=None)
  BUN=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)

# all_patients_vital_record_view 모든환자 모든 정보 뷰
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
  O2Sat=Column(FLOAT,nullable=False)
  temp=Column(FLOAT,nullable=False)
  resp=Column(INT,nullable=False)
  sbp=Column(INT,nullable=False)
  dbp=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  ICULOS=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,defalut=None)
  BaseExcess=Column(FLOAT,nullable=True,default=None)
  HCO3=Column(FLOAT,nullable=True,default=None)
  FiO2=Column(FLOAT,nullable=True,default=None)
  pH=Column(FLOAT,nullable=True,default=None)
  PaCO2=Column(FLOAT,nullable=True,default=None)
  SaO2=Column(FLOAT,nullable=True,default=None)
  AST=Column(FLOAT,nullable=True,default=None)
  BUN=Column(FLOAT,nullable=True,default=None)
  Alkalinephos=Column(FLOAT,nullable=True,default=None)
  Calcium=Column(FLOAT,nullable=True,default=None)
  Chloride=Column(FLOAT,nullable=True,default=None)
  Creatinine=Column(FLOAT,nullable=True,default=None)
  Glucose=Column(FLOAT,nullable=True,default=None)
  Lactate=Column(FLOAT,nullable=True,default=None)
  Magnesium=Column(FLOAT,nullable=True,default=None)
  Phosphate=Column(FLOAT,nullable=True,default=None)
  Potassium=Column(FLOAT,nullable=True,default=None)
  Bilirubin_total=Column(FLOAT,nullable=True,default=None)
  Hct=Column(FLOAT,nullable=True,default=None)
  Hgb=Column(FLOAT,nullable=True,default=None)
  PTT=Column(FLOAT,nullable=True,default=None)
  WBC=Column(FLOAT,nullable=True,default=None)
  Fibrinogen=Column(FLOAT,nullable=True,default=None)
  Platelets=Column(FLOAT,nullable=True,default=None)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)


# -------------------------여기부터 schema---------------
# 일반 정보 입력 모델로 바꿔야함
