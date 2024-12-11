from flask import Response, request
from functools import wraps
from loguru import logger
from flask_jwt_extended import get_jwt, verify_jwt_in_request
import casbin
import uuid
import os

# Dynamically set the base path to the current file's directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the paths to the configuration files
model_path = os.path.join(base_dir, "model.conf")
policy_path = os.path.join(base_dir, "policy.csv")

# Ensure configuration files exist
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model configuration file not found: {model_path}")
if not os.path.exists(policy_path):
    raise FileNotFoundError(f"Policy file not found: {policy_path}")

e = casbin.Enforcer(model_path, policy_path)
# logger.info(f"Model path: {model_path}, Policy path: {policy_path}")


def casbin_validate(validate_jwt=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Validate JWT if required
                if validate_jwt:
                    try:
                        verify_jwt_in_request(refresh=False)
                    except Exception as ex:
                        response_code = uuid.uuid4()
                        logger.error(f"{ex} --> response_code: {response_code}")
                        return {'status': 'Failure', 'message': 'Invalid Token', 'response_code': str(response_code)}, 400

                # Extract claims and user info
                sub = get_jwt()['usertype']
                # sub = claims.get('usertype', None)  # Extract user type
                obj = request.path  # Resource being accessed
                act = request.method  # HTTP method
                
                result = e.enforce(sub, obj, act)
                logger.info(f"Casbin Enforce Result: {result}, Sub: {sub}, Obj: {obj}, Act: {act}")

                # # Log request details
                # logger.info(f"Path --> {obj}, Action --> {act}, Usertype --> {sub}")

                # Enforce access control with Casbin
                if e.enforce(sub, obj, act):
                    return func(*args, **kwargs)
                else:
                    logger.warning(f"Access Denied for Path: {obj}, Action: {act}, Usertype: {sub}")
                    return {'status': 'Failure', 'message': 'Access Denied'}, 403
            except Exception as err:
                response_code = uuid.uuid4()
                logger.error(f"Error --> {repr(err)} ResponseCode --> {response_code}")
                return {'status': 'Failure', 'message': 'Access Denied'}, 403
        return wrapper
    return decorator
