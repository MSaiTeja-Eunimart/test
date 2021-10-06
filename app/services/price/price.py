import logging
import time

from app import db
from app.models.rates import Rates
from app.models.zones import Zones
from app.models.services import Services


logger = logging.getLogger(name=__name__)

class Price(object):
    def __init__(self):
        pass

    def data_to_insert(self,master_data, request_data):
        """ return list of elements to be inserted
        Args:
            master_data ([list]): each and every data point in database
            request_data ([list]): data points recived from request thats need to be inserted
        Returns:
            [list]: data points unable in database
        """
        
        return [x for x in request_data if x not in master_data]
    
    def pick_columns(model, columns):
        model_objects = [eval(f'{model.__name__}.{col}') for col in columns]
        return model_objects

    def get_zones(self, as_dic=False, as_list=True, columns=[]):
        if columns:
            colObj = self.pick_columns(Zones, columns)
            data = Zones.query.with_entities(*colObj).all()
        else:
            data = Zones.all()
        
        if as_dic :
            result = {row.name:row.id for row in data}
        
        elif as_list:
            result = [list(row) for row in data]
        else:
            result = [row._asdict() for row in data]
        return result
    
    def get_service(self, as_dic=False, as_list=True, columns=[]):
        if columns:
            colObj = self.pick_columns(Services, columns)
            data = Services.query.with_entities(*colObj).all()
        else:
            data = Services.all()
        
        if as_dic :
            result = {row.services:row.id for row in data}
        
        elif as_list:
            result = [list(row) for row in data]
        else:
            result = [row._asdict() for row in data]
        return result
    
    
    def price_file_upsert(self,df):
        start_time = time.time()
        df_len = len(df.index)
        zones_dic = self.get_zones(as_dic=True)
        
        intra_city_id = zones_dic['Intra City']
        intra_state_id = zones_dic['Intra State']
        metro_id = zones_dic['Metros']
        sdes_id = zones_dic['SDES']
        roi_id = zones_dic['ROI']
        
        # adding service id
        services = df['service'].unique()
        services_dic = self.get_service(as_dic = True)
        unique_service_id = [services_dic[i] for i in services]
        df['service_id'] = df['service'].replace(services,unique_service_id)

        for row in df.itertuples():
            # intra city
            # weight_slab
            intra_city_data = Rates.query.filter_by(zone_id=intra_city_id, service_id=row.service_id, weight=row.weight_slab).first()
            if not intra_city_data:
                insert =  Rates(zone_id=intra_city_id, service_id=row.service_id, weight=row.weight_slab, price=row.intra_city, cod_percentage=None)
                db.session.add(insert)
            else:
                intra_city_data.price = row.intra_city
                intra_city_data.cod_percentage = row.cod_percentage
                intra_city_data.cod = row.min_cod
        
            # intra state
            intra_state_data = Rates.query.filter_by(zone_id=intra_state_id, service_id=row.service_id, weight=row.weight_slab).first()
            if not intra_state_data:
                insert =  Rates(zone_id=intra_state_id, service_id=row.service_id, weight=row.weight_slab, price=row.intra_state, cod_percentage=None)
                db.session.add(insert)
            else:
                intra_state_data.price = row.intra_state
                intra_state_data.cod_percentage = row.cod_percentage
                intra_city_data.cod = row.min_cod
        
            # metro
            metro_data = Rates.query.filter_by(zone_id=metro_id, service_id=row.service_id, weight=row.weight_slab).first()
            if not metro_data:
                insert =  Rates(zone_id=metro_id, service_id=row.service_id, weight=row.weight_slab, price=row.metros, cod_percentage=None)
                db.session.add(insert)
            else:
                metro_data.price = row.metros
                metro_data.cod_percentage = row.cod_percentage
                intra_city_data.cod = row.min_cod

            # sdes
            sdes_data = Rates.query.filter_by(zone_id=sdes_id, service_id=row.service_id, weight=row.weight_slab).first()
            if not sdes_data:
                insert =  Rates(zone_id=sdes_id, service_id=row.service_id, weight=row.weight_slab, price=row.sdes, cod_percentage=None)
                db.session.add(insert)
            else:
                sdes_data.price = row.sdes
                sdes_data.cod_percentage = row.cod_percentage
                intra_city_data.cod = row.min_cod

            # roi
            roi_data = Rates.query.filter_by(zone_id=roi_id, service_id=row.service_id, weight=row.weight_slab).first()
            if not roi_data:
                insert =  Rates(zone_id=roi_id, service_id=row.service_id, weight=row.weight_slab, price=row.roi, cod_percentage=None)
                db.session.add(insert)
            else:
                roi_data.price = row.roi
                roi_data.cod_percentage = row.cod_percentage
                intra_city_data.cod = row.min_cod

            db.session.commit()

        end_time = time.time()
        time_taken = end_time - start_time
        time_taken_each_insertion = time_taken/df_len
        print('start_time',start_time)
        print('end_time',end_time)
        print('time_taken',time_taken)
        print('time_taken_each_insertion',time_taken_each_insertion)                      

            
PriceOperations = Price()