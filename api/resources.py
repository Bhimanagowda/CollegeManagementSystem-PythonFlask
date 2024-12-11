from datetime import date
from flask import request, jsonify
from flask_jwt_extended import get_jwt
from flask_restful import Resource
from jwt_validation import jwt_validate,jwt_validatenew
from casbin_validate import casbin_validate
from app import db
from models import db,CollegeAdmin,Department,Teacher, StudentPersonalDetails, CourseSubject, Attendance, SubjectMark, AssessmentAssign, AssessmentSubmit
from validate_wrapper import schema_validate,response_schema_validate

from schema import CreateCollegeAdminSchema,CreateDepartmentSchema,CreateTeacherSchema,CreateStudentSchema,CreateAttendanceSchema,CreateAssessmentAssignSchema,CreateAssessmentSubmitSchema,CreateCourseSubjectSchema,ResponseSchema,CollegeAdminAccessTokenSchema,TeacherAccessTokenSchema,AccessTokenSchema,StudentAccessTokenSchema

class CollegeAdminInfo(Resource):
    @response_schema_validate(ResponseSchema)
    def get(self, id=None):
        if id:
            collegeadmin = CollegeAdmin.query.get(id)
            if collegeadmin:
                return {"success":True,"data":collegeadmin.to_dict(),"message":"college retrieved successfully"}
            return {"success":False,"data":None,'message': 'College not found'}, 404
        else:
            collegeadmins = CollegeAdmin.query.all()
            return{"success":True,"data":[collegeadmin.to_dict() for collegeadmin in collegeadmins],"message":"All colleges retrieved successfully"}
    
    @schema_validate(CreateCollegeAdminSchema)
    @response_schema_validate(ResponseSchema)
    def post(self):
        data = request.get_json()
        collegeadmin = CollegeAdmin(**data)
        db.session.add(collegeadmin)
        db.session.commit()
        return {"success":True,"data":collegeadmin.to_dict(),"message":"CollegeInfo added successfully"}
    
    @schema_validate(CreateCollegeAdminSchema)
    @response_schema_validate(ResponseSchema)
    def put(self, id):
        data = request.get_json()
        collegeadmin = CollegeAdmin.query.get(id)
        if not collegeadmin:
            return {'message': 'College not found'}, 404
        for key,value in data.items():
            setattr(collegeadmin,key,value)
        db.session.commit()
        return {"success":True,"data":collegeadmin.to_dict(),"message":"CollegeInfo upate successfully"}
    
    @response_schema_validate(ResponseSchema)
    def delete(self, id):
        collegeadmin = CollegeAdmin.query.get(id)
        if not collegeadmin:
            return {"success":False,"data":None,'message': 'College not found'}, 404
        db.session.delete(collegeadmin)
        db.session.commit()
        return {"success":True,"data":collegeadmin.to_dict(),'message': 'College deleted successfully'}

class DepartmentInfo(Resource):
    @jwt_validate(schema=CollegeAdminAccessTokenSchema)
    @casbin_validate()
    @response_schema_validate(ResponseSchema)
    def get(self, id=None):
        if id:
            department = Department.query.get(id)
            if department:
                return {"success": True,"data": department.to_dict(),"message": "Department retrieved successfully"
                }
            return {"success": False,"data": None,"message": "Department not found"}, 404
        else:
            departments = Department.query.all()
            return {"success": True,"data": [department.to_dict() for department in departments],"message": "All departments retrieved successfully"}

    @jwt_validate(schema=CollegeAdminAccessTokenSchema)
    @casbin_validate()
    @schema_validate(CreateDepartmentSchema)
    @response_schema_validate(ResponseSchema)
    def post(self):
        data = request.get_json()
        department = Department(**data)
        db.session.add(department)
        db.session.commit()
        return { "success": True,"data": department.to_dict(),"message": "Department added successfully"}

    @jwt_validate(schema=CollegeAdminAccessTokenSchema)
    @casbin_validate()
    @schema_validate(CreateDepartmentSchema)
    @response_schema_validate(ResponseSchema)
    def put(self, id):
        data = request.get_json()
        department = Department.query.get(id)
        if not department:
            return {"success": False,"data": None,"message": "Department not found"}, 404

        for key, value in data.items():
            setattr(department, key, value)
        db.session.commit()
        return {
            "success": True,"data": department.to_dict(),"message": "Department updated successfully"}

    @jwt_validate(schema=CollegeAdminAccessTokenSchema)
    @casbin_validate()
    @response_schema_validate(ResponseSchema)
    def delete(self, id):
        department = Department.query.get(id)
        if not department:
            return {"success": False,"data": None,"message": "Department not found"}, 404

        db.session.delete(department)
        db.session.commit()
        return {"success": True,"data": department.to_dict(),"message": "Department deleted successfully"}

