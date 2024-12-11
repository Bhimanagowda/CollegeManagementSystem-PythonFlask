from flask import Response, request
from functools import wraps
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt
from jsonschema import Draft7Validator
import uuid
import casbin
import os
from loguru import logger

# Dynamically set the base path to the current file's directory
base_dir = os.path.dirname(os.path.abspath(__file__))  # Points to the `api` folder

# Construct the paths to the configuration files
model_path = os.path.join(base_dir, "model.conf")
policy_path = os.path.join(base_dir, "policy.csv")

# Ensure configuration files exist
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model configuration file not found: {model_path}")
if not os.path.exists(policy_path):
    raise FileNotFoundError(f"Policy file not found: {policy_path}")

e = casbin.Enforcer(model_path, policy_path)

def jwt_validate(schema, refresh=False):
    """
    Decorator to validate JWT and perform optional schema validation.
    :param schema: JSON schema to validate claims against.
    :param refresh: Whether the token is a refresh token.
    :return: The decorated function or an error response if validation fails.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Verify JWT in request and extract claims
                verify_jwt_in_request(refresh=refresh)
                claims = get_jwt()
                logger.info(f"JWT Claims: {claims}")

                # Ensure 'sub' is a string (check if it's present and convert)
                sub = claims.get('sub', None)
                if sub is None:
                    response_code = uuid.uuid4()
                    logger.error(f"Missing 'sub' in JWT claims --> Response Code: {response_code}")
                    return {'status': 'Failure', 'message': 'Missing subject (sub)', 'responseCode': str(response_code)}, 400

                # Convert 'sub' to string if it's not already
                claims['sub'] = str(sub)

                # Validate claims against the provided schema
                validator = Draft7Validator(schema)
                errors = sorted(validator.iter_errors(claims), key=lambda e: e.path)

                # If there are schema validation errors, return an error response
                if errors:
                    error_message = "\n".join([error.message for error in errors])
                    response_code = uuid.uuid4()
                    logger.info(f"Schema Validation Errors: {error_message} --> Response Code: {response_code}")
                    return {'status': 'Failure', 'message': 'Invalid Token', 'responseCode': str(response_code)}, 400
                
                # If validation is successful, proceed with the original function
                return func(*args, **kwargs)
            except Exception as e:
                # Log any exceptions that occur
                response_code = uuid.uuid4()
                logger.error(f"Error occurred: {e} --> Response Code: {response_code}")
                return {'status': 'Failure', 'message': 'Invalid Token', 'responseCode': str(response_code)}, 400
                
        return wrapper
    return decorator

def jwt_validatenew(schema=None, refresh=False):
    """
    Decorator to validate JWT tokens and optionally validate claims against a JSON schema.
    :param schema: JSON schema to validate claims against (optional).
    :param refresh: Boolean indicating whether to validate a refresh token.
    :return: Decorated function or an error response if validation fails.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Verify JWT in the request
                verify_jwt_in_request(refresh=refresh)
                claims = get_jwt()
                logger.info(f"JWT Claims: {claims}")

                # Ensure 'sub' exists in the token
                sub = claims.get('sub')
                if not sub:
                    response_code = uuid.uuid4()
                    logger.error(f"Missing 'sub' in JWT claims --> Response Code: {response_code}")
                    return {
                        "status": "Failure",
                        "message": "Missing subject (sub) in token",
                        "responseCode": str(response_code)
                    }, 400

                # Validate claims against the provided schema, if applicable
                if schema:
                    validator = Draft7Validator(schema)
                    errors = sorted(validator.iter_errors(claims), key=lambda e: e.path)

                    if errors:
                        error_messages = [f"{'/'.join(map(str, e.path))}: {e.message}" for e in errors]
                        response_code = uuid.uuid4()
                        logger.error(f"Schema Validation Errors: {error_messages} --> Response Code: {response_code}")
                        return {
                            "status": "Failure",
                            "message": "Invalid Token claims",
                            "errors": error_messages,
                            "responseCode": str(response_code)
                        }, 400

                # Proceed with the decorated function
                return func(*args, **kwargs)

            except Exception as e:
                response_code = uuid.uuid4()
                logger.error(f"Error during JWT validation: {e} --> Response Code: {response_code}")
                return {
                    "status": "Failure",
                    "message": "Token validation failed",
                    "error": str(e),
                    "responseCode": str(response_code)
                }, 400

        return wrapper
    return decorator

def jwt_Manager(app):
    """
    Initialize and configure the JWT Manager for the app.
    :param app: The Flask app instance.
    :return: JWTManager instance.
    """
    return JWTManager(app)

