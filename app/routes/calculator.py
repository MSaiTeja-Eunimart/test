import logging
import fastjsonschema

from flask import Blueprint, jsonify, request

from app.routes.validation_schemas.flat_rate_calculator_schema import FlatRateCalculatorSchema
from app.services.calculator import CalculatorOperations

calculator = Blueprint('calculator', __name__)

logger = logging.getLogger(__name__)


@calculator.route('/calculator/flat_rate_calculator', methods=['POST'])
def flat_rate_calculator():
    request_data = request.get_json()
    request_body = request_data.get("data")
    shipment_mode = request_body.get("mode")
    payment_mode = request_body.get("payment")

    # change shipment mode to upper case
    if shipment_mode:
        shipment_mode = shipment_mode.upper()
        request_body['mode'] = shipment_mode

    if payment_mode:
        payment_mode = payment_mode.upper()
        request_body['payment'] = payment_mode

    # validate payload and query params
    fastjsonschema.validate(FlatRateCalculatorSchema, request_data)

    data = CalculatorOperations.flat_rate_calculator(request_body)
    print(data)
    if not data:
        data = {}
    return jsonify(data)
