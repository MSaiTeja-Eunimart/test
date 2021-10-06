FlatRateCalculatorSchema = {
    "type": "object",
    "required": ["data"],
    "properties": {
        "data": {
            "type": "object",
            "required": ["origin_pincode", "destination_pincode", "weight", "mode", "package_details", "payment"],
            "properties": {
                "origin_pincode": {
                    "type": "string",
                    "pattern": "^[1-9]{1}[0-9]{2}[0-9]{3}$"
                },
                "destination_pincode": {
                    "type": "string",
                    "pattern": "^[1-9]{1}[0-9]{2}[0-9]{3}$"
                },
                "weight": {
                    "type": "number",
                    "minimum": 0.1
                },
                "mode": {
                    "type": "string",
                    "enum": ["EXPRESS", "STANDARD"]
                },
                "payment": {
                    "type": "string",
                    "enum": ["COD", "PREPAID"]
                },
                "declared_value": {
                    "type": "number",
                    "minimum": 0.1
                },
                "package_details":{
                    "type": "object",
                    "required": ["length", "height", "width"],
                    "properties": {
                        "length": {
                            "type": "number",
                            "minimum": 0.1
                        },
                        "height": {
                            "type": "number",
                            "minimum": 0.1
                        },
                        "width": {
                            "type": "number",
                            "minimum": 0.1
                        }
                    }
                }
            }
        }
    },
    "additionalProperties": False
}
