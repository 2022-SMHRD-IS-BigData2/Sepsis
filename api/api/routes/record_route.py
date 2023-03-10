from fastapi import APIRouter, Depends
from ..core.database import session
from ..core.pred_model import Sepsis_Pred_Model
from typing import List,Tuple
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey,text,and_,desc
from sqlalchemy.orm import relationship
from fastapi.encoders import jsonable_encoder
from api.models.record_model import *
from api.models.patient_model import *
from api.schemas.record_schema import *
import pandas as pd, numpy as np
from datetime import datetime
import datetime
import random
import json

import torch
import torch.nn.functional as F
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
router = APIRouter()

col_stat = json.load(open('api\\col_stat.json', 'r'))

vital_cols=['HR', 'O2Sat', 'Temp', 'SBP', 'DBP', 'MAP', 'Resp','EtCO2',
      'BaseExcess', 'HCO3', 'FiO2', 'pH', 'PaCO2', 'SaO2', 'AST', 'BUN',
      'Alkalinephos', 'Calcium', 'Chloride', 'Creatinine',
      'Glucose', 'Lactate', 'Magnesium', 'Phosphate', 'Potassium',
      'Bilirubin_total', 'Hct', 'Hgb', 'PTT', 'WBC',
      'Fibrinogen', 'Platelets','Age']

INFO_COLS = ['pid', 'HospAdmTime', 'ICULOS', 'SepsisLabel', 'Age','Gender']

lab_cols=['pid','EtCO2',
      'BaseExcess', 'HCO3', 'FiO2', 'pH', 'PaCO2', 'SaO2', 'AST', 'BUN',
      'Alkalinephos', 'Calcium', 'Chloride', 'Creatinine',
      'Glucose', 'Lactate', 'Magnesium', 'Phosphate', 'Potassium',
      'Bilirubin_total', 'Hct', 'Hgb', 'PTT', 'WBC',
      'Fibrinogen', 'Platelets']
lab_cols2=['EtCO2',
      'BaseExcess', 'HCO3', 'FiO2', 'pH', 'PaCO2', 'SaO2', 'AST', 'BUN',
      'Alkalinephos', 'Calcium', 'Chloride', 'Creatinine',
      'Glucose', 'Lactate', 'Magnesium', 'Phosphate', 'Potassium',
      'Bilirubin_total', 'Hct', 'Hgb', 'PTT', 'WBC',
      'Fibrinogen', 'Platelets','sepsis_in_six','sepsis_percent']
lab_cols3=['EtCO2',
      'BaseExcess', 'HCO3', 'FiO2', 'pH', 'PaCO2', 'SaO2', 'AST', 'BUN',
      'Alkalinephos', 'Calcium', 'Chloride', 'Creatinine',
      'Glucose', 'Lactate', 'Magnesium', 'Phosphate', 'Potassium',
      'Bilirubin_total', 'Hct', 'Hgb', 'PTT', 'WBC',
      'Fibrinogen', 'Platelets']

COLS = ['HR', 'O2Sat', 'Temp', 'SBP', 'MAP', 'DBP', 'Resp','EtCO2',
      'BaseExcess', 'HCO3', 'FiO2', 'pH', 'PaCO2', 'SaO2', 'AST', 'BUN',
      'Alkalinephos', 'Calcium', 'Chloride', 'Creatinine',
      'Glucose', 'Lactate', 'Magnesium', 'Phosphate', 'Potassium',
      'Bilirubin_total', 'Hct', 'Hgb', 'PTT', 'WBC',
      'Fibrinogen', 'Platelets','Age']

MASK_COLS = [x+"_mask" for x in COLS]
drop_list=["pid","p_record_seq","birth_date","input_time","Gender","ICULOS"]

#model ??????
def cut_or_fill_seq(input_tensor, seq_len=30):
  if input_tensor.shape[1]>seq_len:
      input_tensor=input_tensor[:,-seq_len:]
  elif input_tensor.shape[1]<seq_len:
      zeros = np.zeros([input_tensor.shape[0], seq_len-input_tensor.shape[1], input_tensor.shape[2]])
      input_tensor = np.concatenate([zeros, input_tensor], axis=1)
  return torch.Tensor(input_tensor)

