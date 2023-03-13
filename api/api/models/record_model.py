from sqlalchemy import Boolean, Column, INT, FLOAT,String, DateTime, BigInteger, ForeignKey,DATE,DATETIME,INT
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from ..core.database import Base
import datetime

# vital_record_all(모든 데이터:lab data 포함) 테이블 - 사용중임
class VitalRecordAll(Base):
  __tablename__ = 'vital_record_all'
  pid=Column(INT,ForeignKey('patient_general.pid'),primary_key=True)
  ICULOS=Column(INT,nullable=False)
  p_record_seq = Column(INT, primary_key=True)
  birth_date=Column(DATE,nullable=False)
  input_time=Column(DATETIME,nullable=False)
  Gender=Column(INT,nullable=False)
  HR=Column(INT,nullable=False)
  O2Sat=Column(FLOAT,nullable=False)
  Temp=Column(FLOAT,nullable=False)
  SBP=Column(INT,nullable=False)
  DBP=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  Resp=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,default=None)
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
  Age=Column(INT,nullable=False)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)
  
  patient_general = relationship("PatientGeneralTable", back_populates="vital_record_all")
  lab_data_record = relationship("LabDataRecord", primaryjoin="VitalRecordAll.pid == LabDataRecord.pid")
  lab_data_filled = relationship("LabDataFilled", primaryjoin="VitalRecordAll.pid == LabDataFilled.pid")
# lab_data_table(lab data만 따로) 테이블
class LabDataRecord(Base):
  __tablename__='lab_data_record'
  pid=Column(INT,ForeignKey('vital_record_all.pid'),primary_key=True,)
  lab_record_seq=Column(INT,primary_key=True)
  EtCO2=Column(FLOAT,nullable=True,default=None)
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

  vital_record_all = relationship('VitalRecordAll', back_populates='lab_data_record')

class LabDataFilled(Base):
  __tablename__='lab_data_filled'
  pid=Column(INT,ForeignKey('vital_record_all.pid'),primary_key=True,)
  lab_record_seq=Column(INT,primary_key=True)
  EtCO2=Column(FLOAT,nullable=True,default=None)
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

  vital_record_all = relationship('VitalRecordAll', back_populates='lab_data_filled')

# vital_record_all_view 모든 환자 현재 정보 뷰(겹치는것같네)
class VitalRecordAllView(Base):
  __tablename__='vital_record_all_view'
  pid = Column(INT)
  ICULOS=Column(INT,nullable=False)
  birth_date = Column(DATE,nullable=False)
  Gender=Column(INT,nullable=False,)
  name=Column(String(50),nullable=False)
  emp_id=Column(INT,nullable=False)
  admin_date=Column(DATETIME, nullable=False)
  disch_date=Column(DATETIME,nullable=True)
  p_record_seq = Column(INT, primary_key=True)
  input_time=Column(DATETIME,nullable=False)
  HR=Column(INT,nullable=False)
  O2Sat=Column(FLOAT,nullable=False)
  Temp=Column(FLOAT,nullable=False)
  SBP=Column(INT,nullable=False)
  DBP=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  Resp=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,default=None)
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
  Age=Column(INT,nullable=False)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)

# vital_record_now_view 모든 환자 현재 정보 뷰
class VitalRecordNowView(Base):
  __tablename__='vital_record_now_view'
  pid = Column(INT)
  ICULOS=Column(INT,nullable=False)
  birth_date = Column(DATE,nullable=False)
  Gender=Column(INT,nullable=False,)
  name=Column(String(50),nullable=False)
  emp_id=Column(INT,nullable=False)
  admin_date=Column(DATETIME, nullable=False)
  disch_date=Column(DATETIME,nullable=True)
  p_record_seq = Column(INT, primary_key=True)
  input_time=Column(DATETIME,nullable=False)
  HR=Column(INT,nullable=False)
  O2Sat=Column(FLOAT,nullable=False)
  Temp=Column(FLOAT,nullable=False)
  SBP=Column(INT,nullable=False)
  DBP=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  Resp=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,default=None)
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
  Age=Column(INT,nullable=False)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)

# now_view_sepsis 모든 패혈증 환자의 view
class NowViewSepsis(Base):
  __tablename__='now_view_sepsis'
  pid = Column(INT)
  ICULOS=Column(INT,nullable=False)
  birth_date = Column(DATE,nullable=False)
  Gender=Column(INT,nullable=False,)
  name=Column(String(50),nullable=False)
  emp_id=Column(INT,nullable=False)
  admin_date=Column(DATETIME, nullable=False)
  disch_date=Column(DATETIME,nullable=True)
  p_record_seq = Column(INT, primary_key=True)
  input_time=Column(DATETIME,nullable=False)
  HR=Column(INT,nullable=False)
  O2Sat=Column(FLOAT,nullable=False)
  Temp=Column(FLOAT,nullable=False)
  SBP=Column(INT,nullable=False)
  DBP=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  Resp=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,default=None)
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
  Age=Column(INT,nullable=False)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)