# Resource for Teacher
class TeacherInfo(Resource):
    @jwt_validate(schema=CollegeAdminAccessTokenSchema)
    @casbin_validate()
    @response_schema_validate(ResponseSchema)
    def get(self, id=None):
        if id:
            teacher = Teacher.query.get(id)
            if teacher:
                return {"success":True,"data":teacher.to_dict(),'message': 'Teacher retrieved successfully'}
            return {"success":False,"data":None,'message': 'Teacher not found'}, 404
        else:
            teachers = Teacher.query.all()
            return {"success":True,"data":[teacher.to_dict() for teacher in teachers],'message': 'all Teacher retrieved successfully'}

    @jwt_validate(schema=CollegeAdminAccessTokenSchema) 
    @casbin_validate()
    @schema_validate(CreateTeacherSchema)
    @response_schema_validate(ResponseSchema)
    def post(self):
        data = request.get_json()
        
        department_id=data.get("department_id")
        usertype=data.get("usertype")
        
        if usertype == "Teacher":
            hod_exist=Teacher.query.filter_by(department_id=department_id,usertype="HOD").first()
            if not hod_exist:
                return{"success":False,"data":None,"message":"First you need to create HOD for the department,before adding Teacher"}
        
        if usertype == "HOD":
            existing_hod=Teacher.query.filter_by(department_id=department_id,usertype="HOD").first()
            if existing_hod:
                return{"Success":False,"data":None,"message":"1 HOD is alreay in this Department"}
            
        teacher = Teacher(**data)
        db.session.add(teacher)
        db.session.commit()
        return {"success":True,"data":teacher.to_dict(),'message': 'Teacher added successfully'}

    @jwt_validate(schema=CollegeAdminAccessTokenSchema)
    @casbin_validate()
    @schema_validate(CreateTeacherSchema)
    @response_schema_validate(ResponseSchema)
    def put(self, id):
        data = request.get_json()
        usertype=data.get("usertype")
        department_id=data.get("department_id")
        
        if usertype == "HOD":
            exist_hod=Teacher.query.filter_by(department_id=department_id,usertype="HOD").first()
            if exist_hod:
                return{"message":"Only one HOD aloowed per department"}
        teacher = Teacher.query.get(id)
        if not teacher:
            return {"success":False,"data":None,'message': 'Teacher not found'}, 404
        for key,value in data.items():
            setattr(teacher,key,value)
        db.session.commit()
        return {"success":True,"data":teacher.to_dict(),'message': 'Teacher update successfully'}

    @jwt_validate(schema=CollegeAdminAccessTokenSchema)
    @casbin_validate()
    @response_schema_validate(ResponseSchema)
    def delete(self, id):
        teacher = Teacher.query.get(id)
        if not teacher:
            return {"success":False,"data":None,'message': 'Teacher not found'}, 404
        db.session.delete(teacher)
        db.session.commit()
        return {"success":True,"data":teacher.to_dict(),'message': 'Teacher delete successfully'}
      