def percent_80(output:float):
  if output>0.8:
    sepsis=1
  else:
    sepsis=0
  return sepsis,output*100

sepsis_model=Sepsis_Pred_Model(66,64)

  # import pdb; pdb.set_trace()
# model predict
@router.get("/api/predict_sepsis/{pid}")
async def model_pred(pid:int):
  data_sat_raw2 = session.query(VitalRecordAllMask).filter(VitalRecordAllMask.pid == pid).order_by(VitalRecordAllMask.p_record_seq.desc()).limit(30).all()
  if data_sat_raw2:
    data_sat_raw = pd.DataFrame.from_records([record.__dict__ for record in data_sat_raw2])
    data_sat_raw.drop('_sa_instance_state',axis=1,inplace=True)
    data_sat_raw=data_sat_raw.sort_values(["pid", "p_record_seq"]).reset_index(drop=True)
    max_seq = len(data_sat_raw)

    pred_sat=[]
    # ICULOS ?????? ???????????? ??????????????? ?????????~
    for k in range(max_seq):
      if (data_sat_raw.iloc[max_seq-k-1].ICULOS - data_sat_raw.iloc[max_seq-k-2].ICULOS == 1):
        pred_sat.insert(0,data_sat_raw.iloc[max_seq-k-1])
      else:
        if k == max_seq-1:
          pred_sat.insert(0,data_sat_raw.iloc[max_seq-k-1])
          break
        else:
          break

    # pred_sat df??? ????????????
    pred_sat2=pd.DataFrame(pred_sat)
    pred_sat_dropped=pred_sat2.drop(drop_list,axis=1,inplace=False).copy()
    # ?????? ?????????
    pred_sat_dropped = pred_sat_dropped[COLS+MASK_COLS]
    max_seq_len = 30
    # ??????????????????~
    for col in COLS:
      pred_sat_dropped[col] = (pred_sat_dropped[col] - col_stat[col]['mean']) / col_stat[col]['std']
    
    # zero ????????????!
    pred_array=pred_sat_dropped.values
    # print(pred_array)
    input_tensor_raw = torch.tensor(pred_array, dtype=torch.float32).unsqueeze(0) 
    input_tensor=cut_or_fill_seq(input_tensor_raw,seq_len=max_seq_len)

    sepsis_model.load_state_dict(torch.load("api\\0.774.pth"))
    sepsis_model.eval()
    with torch.no_grad():
      output_tensor = sepsis_model(input_tensor)
    # ????????? ??????
    output_tensor = F.sigmoid(output_tensor)
    output = output_tensor.squeeze().item() # Tensor?????? ?????? ????????? scalar ????????? ??????
    # update?????????
    sep,percent=percent_80(output)
    query=text("update vital_record_all set sepsis_in_six = :sepsis_in_six, sepsis_percent = :sepsis_percent where pid = :pid and p_record_seq = :p_record_seq")
    values={'sepsis_in_six' : sep,
            'sepsis_percent' : percent,
            'pid': pid,
            'p_record_seq':data_sat_raw.iloc[-1].p_record_seq}
    session.execute(query,values)
    session.commit()
    session.close()
    return sep,percent

@router.get("/api/data/")
async def get_data(limit: int = 10, page: int = 1):
  offset = (page - 1) * limit
  query = text(f"SELECT * FROM vital_record_now_view LIMIT :limit OFFSET :offset")
  result = session.execute(query, {"limit": limit, "offset": offset})
  data = [dict(row) for row in result]
  count = session.execute(text("SELECT COUNT(*) FROM vital_record_now_view")).fetchone()[0]
  session.close()
  return {"data": data, "count": count,'page':{'page':1,'limit':10}}

# ?????? ????????? ?????? ??????????????? ????????? ?????? ??????
@router.get('/api/get_latest_all/{pid}')
async def get_latest_all(pid:int):
  record=session.query(VitalRecordNowView).filter(VitalRecordNowView.pid==pid).all()
  session.close()
  return record

