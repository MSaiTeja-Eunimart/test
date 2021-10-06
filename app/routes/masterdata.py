import logging
import pandas as pd
from flask import Blueprint, jsonify, request

from app.services.masterdata import MasterDataOperations

masterdata = Blueprint('masterdata', __name__)

logger = logging.getLogger(__name__)

@masterdata.route('/masterdata/bulk_insert', methods=['POST'])
def bulk_insert():
    
    file = request.files.get('file')
    file_name = file.filename
    if file_name.split('.')[-1] in ['xlsx', 'xls']:
        df = pd.read_excel(file)
    elif file_name.split('.')[-1] == 'csv':
        df = pd.read_csv(file)
    else:
        return 0 # need to add responce later
    
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.lower())
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    df['pickup'] = df['pickup'].replace(['yes',1,'1','no',0,'0',None],[True,True,True,False,False,False,False])
    df['delivery'] = df['delivery'].replace(['yes',1,'1','no',0,'0',None],[True,True,True,False,False,False,False])
    df['cod_delivery'] = df['cod_delivery'].replace(['yes',1,'1','no',0,'0',None],[True,True,True,False,False,False,False])
    df['reverse_pickup'] = df['reverse_pickup'].replace(['yes',1,'1','no',0,'0',None],[True,True,True,False,False,False,False])

    data = MasterDataOperations.master_file_insert(df)
    if not data:
        data = {}
    return jsonify(data)