# Resource for Student Personal Details
class StudentInfo(Resource):
    @jwt_validatenew(schema=AccessTokenSchema)
    @casbin_validate()
    @response_schema_validate(ResponseSchema)
    def get(self, id=None):
    
        claims = get_jwt()
        teacher_id = claims.get("sub")  
        if not teacher_id:
            return {"success": False, "message": "Invalid or missing teacher ID in token"}, 403
    
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {"success": False, "message": "Teacher not found"}, 404
    
        teacher_department = teacher.department_id 
    
        if id:
            student = StudentPersonalDetails.query.get(id)
            if not student:
                return {"success": False, "message": "Student not found"}, 404
    
            if student.department_id != teacher_department:
                return {"success": False, "message": "Unauthorized access: Student belongs to another department"}, 403
    
            return {"success": True, "data": student.to_dict(), "message": "Student retrieved successfully"}, 200
    
        else:
            students = StudentPersonalDetails.query.filter_by(department_id=teacher_department).all()
            if not students:
                return {"success": False, "message": "No students found for your department"}, 404
    
            return {
                "success": True,
                "data": [student.to_dict() for student in students],
                "message": "Students retrieved successfully",
            }, 200
            
    @jwt_validatenew(schema=AccessTokenSchema)
    @casbin_validate()
    @schema_validate(CreateStudentSchema)
    @response_schema_validate(ResponseSchema)
    def post(self):
        claims=get_jwt()
        teacher_id=claims.get('sub')
        if not teacher_id:
            return{"message":"Invalid or missing Teacher id"}
        
        data = request.get_json()
        
        teacher=Teacher.query.get(id)
        if not teacher:
            return{"message":"from db Teacher not found"}
        
        department_id=data.get("department_id")
        if teacher.department_id != department_id:
            return{"message":"Teacher'department is mismatch"}
        
        try:
            student = StudentPersonalDetails(**data)
            db.session.add(student)
            db.session.commit()
            return {"success":True,"data":student.to_dict(),'message': 'student added successfully'}
        except Exception as e:
            return{"Sucess":False,"Message":str(e)}
    
    @jwt_validate(schema=AccessTokenSchema)
    @casbin_validate()
    @schema_validate(CreateStudentSchema)
    @response_schema_validate(ResponseSchema)
    def put(self, id):
        claims=get_jwt()
        teacher_id=claims.get('sub')
        if not teacher_id:
            return{"Message":"Invalid or missing teacher ID's"}
        
        data = request.get_json()
        
        teacher=Teacher.query.get(teacher_id)
        if not teacher:
            return{"message":"Teacher not found"}
        
        department_id=data.get("department_id")
            
        if  teacher.department_id != department_id:
            return{"message":"Unauthorized access: Student belongs to another department"}
        try:
            student = StudentPersonalDetails.query.get(id)
            if not student:
                return {"success":False,"data":None,'message': 'Student not found'}, 404
            for key,value in data.items():
                setattr(student,key,value)
            db.session.commit()
            return {"success":True,"data":student.to_dict(),'message': 'student update successfully'}
        except Exception as e:
            db.session.rollback() 
            return{"success":False,"message":str(e)}

    @jwt_validate(schema=AccessTokenSchema)
    @casbin_validate()
    @response_schema_validate(ResponseSchema)
    def delete(self, id):
        claims = get_jwt()
        teacher_id = claims.get('sub')
    
        if not teacher_id:
            return {"message": "Invalid or missing teacher ID."}, 403
    
        # Retrieve the teacher by ID from JWT claims
        teacher = Teacher.query.get(teacher_id)
        if not teacher:
            return {"message": "Teacher not found."}, 404
    
        # Retrieve the student by ID
        student = StudentPersonalDetails.query.get(id)
        if not student:
            return {"success": False, "data": None, "message": "Student not found."}, 404
    
        # Check if the student belongs to the same department as the teacher
        if student.department_id != teacher.department_id:
            return {"message": "Unauthorized access: Student belongs to another department."}, 403
    
        try:
            # Delete the student
            db.session.delete(student)
            db.session.commit()
            return {
                "success": True,
                "data": student.to_dict(),
                "message": "Student deleted successfully."
            }
        except Exception as e:
            db.session.rollback()  # Rollback in case of failure
            return {"success": False, "message": str(e)}, 500