# sepsis ????????? ????????????/????????? ????????????
@router.get('/api/get_latest_sepsis_all')
async def get_latest_sepsis_all(limit: int = 10, page: int = 1):
  offset = (page - 1) * limit
  query = text(f"SELECT * FROM now_view_sepsis LIMIT :limit OFFSET :offset")
  result = session.execute(query, {"limit": limit, "offset": offset}).all()
  data = [dict(row) for row in result]
  count = session.execute(text("SELECT COUNT(*) FROM now_view_sepsis")).fetchone()[0]
  session.close()
  return {"data": data, "count": count,'page':{'page':1,'limit':10}}

# sepsis ???????????? 80?????? ???????????? / ????????? ????????????
@router.get('/api/get_latest_sepsis_percent')
async def get_latest_sepsis_percent(limit: int = 10, page: int = 1):
  offset = (page - 1) * limit
  query = text(f"SELECT * FROM vital_record_now_view where sepsis_percent>=80 LIMIT :limit OFFSET :offset")
  result = session.execute(query, {"limit": limit, "offset": offset}).all()
  data = [dict(row) for row in result]
  count = session.execute(text("SELECT COUNT(*) FROM vital_record_now_view where sepsis_percent>=80")).fetchone()[0]
  session.close()
  return {"data": data, "count": count,'page':{'page':1,'limit':10}}

# 
@router.get('/api/get_all_record')
async def get_all_record():
  record=session.query(AllPatientRecordView).all()
  session.close()
  return record

@router.get('/api/get_select_date')
async def get_select_date(pid:int,date:str):
  date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()  # ????????? ????????? ????????? datetime ????????? ??????
  record = session.query(AllPatientRecordView).filter(and_(AllPatientRecordView.pid == pid, AllPatientRecordView.input_time >= date_obj, AllPatientRecordView.input_time < date_obj + datetime.timedelta(days=1))).all()
  session.close()
  return record

# ????????????~????????? ???????????? ????????????????????? ??????????????????
@router.get('/api/get_search_data')
async def get_search_patient(path: str = '', search_str: str = '', limit: int = 10, page: int = 1):
    offset = (page - 1) * limit
    search_str = f"%{search_str}%" # ?????? ????????? ????????? % ??????
    query = None
    count = None
    data=[]

    switch_path = {
        '/': f"SELECT * FROM vital_record_now_view WHERE (pid LIKE :search_str OR name LIKE :search_str) LIMIT :limit OFFSET :offset",
        '/detected': f"SELECT * FROM now_view_sepsis WHERE (pid LIKE :search_str OR name LIKE :search_str) LIMIT :limit OFFSET :offset",
    }
    switch_count = {
        '/': "SELECT COUNT(*) FROM patient_general WHERE (pid LIKE :search_str OR name LIKE :search_str)",
        '/detected': "SELECT COUNT(*) FROM now_view_sepsis WHERE (pid LIKE :search_str OR name LIKE :search_str)",
    }
    if path in switch_path:
        query = text(switch_path[path])
        count = session.execute(text(switch_count[path]), {"search_str": search_str}).fetchone()[0]

    if query is not None:
        result = session.execute(query, {"search_str": search_str, "limit": limit, "offset": offset}).all()
        data = [dict(row) for row in result]
    else:
        data = []

    return {"data": data, "count": count, "page": {"page": page, "limit": limit}}

# pid, input_time ??????????????? ??? ????????? record ???????????? api
@router.get('/api/get_select_record/{pid}')
async def get_select_record(pid: int, input_time: str):
    input_time = datetime.datetime.strptime(input_time, '%Y-%m-%dT%H:%M:%S')
    query = text(f'select * from all_patients_vital_record_view where pid =:pid and input_time=:input_time')
    record = session.execute(query, {"pid":pid,"input_time": input_time}).first()
    session.close()
    return {"data": record}

