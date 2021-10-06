import logging
import pandas as pd
from flask import Blueprint, jsonify, request

from app.services.price import PriceOperations


price = Blueprint('price', __name__)

logger = logging.getLogger(__name__)

@price.route('/price/bulk_insert', methods=['POST'])
def bulk_insert():
    
    file = request.files.get('file')
    file_name = file.filename
    if file_name.split('.')[-1] in ['xlsx', 'xls', 'xls']:
        df = pd.read_excel(file)
    elif file_name.split('.')[-1] == 'csv':
        df = pd.read_csv(file)
    else:
        return 0 # need to add responce later
    
    df_obj = df.select_dtypes(['object'])
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())
    df[df_obj.columns] = df_obj.apply(lambda x: x.str.lower())
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]    

    data = PriceOperations.price_file_upsert(df)
    if not data:
        data = {}
    return jsonify(data)
    
