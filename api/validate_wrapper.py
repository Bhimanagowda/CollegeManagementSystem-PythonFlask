from functools import wraps
from flask import request, jsonify
from jsonschema import validate, ValidationError

def schema_validate(schema):
    """Decorator to validate request payload against a schema."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                validate(instance=request.get_json(), schema=schema)
            except ValidationError as e:
                return {"success": False, "message": f"Validation error: {e.message}"}, 400
            return func(*args, **kwargs)
        return wrapper
    return decorator

def response_schema_validate(schema):
    """Decorator to validate response payload against a schema."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if isinstance(response, tuple):
                response_body, status = response
            else:
                response_body, status = response, 200
            
            if response_body.get("success", False):
                try:
                    validate(instance=response_body, schema=schema)
                except ValidationError as e:
                    return {"success": False, "data": None, "message": f"Response validation error: {e.message}"}, 500
            # try:
            #     validate(instance=response_body, schema=schema)
            # except ValidationError as e:
            #     return {"success": False, "message": f"Response validation error: {e.message}"}, 500
            return response, status
        return wrapper
    return decorator