# record ????????? ??? ????????? ?????????????????? api
@router.post('/api/update_record/{pid}')
async def update_record(pid:int, record_u:Record_u):
  query = text(f"UPDATE vital_record_all SET HR = :HR, O2Sat = :O2Sat, Temp = :Temp, Resp = :Resp, SBP = :SBP, DBP = :DBP WHERE pid = :pid AND p_record_seq = :p_record_seq")
  values = {'HR': record_u.HR, 'O2Sat': record_u.O2Sat, 'Temp': record_u.Temp, 'Resp': record_u.Resp, 'SBP': record_u.SBP, 'DBP': record_u.DBP, 'pid': pid, 'p_record_seq': record_u.p_record_seq}
    # ?????? ??????
  session.execute(query,values)
  session.commit()
  query = text(f"UPDATE vital_record_all_mask SET HR = :HR, O2Sat = :O2Sat, Temp = :Temp, Resp = :Resp, SBP = :SBP, DBP = :DBP WHERE pid = :pid AND p_record_seq = :p_record_seq")
  values = {'HR': record_u.HR, 'O2Sat': record_u.O2Sat, 'Temp': record_u.Temp, 'Resp': record_u.Resp, 'SBP': record_u.SBP, 'DBP': record_u.DBP, 'pid': pid, 'p_record_seq': record_u.p_record_seq}
    # ?????? ??????
  session.execute(query,values)
  session.commit()
  model_pred(pid)
  updated_record = session.query(AllPatientRecordView).filter(AllPatientRecordView.pid == pid, AllPatientRecordView.p_record_seq == record_u.p_record_seq).first()
  session.close()
  return updated_record

# ????????? ????????? ?????? 7??? record??? ????????????
@router.get('/api/chart_records/{pid}')
async def chart_records(pid:int):
  query=text(f"SELECT * FROM all_patients_vital_record_view WHERE pid={pid} ORDER BY input_time DESC LIMIT 7")
  
  chart_records = session.execute(query).all()
  session.close()
  return chart_records

# lab data!!!!!!
@router.post('/api/lab_insert/{pid}')
async def lab_insert(pid:int,labdata: LabData):
    # -----------------lab_data_record ??????--------------------------
  db_lab_data = LabDataRecord(**labdata.dict())
  session.add(db_lab_data)
  session.commit()

  # -----------------lab_data_filled ?????????-------------------
  df_fill_list = pd.read_sql(session.query(LabDataRecord).filter(LabDataRecord.pid==pid).statement, session.bind)
  # ????????? ??????????????? dup??? ?????????

  for col in lab_cols:
    # pid??? ????????? ???(record_seq=1)?????? ????????? => ????????? ????????? ??????
    first_index = df_fill_list.drop_duplicates(['pid'], keep='first').index
    # train_df.loc[first_index,col]??? ???: ??? pid??? ????????? ????????? ????????? ????????? null?????? ??????????????? ?????????, ????????? ?????? ????????? ??????!
    df_fill_list.loc[first_index, col] = df_fill_list.loc[first_index,col].apply(lambda x:col_stat[col]['median'] if pd.isna(x) else x)
    # ??? ?????? null?????? ??????????????? ??????????????? ffill ?????? ??? ?????????
    df_fill_list[col] = df_fill_list[col].fillna(method='ffill')
    db_lab_fill = LabDataFilled(**df_fill_list.iloc[-1].to_dict())
  session.add(db_lab_fill)
  session.commit()