# all_patients_vital_record_view 모든환자 모든 정보 뷰
class AllPatientRecordView(Base):
  __tablename__='all_patients_vital_record_view'
  pid = Column(INT)
  ICULOS=Column(INT,nullable=False)
  birth_date = Column(DATE,nullable=False)
  Gender=Column(INT,nullable=False,)
  name=Column(String(50),nullable=False)
  emp_id=Column(INT,nullable=False)
  admin_date=Column(DATETIME, nullable=False)
  disch_date=Column(DATETIME,nullable=True)
  p_record_seq = Column(INT, primary_key=True)
  input_time=Column(DATETIME,nullable=False)
  HR=Column(INT,nullable=False)
  O2Sat=Column(FLOAT,nullable=False)
  Temp=Column(FLOAT,nullable=False)
  SBP=Column(INT,nullable=False)
  DBP=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  Resp=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,default=None)
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
  Age=Column(INT,nullable=False)
  sepsis_in_six=Column(INT,nullable=True,default=None)
  sepsis_percent=Column(FLOAT,nullable=True,default=None)


# -------------------------여기부터 schema---------------
# 일반 정보 입력 모델로 바꿔야함
class VitalRecordAllMask(Base):
  __tablename__ = 'vital_record_all_mask'
  pid=Column(INT,ForeignKey('patient_general.pid'),primary_key=True)
  p_record_seq = Column(INT, primary_key=True)
  ICULOS=Column(INT,nullable=False)
  birth_date=Column(DATE,nullable=False)
  input_time=Column(DATETIME,nullable=False)
  Gender=Column(INT,nullable=False)
  HR=Column(INT,nullable=False)
  O2Sat=Column(FLOAT,nullable=False)
  Temp=Column(FLOAT,nullable=False)
  SBP=Column(INT,nullable=False)
  DBP=Column(INT,nullable=False)
  MAP=Column(FLOAT,nullable=True)
  Resp=Column(INT,nullable=False)
  EtCO2=Column(FLOAT,nullable=True,default=None)
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
  Age=Column(INT,nullable=False)

  HR_mask = Column(INT, nullable=False, default=0)
  O2Sat_mask = Column(INT, nullable=False, default=0)
  Temp_mask = Column(INT, nullable=False, default=0)
  SBP_mask = Column(INT, nullable=False, default=0)
  DBP_mask = Column(INT, nullable=False, default=0)
  MAP_mask = Column(INT, nullable=False, default=0)
  Resp_mask = Column(INT, nullable=False, default=0)
  EtCO2_mask = Column(INT, nullable=False, default=0)
  BaseExcess_mask = Column(INT, nullable=False, default=0)
  HCO3_mask = Column(INT, nullable=False, default=0)
  FiO2_mask = Column(INT, nullable=False, default=0)
  pH_mask = Column(INT, nullable=False, default=0)
  PaCO2_mask = Column(INT, nullable=False, default=0)
  SaO2_mask = Column(INT, nullable=False, default=0)
  AST_mask = Column(INT, nullable=False, default=0)
  BUN_mask = Column(INT, nullable=False, default=0)
  Alkalinephos_mask = Column(INT, nullable=False, default=0)
  Calcium_mask = Column(INT, nullable=False, default=0)
  Chloride_mask = Column(INT, nullable=False, default=0)
  Creatinine_mask = Column(INT, nullable=False, default=0)
  Glucose_mask = Column(INT, nullable=False, default=0)
  Lactate_mask = Column(INT, nullable=False, default=0)
  Magnesium_mask = Column(INT, nullable=False, default=0)
  Phosphate_mask = Column(INT, nullable=False, default=0)
  Potassium_mask = Column(INT, nullable=False, default=0)
  Bilirubin_total_mask = Column(INT, nullable=False, default=0)
  Hct_mask = Column(INT, nullable=False, default=0)
  Hgb_mask = Column(INT, nullable=False, default=0)
  PTT_mask = Column(INT, nullable=False, default=0)
  WBC_mask = Column(INT, nullable=False, default=0)
  Fibrinogen_mask = Column(INT, nullable=False, default=0)
  Platelets_mask = Column(INT, nullable=False, default=0)
  Age_mask = Column(INT, nullable=False, default=0)
  
  
  patient_general = relationship("PatientGeneralTable", back_populates="vital_record_all_mask")