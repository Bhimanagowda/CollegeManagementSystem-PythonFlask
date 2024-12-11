from models import CollegeAdmin,Teacher, StudentPersonalDetails
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import timedelta
from flask import request
from flask_restful import Resource

class AdminLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_id=data.get("user_id")
            admin_name = data.get("admin_name")
            password=data.get("password")
            usertype = data.get("usertype")
            
            
            if not all([user_id,admin_name,password,usertype]):
                return {"message": "All fields are required (user_id,name,password & usertype)"}, 400
            
            if usertype == "Admin":
                collegeadmin = CollegeAdmin.query.filter_by(id=user_id).first()
                if collegeadmin is None:
                    return {"message": "Admin not found"}, 404
                if collegeadmin.admin_name != admin_name:
                    return{"message":"admin is invalid"}
                if collegeadmin.password != password:
                    return{"message":"Password is wrong"}

                identity = {"usertype": usertype, "name": collegeadmin.admin_name}
            
            else:
                return {"message": "Invalid college usertype ."}, 400

            # Generate access and refresh tokens
            access_token = create_access_token(identity=str(user_id),additional_claims=identity, expires_delta=timedelta(minutes=60))
            refresh_token = create_refresh_token(identity=str(user_id),additional_claims=identity, expires_delta=timedelta(days=7))

            return {
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
        
            
class TeacherLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_id=data.get("user_id")
            usertype = data.get("usertype")
            name = data.get("name")
            password = data.get("password")
            
            if not all([user_id,name, password, usertype]):
                return {"message": "All fields are required (user_id,name, password, usertype)"}, 400
            
            # Query the teacher table for the given usertype
            if usertype == "Teacher":
                teacher = Teacher.query.filter_by(id=user_id,usertype="Teacher").first()
                if teacher is None:
                    return {"message": "Teacher not found"}, 404
                if teacher.name != name:
                    return {"message": "Invalid teacher name"}, 401
                if teacher.password != password:
                    return {"message": "Teacher Password mismatch"}, 401

                identity = { "usertype":usertype,"name": teacher.name }
            
            elif usertype == "HOD":
                hod = Teacher.query.filter_by(id=user_id,usertype="HOD").first()
                if not hod:
                    return {"message": "HOD not found"}, 404
                if hod.name != name:
                    return {"message": "Invalid HOD name"}, 401
                if hod.password != password:
                    return {"message": "HOD Password mismatch"}, 401

                identity = {"usertype": usertype, "name": hod.name}
            
            else:
                return {"message": "Invalid usertype provided"}, 400

            # Generate access and refresh tokens
            access_token = create_access_token(identity=str(user_id),additional_claims=identity,  expires_delta=timedelta(minutes=60))
            refresh_token = create_refresh_token(identity=str(user_id),additional_claims=identity,  expires_delta=timedelta(days=7))
            return {
                "message": "login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500
    
class StudentLogin(Resource):
    def post(self):
        try:
            data = request.get_json()
            user_id=data.get("user_id")
            usertype = data.get("usertype")
            name = data.get("name")
            password=data.get("password")
            
            
            if not all([user_id,usertype,name,password]):
                return {"message": "All fields are required (user_id, usertype,name, password)"}, 400

            if usertype == "Student":
                student = StudentPersonalDetails.query.filter_by(id=user_id).first()
                if student is None:
                    return {"message": "Student not found"}, 404
                if student.name != name:
                    return {"message": "Student Password mismatch"}, 401
                if student.password != password:
                    return {"message": "Student Password mismatch"}, 401

                identity = {"usertype": usertype, "name": student.student_name}
                
            else:
                return {"message": "Invalid 'Student' user type."}, 400

            # Generate access and refresh tokens
            access_token = create_access_token(identity=str(user_id),additional_claims=identity,  expires_delta=timedelta(minutes=60))
            refresh_token = create_refresh_token(identity=str(user_id),additional_claims=identity,  expires_delta=timedelta(days=7))

            return {
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200

        except Exception as e:
            return {"message": f"An error occurred: {str(e)}"}, 500