# -----------------vital_record_all ?????? ????????? ??????????????????-----------
  latest_raw = session.query(VitalRecordAll).filter_by(pid=pid).order_by(desc(VitalRecordAll.p_record_seq)).first()
  filled_raw = session.query(LabDataFilled).filter_by(pid=pid).order_by(desc(LabDataFilled.lab_record_seq)).first()
  if latest_raw:
    #------latest vital_record_all update)
    dict_latest_raw=latest_raw.__dict__
    dict_filled_raw=filled_raw.__dict__
    dict_latest=dict_latest_raw.copy()
    dict_filled=dict_filled_raw.copy()
    df_latest=pd.DataFrame([dict_latest])
    df_filled=pd.DataFrame([dict_filled])
    df_latest.drop('_sa_instance_state',axis=1,inplace=True)
    df_filled.drop('_sa_instance_state',axis=1,inplace=True)
    df_filled.drop('lab_record_seq',axis=1,inplace=True)
    # ?????? lab data??? ????????? filled????????? ????????? ????????????????????????~~
    df_droped=df_latest.drop(lab_cols3,axis=1,inplace=False)
    # ?????? record_all ???????????? ????????? lab_record ????????????!
    df_merged=pd.merge(df_droped,df_filled,on='pid',how='outer')
    # to_dict!
    dict_merged=df_merged.iloc[0].to_dict()
    vital_update=VitalRecordAll(**dict_merged)
    session.merge(vital_update)
    session.commit()
    # latest_record??? ?????? ?????? vital_record_all ??? vital_record_all_mask ????????????
    # COLS: ?????? column ???????????? ?????????
    # ????????? ???????????????
    data1 = session.execute(f"SELECT * FROM vital_record_all WHERE pid={pid} ORDER BY p_record_seq DESC").fetchone()
    raw_data = pd.DataFrame([data1]) # ????????? ???????????????
    df_filled1 = raw_data.drop(['sepsis_in_six','sepsis_percent'],axis=1,inplace=False).copy()
    data2=raw_data.drop(lab_cols2,axis=1,inplace=False)
    data3=pd.DataFrame([labdata.dict()])
    # mask??????????????? df
    df_sub=pd.merge(data2,data3,on='pid')
    df_masks = pd.DataFrame()
    for col in COLS:
        # ?????? column?????? NaN??? ?????? ?????? index??? True???, NaN?????? False??? ??????
        df_masks[col+'_mask'] = df_sub[col].notnull().astype(int)
    # ?????? mask column??? ???????????? ????????? DataFrame?????? ??????
    df_masks = pd.concat([df_masks[x] for x in MASK_COLS], axis=1)
    df_filled1[df_masks.columns]=df_masks
    # df_filled??? df_masks??? merge
    df_sub_mask = df_filled1.copy()
    df_sub_dict=df_sub_mask.iloc[0].to_dict()
    print(df_sub_dict)
#   VitalRecordAllMask ???????????? primary key??? 'pid'??? 'p_record_seq' ?????? ????????? ???????????????
# -------------vital_record_all_mask ????????????~-----------------
    sub_mask = VitalRecordAllMask(**df_sub_dict)
    session.merge(sub_mask)
    session.commit()
#   # # ------------------vital_record_all_mask ?????? batch ??? ????????? model pred ?????????--------
  return pid

v_insert_list=['HR', 'O2Sat', 'Temp', 'SBP', 'DBP', 'MAP', 'Resp']

  # ------------------vital_record_all ?????? ????????? sepsis??????????????????--------------
