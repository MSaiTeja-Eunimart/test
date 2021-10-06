import logging
import time

from app import db
from app.models.cities import Cities
from app.models.services import Services
from app.models.pincodes import Pincodes
from app.models.shipping_partners import ShippingPartners
from app.models.shipping_partner_service_mapping import ShippingPartnerServiceMapping
from app.models.aggregators import Aggregators
from app.models.areas_served import AreaServed

logger = logging.getLogger(name=__name__)


class Masterdata(object):

    def __init__(self):
        pass
        
    def data_to_insert(self, master_data, request_data):
        """ return list of elements to be inserted
        Args:
            master_data ([list]): each and every data point in database
            request_data ([list]): data points recived from request thats need to be inserted
        Returns:
            [list]: data points unable in database
        """
        return [x for x in request_data if x not in master_data]
        # return list(set(request_data) - set(master_data))

    def pick_columns(self, model, columns):
        model_objects = [eval(f'{model.__name__}.{col}') for col in columns]
        return model_objects
        
    def get_service(self, as_dic=False, as_list=False, as_list_o_list=False, columns=[], filters=[], index=0):
        if columns:
            colObj = self.pick_columns(Services, columns)
            data = Services.query.with_entities(*colObj).all()
        else:
            data = Services.all()
        
        if as_dic :
            result = {row.services:row.id for row in data}
        
        elif as_list:
            result = [list(row)[index] for row in data]
                
        elif as_list_o_list:
            result = [list(row) for row in data]

        else:
            result = [row._asdict() for row in data]
        return result

    def get_cities(self, as_dic=False, as_list=False, as_list_o_list=False, columns=[], filters=[], index=0):
        if columns:
            colObj = self.pick_columns(Cities, columns)
            data = Cities.query.with_entities(*colObj).all()
        else:
            data = Cities.all()
        
        if as_dic :
            result = {row.name:row.id for row in data}
        
        elif as_list:
            result = [list(row)[index] for row in data]
        
        elif as_list_o_list:
            result = [list(row) for row in data]

        else:
            result = [row._asdict() for row in data]
        return result
        
    def get_shipping_partners(self, as_dic=False, as_list=False, as_list_o_list=False, columns=[], filters=[], index=0):
        if columns:
            colObj = self.pick_columns(ShippingPartners, columns)
            data = ShippingPartners.query.with_entities(*colObj).all()
        else:
            data = ShippingPartners.all()
        
        if as_dic :
            result = {row.name:row.id for row in data}
        
        elif as_list:
            result = [list(row)[index] for row in data]
        
        elif as_list_o_list:
            result = [list(row) for row in data]

        else:
            result = [row._asdict() for row in data]
        return result
            
    def get_aggregators(self, as_dic=False, as_list=False, as_list_o_list=False, columns=[], filters=[], index=0):
        if columns:
            colObj = self.pick_columns(Aggregators, columns)
            data = Aggregators.query.with_entities(*colObj).all()
        else:
            data = Aggregators.all()
        
        if as_dic :
            result = {row.aggregator_name:row.id for row in data}
        
        elif as_list:
            result = [list(row)[index] for row in data]
        
        elif as_list_o_list:
            result = [list(row) for row in data]

        else:
            result = [row._asdict() for row in data]
        return result

    def get_pincodes(self, as_dic=False, as_list=False, as_list_o_list=False, columns=[], filters=[], index=0):
        if columns:
            colObj = self.pick_columns(Pincodes, columns)
            data = Pincodes.query.with_entities(*colObj)
        else:
            data = Pincodes
        
        if filters:
            data = data.filter(*filters)
        
        data = data.all()
        
        if as_dic :
            result = {row.pincode:row.id for row in data}
        
        elif as_list:
            result = [list(row)[index] for row in data]
        
        elif as_list_o_list:
            result = [list(row) for row in data]
        
        else:
            result = [row._asdict() for row in data]
        return result

    def get_shipping_partner_service_mapping(self, as_dic=False, as_list=False, as_list_o_list=False, columns=[], filters=[], index=0):
        if columns:
            colObj = self.pick_columns(ShippingPartnerServiceMapping, columns)
            data = ShippingPartnerServiceMapping.query.with_entities(*colObj).all()
        else:
            data = ShippingPartnerServiceMapping.all()
        
        if as_dic :
            result = {}
        
        elif as_list:
            result = [list(row)[index] for row in data]
        
        elif as_list_o_list:
            result = [list(row) for row in data]

        else:
            result = [row._asdict() for row in data]
        return result
        
    def insert_services(self,services):   
        print('insert services...')
        master_data = self.get_service(as_list=True, columns=['services'])
        services = self.data_to_insert(master_data, services)
        for service in services:
            print(f'inserting service: {service}')
            insert =  Services(services = service)
            db.session.add(insert)
        db.session.commit()
        print("insert services --> completed")
        return self.get_service(as_dic = True)

    def insert_cities(self,cities):
        print('insert cities...')
        master_data = self.get_cities(as_list=True, columns=['name'])
        cities = self.data_to_insert(master_data, cities)
        for citie in cities:
            print(f'inserting city: {citie}')
            insert =  Cities(name = citie)
            db.session.add(insert)
        db.session.commit()
        print("insert cities --> completed")
        return self.get_cities(as_dic = True)
    
    def insert_shipping_partners(self, shipping_partners):
        print('insert shipping partners...')
        master_data = self.get_shipping_partners(as_list=True, columns=['name'])
        shipping_partners = self.data_to_insert(master_data, shipping_partners)
        for shipping_partner in shipping_partners:
            print(f'inserting shipping partner: {shipping_partner}')
            insert =  ShippingPartners(name = shipping_partner)
            db.session.add(insert)
        db.session.commit()
        print("insert shipping partner --> completed")
        return self.get_shipping_partners(as_dic = True)
    
    def insert_aggregators(self,aggregators):
        print('insert aggregators...')
        master_data = self.get_aggregators(as_list=True, columns=['aggregator_name'])
        aggregators = self.data_to_insert(master_data, aggregators)
        for aggregator in aggregators:
            print(f'inserting aggregator: {aggregator}')
            insert =  Aggregators(aggregator_name = aggregator)
            db.session.add(insert)
        db.session.commit()
        print("insert aggregators --> completed")
        return self.get_aggregators(as_dic = True)

    def insert_pincodes(self, df):
        print('insert pincodes...')
        pincodes = df['pincode'].unique()
        no_pincode = len(pincodes)
        min_pincode = min(pincodes)
        max_pincode = max(pincodes)
        filters = []            
        if (int(max_pincode) - int(min_pincode)) < no_pincode:
            print('with max and min logic')
            filters.append(Pincodes.pincode >= min_pincode)
            filters.append(Pincodes.pincode <= max_pincode)
        else:
            print('list logic')
            filters.append(Pincodes.pincode.in_(list(pincodes)))

        master_data = self.get_pincodes(as_list=True, columns=['pincode'], filters=filters)
        
        pincodes = self.data_to_insert(master_data, pincodes)
        df = df[df['pincode'].isin(pincodes)]
        for row in df.itertuples():
            print(f'inserting pincode: {row.pincode}')
            insert =  Pincodes(pincode=row.pincode, state_name=row.state, city_name=row.city)
            db.session.add(insert)
        db.session.commit()
        print("insert pincodess --> completed")
        return df
                
    def insert_shipping_partner_service_mapping(self, df):
        print('insert shipping partner service mapping...')
        master_data = self.get_shipping_partner_service_mapping(as_list_o_list=True, columns=['service_id','aggregator_id','shipping_partner_id'])
        
        df1 = df[['service_id','aggregator_id','shipping_partner_id']].drop_duplicates()
        insert_data = df1.values.tolist()
        df1 = df[['service_id','aggregator_id','shipping_partner_id','pincode','pickup','delivery','cod_delivery','reverse_pickup']]
        df1['shipping_partner_service_mapping_id'] = ''
        insert_data = self.data_to_insert(master_data, insert_data)
        unique_data = [list(x) for x in set(tuple(x) for x in insert_data)]
        
        for row in unique_data:
            print(f'inserting shipping partner service mapping: {row[0]},{row[1]},{row[2]}')
            insert =  ShippingPartnerServiceMapping(service_id=row[0], aggregator_id=row[1], shipping_partner_id=row[2], is_part_of_aggregator=1)
            db.session.add(insert)
            db.session.commit()    
            shipping_partner_service_mapping_id = insert.id
            print(shipping_partner_service_mapping_id)
            df1.loc[(df1.service_id == row[0]) & (df1.aggregator_id == row[1]) & (df1.shipping_partner_id == row[2]), "shipping_partner_service_mapping_id"] = shipping_partner_service_mapping_id
        print("insert shipping partner service mapping --> completed")
        df1 = df1[~df1['shipping_partner_service_mapping_id'].isin([''])]
        return df1
    
    def insert_area_served(self, df):
        print('insert area served mapping...')
        for row in df.itertuples():
            print(f'mapping pincodes id {row.pincode}, shipping partner service {row.shipping_partner_service_mapping_id}')
            insert = AreaServed(pincodes_id=row.pincode, shipping_partner_service_mapping_id=row.shipping_partner_service_mapping_id, pickup=row.pickup, delivery=row.delivery, cod=row.cod_delivery, prepaid = False, return_shipment=row.reverse_pickup)
            db.session.add(insert)
        db.session.commit()
        print("insert area served mapping --> completed")
        return df
    
    def master_file_insert(self, df):
        start_time = time.time()
        df_len = len(df.index)
        
        # services
        services = df['service'].unique()
        services_dic = self.insert_services(services)
        print(services_dic)

        # adding service id
        unique_service_id = [services_dic[i] for i in services]
        df['service_id'] = df['service'].replace(services,unique_service_id)

        
        # shipping partners
        shipping_partners = df['shipping_partner'].unique()
        shipping_partners_dic = self.insert_shipping_partners(shipping_partners)
        print(shipping_partners_dic)

        # adding shipping partners id
        unique_shipping_partner_id = [shipping_partners_dic[i] for i in shipping_partners]
        df['shipping_partner_id'] = df['shipping_partner'].replace(shipping_partners,unique_shipping_partner_id)

        # aggregators
        df['aggregator'] = df['shipping_partner'] + '_' + df['sub_shipping_partner']
        adf = df[['shipping_partner','sub_shipping_partner','aggregator']].drop_duplicates()
        aggregators = adf['aggregator'].unique()
        aggregators_dic = self.insert_aggregators(aggregators)
        print(aggregators_dic)

        # adding aggregators id
        unique_aggregator_id = [aggregators_dic[i] for i in aggregators]
        df['aggregator_id'] = df['aggregator'].replace(aggregators,unique_aggregator_id)

        # pincode
        self.insert_pincodes(df)
        pincodes = df['pincode'].unique()
        
        # shipping partner service mapping
        mdf = self.insert_shipping_partner_service_mapping(df)
        
        # area served
        mdf = self.insert_area_served(mdf)
        

        end_time = time.time()
        time_taken = end_time - start_time
        time_taken_each_insertion = time_taken/df_len
        print('start_time',start_time)
        print('end_time',end_time)
        print('time_taken',time_taken)
        print('time_taken_each_insertion',time_taken_each_insertion)                      
        return {"status": True}

MasterDataOperations = Masterdata()