class CourseSubjectInfo(Resource):
    @jwt_validate(schema=TeacherAccessTokenSchema)
    @casbin_validate()
    @response_schema_validate(ResponseSchema)
    def get(self,id=None):
        if id:
            coursesubject=CourseSubject.query.get(id)
            if not coursesubject:
                return {"success":False,"data":None,"message":"CourseSubject not found"}
            return{"success":True,"data":coursesubject.to_dict(),"message":"coursesubject retrieved successfully"}
        else:
            coursesubjects=CourseSubject.query.all()
            return{"success":True,"data":[coursesubject.to_dict() for coursesubject in coursesubjects],"message":"All CourseSubject retrieved successfully"}
    
    @jwt_validate(schema=TeacherAccessTokenSchema)
    @casbin_validate()
    @schema_validate(CreateCourseSubjectSchema)
    @response_schema_validate(ResponseSchema)
    def post(self):
        claims=get_jwt()
        teacher_id=claims.get('sub')
        if not teacher_id:
            return{"message":"Invalid or missing Teacher id"}
        
        data=request.get_json()
        
        teacher=Teacher.query.filter_by(id=teacher_id).first()
        if not teacher:
            return{"message":"Teacher is not found"},404
        
        department_id=data.get('department_id')
        
        if teacher.department_id != department_id:
            return{"message":"Teacher not found"}
        try:
            new_coursesubject=CourseSubject(**data)
            db.session.add(new_coursesubject)
            db.session.commit()
            return{"success":True,"data":new_coursesubject.to_dict(),"message":"CourseSubject added successfully"}
        except Exception as e:
            db.session.rollback()
            return{"success":False,"message":str(e)},500
        
    @jwt_validate(schema=TeacherAccessTokenSchema)
    @casbin_validate()
    @schema_validate(CreateCourseSubjectSchema)
    @response_schema_validate(ResponseSchema)   
    def put(self,id):
        data=request.get_json()
        coursesubject=CourseSubject.query.get(id)
        if not coursesubject:
            return{"success":False,"data":None,"message":"coursesubject not found"}   
        
        for key,value in data.items():
            setattr(coursesubject,key,value)
        db.session.commit()
        return{"success":True,"data":coursesubject.to_dict(),"message":"coursesubject update successfully"}  
    
    @jwt_validate(schema=TeacherAccessTokenSchema)
    @casbin_validate()
    @response_schema_validate(ResponseSchema)  
    def delete(self,id):
        coursesubject=CourseSubject.query.get(id)
        if not coursesubject:
            return{"success":False,"data":None,"message":"CourseSubject not found"}
        db.session.delete(coursesubject)
        db.session.commit()
        return{"success":True,"data":coursesubject.to_dict(),"message":"CourseSubject deleted successfully"}
        
    