@router.post('/api/vital_insert/{pid}')
async def vital_insert(pid:int,vital: Record_i):
  input_time = datetime.datetime.strptime(vital.input_time, '%Y-%m-%dT%H:%M:%S')
  birth_date = datetime.datetime.strptime(vital.birth_date, '%Y-%m-%d').date()
    # -----------------vital_record_all ????????? ??????--------------------------
  latest_filled=session.query(LabDataFilled).filter(LabDataFilled.pid==pid).order_by(desc(LabDataFilled.lab_record_seq)).first()
  vital_dict=vital.dict()

  if latest_filled: # lab data??? ?????????
    filled_dict=latest_filled.__dict__
    filled_dict.pop('_sa_instance_state')
    df_vi=pd.DataFrame([vital_dict])
    pd_fi=pd.DataFrame([filled_dict])
    df_fi=pd_fi.drop(['lab_record_seq'],axis=1,inplace=False).copy()
    df_filled=pd.merge(df_vi,df_fi,on='pid',how='outer')
    merged_dict = df_filled.to_dict(orient='records')[0]
    df_vital_insult=VitalRecordAll(**merged_dict)
    session.add(df_vital_insult)
    session.commit()

  #-------------------vital_record_all_mask ???????????? ????????????-----------------
    mask_raw2=session.query(VitalRecordAllMask).filter(VitalRecordAllMask.pid==pid).order_by(desc(VitalRecordAllMask.p_record_seq)).first()
    dict_mask=mask_raw2.__dict__
    df_mask=pd.DataFrame([dict_mask])
    df_mask_droped=df_mask.drop(COLS,axis=1,inplace=False)
    df_mask_droped.drop('_sa_instance_state',axis=1,inplace=True)
    df_merged_vital=pd.DataFrame([merged_dict]).copy()
    df_merged_vital.drop(['sepsis_in_six','sepsis_percent'],axis=1,inplace=True)
    df_vital_mask=pd.concat([df_merged_vital,df_mask_droped],axis=1)
    dict_vital_mask=df_vital_mask.to_dict('records')[0].copy()
    vital_mask_insert=VitalRecordAllMask(**dict_vital_mask)
    session.add(vital_mask_insert)
    session.commit()
  else:#lab data??? ?????????~
      # -----------------vital_record_all ????????? ??????--------------------------
    lab_list=[]
    df_vi=pd.DataFrame([vital_dict])
    lab_list=[]
    for col in COLS:
      lab_list.append([col_stat[col]['median']])  # [] ??????
    df_median=pd.DataFrame(lab_list).T
    df_median.columns=COLS
    df_medi_droped=df_median.drop(v_insert_list,axis=1,inplace=False).copy()
    df_merged=pd.concat([df_vi,df_medi_droped],axis=1)
    merged_dict = df_merged.to_dict(orient='records')[0]
    vital_insert=VitalRecordAll(**merged_dict)
    session.add(vital_insert)
    session.commit()

    # ------------------vital_record_all_mask ????????? ??????------------  ~~~~~~~~???????????? ???????????? ????????????!!~~~~~~~~~~~~
    # ????????? record_all ?????? ????????????
    latest_raw=session.query(VitalRecordAll).filter(VitalRecordAll.pid == pid).order_by(desc(VitalRecordAll.p_record_seq)).first()
    dict_latest_raw=latest_raw.__dict__
    df_latest=pd.DataFrame([dict_latest_raw])
    df_latest.drop('_sa_instance_state',axis=1,inplace=True)
    df_droped=df_latest.drop(lab_cols2,axis=1,inplace=False)

    # pid?????? null?????? ????????? lab ????????? ??????!
    dict_null={'pid':pid}
    lab_null=LabData(**dict_null)
    dict_lab_null=lab_null.__dict__
    df_lab_null=pd.DataFrame([dict_lab_null])
    # merge data ???????????? mask ???????????????
    df_null_merged=pd.merge(df_droped,df_lab_null,on='pid',how='outer')
    df_masks = pd.DataFrame()
    MASK_COLS = [x+'_mask' for x in COLS]
    for col in COLS:
        # ?????? column?????? NaN??? ?????? ?????? index??? True???, NaN?????? False??? ??????
        df_masks[col+'_mask'] = df_null_merged[col].notnull().astype(int)
    # ?????? mask column??? ???????????? ????????? DataFrame?????? ??????
    df_masks = pd.concat([df_masks[x] for x in MASK_COLS], axis=1)
    df_droped[df_masks.columns]=df_masks
    # df_filled??? df_masks??? merge
    df_null_merged_mask = df_droped
    df_null_merged_dict=df_null_merged_mask.iloc[0].to_dict()
#   VitalRecordAllMask ???????????? primary key??? 'pid'??? 'p_record_seq' ?????? ????????? ???????????????
# -------------vital_record_all_mask ????????????~-----------------
    sub_mask = VitalRecordAllMask(**df_null_merged_dict)
    session.add(sub_mask)
    session.commit()
    # ?????? 30?????? ??????!            ~~~~~~~??? ??????????????? ???????????? ??????????????????!~~~~~~~~~~~~
    # model ?????? ?????? ??? ??????????????? ????????????
  return pid


