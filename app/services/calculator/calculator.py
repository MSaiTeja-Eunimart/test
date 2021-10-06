from app import models
from app.models import zones
from app.models.zones import Zones
from app.models.services import Services
from sqlalchemy.orm import aliased
import logging
import math

from app import db

from app.models.states_pincode_prefix import StatesPincodePrefix
from app.models.metros import Metros
from app.models.metros_pincode_prefix import MetrosPincodePrefix
from app.models.areas_served import AreaServed
from app.models.shipping_partner_service_mapping import ShippingPartnerServiceMapping
from app.models.shipping_partners import ShippingPartners
from app.models.rates import Rates
from app.models.special_destinations import SpecialDestinations
logger = logging.getLogger(name=__name__)

# from sqlalchemy import select, join


class Calculator(object):

    zone_dic = {
        "INTRA-CITY": "intra_city",
        "INTRA-STATE": "intra_state",
        "METROS": "metros",
        "PINCODE-NOT-VALID": None,
        "SDES": "sdes",
        "ROI": "roi"
    }
    
    def __init__(self):
        pass

    def to_dic(self,data):
        data = [row._asdict() for row in data]
        if len(data) == 1:
            return data[0]
        else:
            return data
    
    def get_zone(self, origin_pincode, destination_pincode):
                
        zone = None
        
        # same pincode check
        if origin_pincode == destination_pincode:
            return 'INTRA-CITY'
         
        origin_metro = db.session.query(MetrosPincodePrefix.metro_city_id)\
                        .join(Metros, Metros.id == MetrosPincodePrefix.metro_city_id)\
                        .filter(MetrosPincodePrefix.metro_prefix_code == origin_pincode[:3])\
                        .all()
        destination_metro = db.session.query(MetrosPincodePrefix.metro_city_id)\
                        .join(Metros, Metros.id == MetrosPincodePrefix.metro_city_id)\
                        .filter(MetrosPincodePrefix.metro_prefix_code == destination_pincode[:3])\
                        .all()
        if origin_metro and destination_metro:
            if origin_metro == destination_metro:
                return 'INTRA-CITY'
            else:
                return 'METROS'
        
        # getting state ids from pincodes
        origin_state_id = db.session.query(StatesPincodePrefix.state_id)\
                        .filter(StatesPincodePrefix.state_prefix == origin_pincode[:3])\
                        .all()
        destination_state_id = db.session.query(StatesPincodePrefix.state_id)\
                        .filter(StatesPincodePrefix.state_prefix == destination_pincode[:3])\
                        .all()
        if not origin_state_id:
            origin_state_id = db.session.query(StatesPincodePrefix.state_id)\
                        .filter(StatesPincodePrefix.state_prefix == origin_pincode[:2])\
                        .all()
        if not destination_state_id:
            destination_state_id = db.session.query(StatesPincodePrefix.state_id)\
                        .filter(StatesPincodePrefix.state_prefix == destination_pincode[:2])\
                        .all()
        
        if not origin_state_id or not destination_state_id:
            return "PINCODE-NOT-VALID"

        # SDES zone check
        origin_sdes_id = db.session.query(SpecialDestinations.state_id)\
                        .filter(SpecialDestinations.state_id == origin_state_id)\
                        .all()
        destination_sdes_id = db.session.query(SpecialDestinations.state_id)\
                        .filter(SpecialDestinations.state_id == destination_state_id)\
                        .all()
        
        if origin_sdes_id or destination_sdes_id:
            return "SDES"
    
        if origin_state_id == destination_state_id and origin_pincode[2] == destination_pincode[2]:
            return "INTRA-CITY"
        elif origin_state_id ==  destination_state_id:
            return "INTRA-STATE"
        else:
            return "ROI"

    def calculate_weight(self, actual_weight, length, height, width, mode):
        if mode == "EXPRESS":
            volume_weight = (length * height * width)/ 5000
            if actual_weight > volume_weight:
                return actual_weight
            else:
                return volume_weight
        
        elif mode == "STANDARD":
            volume_weight = (length * height * width)/ 4000
            if actual_weight > volume_weight:
                return actual_weight
            else:
                return volume_weight
            
    def get_service_availability(self, origin_pincode, destination_pincode, service_mode, payment_mode):
        service_mode  = service_mode.strip().lower()
        AreaServed2 = aliased(AreaServed, name='parent_device')
        if payment_mode == "COD":
            cod = True
            prepaid = False
        elif payment_mode == "PREPAID":
            cod = False
            prepaid = True

        origin_data = db.session.query(AreaServed.id.label("area_serverd_id"), ShippingPartnerServiceMapping.id.label("shipping_partner_service_mapping_id"), ShippingPartners.name)\
                        .join(ShippingPartnerServiceMapping, ShippingPartnerServiceMapping.id == AreaServed.shipping_partner_service_mapping_id)\
                        .join(ShippingPartners, ShippingPartners.id == ShippingPartnerServiceMapping.shipping_partner_id)\
                        .join(Services, Services.id == ShippingPartnerServiceMapping.service_id)\
                        .filter(AreaServed.pincodes_id == origin_pincode, AreaServed.pickup == True, Services.services == service_mode, AreaServed.cod == cod, AreaServed.prepaid == prepaid)\
                        .all()
        origin_data = {row.shipping_partner_service_mapping_id: row._asdict() for row in origin_data}
        destination_data = db.session.query(AreaServed.id.label("area_serverd_id"), ShippingPartnerServiceMapping.id.label("shipping_partner_service_mapping_id"), ShippingPartners.name)\
                        .join(ShippingPartnerServiceMapping, ShippingPartnerServiceMapping.id == AreaServed.shipping_partner_service_mapping_id)\
                        .join(ShippingPartners, ShippingPartners.id == ShippingPartnerServiceMapping.shipping_partner_id)\
                        .join(Services, Services.id == ShippingPartnerServiceMapping.service_id)\
                        .filter(AreaServed.pincodes_id == destination_pincode, AreaServed.pickup == True, Services.services == service_mode, AreaServed.cod == cod, AreaServed.prepaid == prepaid)\
                        .all()
        destination_data = {row.shipping_partner_service_mapping_id: row._asdict() for row in destination_data}
        response  = {}
                
        if origin_data and destination_data:
            service_flag = False
            for o in origin_data:
                if o in destination_data:            
                    response["status"] = True
                    response["message"] = "Service available"
                    service = {}
                    response["data"] =  service # will look into it later
                    service_flag = True
                    break
            if not service_flag:
                response["status"] = False
                response["message"] = "Service for destination unavailable"
                response["data"] = {}

        elif origin_data:
            response["status"] = False
            response["message"] = "Service for destination unavailable"
            response["data"] = {}
        
        elif destination_data:
            response["status"] = False
            response["message"] = "Service from sorce/origin unavailable"
            response["data"] = {}
        
        else:
            response["status"] = False
            response["message"] = "Service from sorce/origin and destination unavailable"
            response["data"] = {}
        return response
    
    def get_price(self, zone, weight, payment, mode):
        if weight < 0.5:
            weight = 0.5
        else:
            weight = math.ceil(weight)
        if payment == "PREPAID":
            price = db.session.query(Rates.price)\
                        .join(Services, Services.id == Rates.service_id)\
                        .join(Zones, Zones.id == Rates.zone_id)\
                        .filter(Rates.weight == weight, Zones.slug == zone, Services.services == mode)\
                        .all()
        elif payment == "COD":
            price = db.session.query(Rates.price, Rates.cod, Rates.cod_percentage)\
                        .join(Services, Services.id == Rates.service_id)\
                        .join(Zones, Zones.id == Rates.zone_id)\
                        .filter(Rates.weight == weight, Zones.slug == zone, Services.services == mode)\
                        .all()            
        return self.to_dic(price)

    def flat_rate_calculator(self,request_data):
        response = {}
        origin_pincode = request_data.get("origin_pincode")
        destination_pincode = request_data.get("destination_pincode")
        weight = request_data.get("weight")
        mode = request_data.get("mode")
        payment = request_data.get("payment")
        package_details = request_data.get("package_details")
        length = package_details.get("length")
        height = package_details.get("height")
        width = package_details.get("width")

        # checking service availability
        service_details = self.get_service_availability(origin_pincode, destination_pincode, mode, payment)
        if not service_details["status"]:
            return service_details
        
        # finding zone category
        zone = self.get_zone(origin_pincode, destination_pincode)
        if not zone:
            response["status"] = False
            response["message"] = "Invalid pincodes or service unavailable"
        else:
            response["zone"] = zone
            zone = self.zone_dic[zone]
            weight = self.calculate_weight(weight, length, height, width, mode)
            price = self.get_price(zone, weight, payment, mode)
            
            if not price:
                response["status"] = False
                response["message"] = "service available but price data is not available"
                
            else:
                gst_percentage = '18%'
                shipping_charges = math.ceil(price['price'] - (price['price']/1.18))
                response["message"] = "service available"

                if payment == "PREPAID":
                    gst_amount = math.ceil(shipping_charges * 0.18)
                    total_amount = shipping_charges + gst_amount            
                    response["status"] = True
                    response["gst_percentage"] = gst_percentage
                    response["shipping_charges"] = shipping_charges
                    response["gst_amount"] = gst_amount
                    response["total_amount"] = total_amount
                
                elif payment == "COD":
                    declared_value = request_data.get("declared_value")
                    if price['cod'] > shipping_charges * price['cod_percentage']:
                        cod_charges = math.ceil(price['cod'])
                    else:
                        cod_charges = math.ceil(shipping_charges * price['cod_percentage'])

                    gst_amount = math.ceil((shipping_charges + cod_charges) * 0.18)
                    total_amount = shipping_charges + cod_charges + gst_amount + declared_value          
                    response["status"] = True
                    response["gst_percentage"] = gst_percentage
                    response["shipping_charges"] = shipping_charges
                    response["cod_charges"] = cod_charges
                    response["gst_amount"] = gst_amount
                    response["declared_value"] = declared_value
                    response["total_amount"] = total_amount
        return response

CalculatorOperations = Calculator()