# Resource for Attendance
class AttendanceInfo(Resource):
    @response_schema_validate(ResponseSchema)
    def get(self, id=None):
        if id:
            attendance = Attendance.query.get(id)
            if attendance:
                return{"success":True,"data":attendance.to_dict(),"message":"attendance retrieved successfully"}
            return{"success":False,"data":None,"message":"attendance not found"}
        else:
            attendances = Attendance.query.all()
            return{"success":True,"data":[attendance.to_dict() for attendance in attendances],"message":"All attendance retrieved successfully"}

    @schema_validate(CreateAttendanceSchema)
    @response_schema_validate(ResponseSchema)
    def post(self):
        data = request.get_json()
        attendance = Attendance(**data)
        db.session.add(attendance)
        db.session.commit()
        return{"success":True,"data":attendance.to_dict(),"message":"attendance added successfully"}

    @schema_validate(CreateAttendanceSchema)
    @response_schema_validate(ResponseSchema)
    def put(self, id):
        data = request.get_json()
        attendance = Attendance.query.get(id)
        if not attendance:
            return{"success":False,"data":None,"message":"attendance not found"}
        
        for key,value in data.items():
            setattr(attendance,key,value)
        db.session.commit()
        return{"success":True,"data":attendance.to_dict(),"message":"attendance update successfully"}

    @response_schema_validate(ResponseSchema)
    def delete(self, id):
        attendance = Attendance.query.get(id)
        if not attendance:
            return{"success":False,"data":None,"message":"attendance not found"}
        db.session.delete(attendance)
        db.session.commit()
        return{"success":True,"data":attendance.to_dict(),"message":"attendance delate successfully"}

# Resource for Subject Marks
class SubjectMarkInfo(Resource):
    @response_schema_validate(ResponseSchema)
    def get(self, id=None):
        if id:
            subject_mark = SubjectMark.query.get(id)
            if subject_mark:
                return{"success":True,"data":subject_mark.to_dict(),"message":"subject_mark retrieved successfully"}
            return{"success":False,"data":None,"message":"subject_mark not found"}
        else:
            subject_marks = SubjectMark.query.all()
            return{"success":True,"data":[subject_mark.to_dict() for subject_mark in subject_marks],"message":"All subject_mark retrieved successfully"}

    @response_schema_validate(ResponseSchema)
    def post(self):
        data = request.get_json()
        subjectname1_marks=data['subjectname1_marks']
        subjectname2_marks=data['subjectname2_marks']
        subjectname3_marks=data['subjectname3_marks']
        total_marks=subjectname1_marks+subjectname2_marks+subjectname3_marks
        average_percentage=total_marks/3
        result="pass" if average_percentage >=35 else "fail"
        
        subject_mark = SubjectMark(
            teacher_id=data['teacher_id'],
            teacher_name=data['teacher_name'],
            student_id=data['student_id'],
            student_name=data['student_name'],
            subjectname1_marks=subjectname1_marks,
            subjectname2_marks=subjectname2_marks,
            subjectname3_marks=subjectname3_marks,
            total_marks=total_marks,
            average_percentage=average_percentage,
            result=result
        )
        db.session.add(subject_mark)
        db.session.commit()
        return{"success":True,"data":subject_mark.to_dict(),"message":"subject_mark added successfully"}

    @response_schema_validate(ResponseSchema)
    def put(self, id):
        data = request.get_json()
        subject_mark = SubjectMark.query.get(id)
        if not subject_mark:
            return{"success":False,"data":None,"message":"subject_mark not found"}
        subject_mark.teacher_id = data.get('teacher_id')
        subject_mark.teacher_name = data.get('teacher_name')
        subject_mark.student_id = data.get('student_id')
        subject_mark.student_name = data.get('student_name')
        subject_mark.subjectname1_marks = data.get('subjectname1_marks')
        subject_mark.subjectname2_marks = data.get('subjectname2_marks')
        subject_mark.subjectname3_marks = data.get('subjectname3_marks')
        subject_mark.total_marks = subject_mark.subjectname1_marks +subject_mark.subjectname2_marks +subject_mark.subjectname3_marks 
        subject_mark.average_percentage =subject_mark.total_marks/3
        subject_mark.result ="pass" if subject_mark.average_percentage >=35 else "fail"
        db.session.commit()
        return{"success":True,"data":subject_mark.to_dict(),"message":"subject_mark update successfully"}

    @response_schema_validate(ResponseSchema)
    def delete(self, id):
        subject_mark = SubjectMark.query.get(id)
        if not subject_mark:
            return{"success":False,"data":None,"message":"subject_mark not found"}
        db.session.delete(subject_mark)
        db.session.commit()
        return{"success":True,"data":subject_mark.to_dict(),"message":"subject_mark delete successfully"}


# Resource for Assessment Assignment
class AssessmentAssignInfo(Resource):
    @response_schema_validate(ResponseSchema)
    def get(self, id=None):
        if id:
            assessment = AssessmentAssign.query.get(id)
            if assessment:
                return{"success":True,"data":assessment.to_dict(),"message":"AssessmentAssign retrieved successfully"}
            return{"success":False,"data":None,"message":"subject_mark not found"}
        else:
            assessments = AssessmentAssign.query.all()
            return{"success":True,"data":[assessment.to_dict() for assessment in assessments],"message":"All AssessmentAssign retrieved successfully"}

    @schema_validate(CreateAssessmentAssignSchema)
    @response_schema_validate(ResponseSchema)
    def post(self):
        data = request.get_json()
        assessment = AssessmentAssign(**data)
        db.session.add(assessment)
        db.session.commit()
        return{"success":True,"data":assessment.to_dict(),"message":"AssessmentAssign added successfully"}

    @schema_validate(CreateAssessmentAssignSchema)
    @response_schema_validate(ResponseSchema)
    def put(self, id):
        data = request.get_json()
        assessment = AssessmentAssign.query.get(id)
        if not assessment:
            return{"success":False,"data":None,"message":"AssessmentAssign not found"}
        
        for key,value in data.items():
            setattr(assessment,key,value)
        db.session.commit()
        return{"success":True,"data":assessment.to_dict(),"message":"AssessmentAssign update successfully"}

    @response_schema_validate(ResponseSchema)
    def delete(self, id):
        assessment = AssessmentAssign.query.get(id)
        if not assessment:
            return{"success":False,"data":None,"message":"AssessmentAssign not found"}
        db.session.delete(assessment)
        db.session.commit()
        return{"success":True,"data":assessment.to_dict(),"message":"AssessmentAssign delete successfully"}


# Resource for Assessment Submit
class AssessmentSubmitInfo(Resource):
    @response_schema_validate(ResponseSchema)
    def get(self, id=None):
        if id:
            assessment_submit = AssessmentSubmit.query.get(id)
            if assessment_submit:
                return{"success":True,"data":assessment_submit.to_dict(),"message":"AssessmentSubmit retrieved successfully"}
            return{"success":False,"data":None,"message":"AssessmentAssign not found"}
        else:
            assessment_submits = AssessmentSubmit.query.all()
            return{"success":True,"data":[assessment_submit.to_dict() for assessment_submit in assessment_submits],"message":"All AssessmentSubmit retrieved successfully"}

    @schema_validate(CreateAssessmentSubmitSchema)
    @response_schema_validate(ResponseSchema)
    def post(self):
        data = request.get_json()
        assessment_submit = AssessmentSubmit(**data)
        db.session.add(assessment_submit)
        db.session.commit()
        return{"success":True,"data":assessment_submit.to_dict(),"message":"AssessmentSubmit added successfully"}

    @schema_validate(CreateAssessmentSubmitSchema)
    @response_schema_validate(ResponseSchema)
    def put(self, id):
        data = request.get_json()
        assessment_submit = AssessmentSubmit.query.get(id)
        if not assessment_submit:
            return{"success":False,"data":None,"message":"AssessmentSubmit not found"}
        for key,value in data.items():
            setattr(assessment_submit,key,value)
        db.session.commit()
        return{"success":True,"data":assessment_submit.to_dict(),"message":"AssessmentSubmit delete successfully"}

    @response_schema_validate(ResponseSchema)
    def delete(self, id):
        assessment_submit = AssessmentSubmit.query.get(id)
        if not assessment_submit:
            return{"success":False,"data":None,"message":"AssessmentSubmit not found"}
        db.session.delete(assessment_submit)
        db.session.commit()
        return{"success":True,"data":assessment_submit.to_dict(),"message":"AssessmentSubmit delete successfully"}



