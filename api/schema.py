CreateCollegeAdminSchema={
    "type":"object",
    "properties":{
        "college_name":{"type":"string"},
        "admin_name":{"type":"string"},
        "email":{"type":"string"},
        "password":{"type":"string"},
        "usertype":{"type":"string"}
    },
    "additionalproperties":False,
    "required":[
        "college_name",
        "admin_name",
        "email",
        "password",
        "usertype"
        ],
}
CreateDepartmentSchema={
  "type":"object",
  "properties":{
    "collegeadmin_id":{"type":"integer"},  
    "department_name":{"type":"string"},
    "department_code":{"type":"string"},
    "course_available":{"type":"string"},
    "num_faculties":{"type":"integer"},
  },
  "additionalproperties":False,
  "required":[
    "collegeadmin_id",
    "department_name",
    "department_code",
    "course_available",
    "num_faculties"
    ],
}

CreateTeacherSchema={
  "type":"object",
  "properties":{
    "admin_id":{"type":"integer"},
    "department_id":{"type":"integer"},
    "name":{"type":"string"},
    "subject_name":{"type":"string"},
    "email":{"type":"string"},
    "password":{"type":"string"},
    "usertype":{"type":"string"}
  },
  "additionalproperties":False,
  "required":[
    "admin_id",
    "department_id",
    "name",
    "subject_name",
    "email",
    "password",
    "usertype",
  ],
}

CreateStudentSchema = {
    "type": "object",
    "properties": {
        "teacher_id": {"type": "integer"},
        "student_name": {"type": "string"},
        "date_of_birth": {"type": "string"},
        "email": {"type": "string"},
        "gender": {"type": "string"},
        "phone_number": {"type": "string"}, 
        "address": {"type": "string"},
        "city": {"type": "string"},
        "state": {"type": "string"},
        "country": {"type": "string"},
        "postal_code": {"type": "string"},
        "password": {"type": "string"},
        "usertype":{"type":"string"},
        "department_id":{"type":"integer"}
    },
    "additionalProperties": False,
    "required": [
        "teacher_id",
        "student_name",
        "date_of_birth",
        "email",
        "gender",
        "phone_number",
        "address",
        "city",
        "state",
        "country",
        "postal_code",
        "password",
        "usertype",
        "department_id"
    ],
}


CreateCourseSubjectSchema={
  "type":"object",
  "properties":{
    "teacher_id":{"type":"integer"},
    "department_id":{"type":"integer"},
    "subject_name1":{"type":"string"},
    "subject_name2":{"type":"string"},
    "subject_name3":{"type":"string"},
  },
  "additionalProperties":False,
  "required":[
    "teacher_id",
    "department_id",
    "subject_name1",
    "subject_name2",
    "subject_name3",
  ],
}

CreateAttendanceSchema = {
    "type": "object",
    "properties": {
        "teacher_id": {"type": "integer"},
        "student_id": {"type": "integer"},
        "subject_id": {"type": "integer"},
        "date": {"type": "string"}, 
        "time": {"type": "string"},  
        "status": {"type": "string"},
    },
    "additionalProperties": False,
    "required": [
        "teacher_id",
        "student_id",
        "subject_id",
        "date",
        "time",
        "status"
    ],
}

# CreateSubjectMarkSchema = {
#     "type": "object",
#     "properties": {
#         "teacher_id": {"type": "integer"},
#         "teacher_name": {"type": "string"},
#         "student_id": {"type": "integer"},
#         "student_name": {"type": "string"},
#         "subjectname1_marks": {"type": "integer"},
#         "subjectname2_marks": {"type": "integer"},
#         "subjectname3_marks": {"type": "integer"},
#         "total_marks": {"type": "integer"},
#         "average_percentage": {"type": "number"},
#         "result": {"type": "string"}
#     },
#     "additionalProperties": False,
#     "required": [
#         "teacher_id",
#         "teacher_name",
#         "student_id",
#         "student_name",
#         "subjectname1_marks",
#         "subjectname2_marks",
#         "subjectname3_marks",
#         "total_marks",
#         "average_percentage",
#         "result"
#     ],
# }

CreateAssessmentAssignSchema = {
    "type": "object",
    "properties": {
        "teacher_id": {"type": "integer"},
        "student_id": {"type": "integer"},
        "subject_id": {"type": "integer"},
        "issue_date": {"type": "string"},
        "due_date": {"type": "string"},
    },
    "additionalProperties": False,
    "required": [
        "teacher_id",
        "student_id",
        "subject_id",
        "issue_date",
        "due_date",
    ],
}

CreateAssessmentSubmitSchema = {
    "type": "object",
    "properties": {
        "teacher_id": {"type": "integer"},
        "student_id": {"type": "integer"},
        "subject_id": {"type": "integer"},
        "due_date": {"type": "string"},
    },
    "additionalProperties": False,
    "required": [
        "teacher_id",
        "student_id",
        "subject_id",
        "due_date"
    ],
}


ResponseSchema = {
    "type": "object",
    "properties": {
        "success": {"type": "boolean"},
        "data": {
            "anyOf": [
                {"type": "object"},  # For single records.
                {"type": "array", "items": {"type": "object"}},  # For multiple records.
            ]
        },
        "message": {"type": "string"},
    },
    "additionalProperties": False,
    "required": ["success", "data", "message"],
}



CollegeAdminAccessTokenSchema = {
    "type": "object",
    "properties": {
        "fresh": {"type": "boolean"},
        "iat": {"type": "integer"},
        "jti": {"type": "string"},
        "type": {"type": "string"},
        "sub": {"type": "string"},  # Changed to integer
        "nbf": {"type": "integer"},
        "csrf": {"type": "string"},
        "exp": {"type": "integer"},
        "usertype": {"type": "string"},  # Added as a top-level field
        "name": {"type": "string"}      # Added as a top-level field
    },
    "required": ["fresh", "iat", "jti", "type", "sub", "nbf", "csrf", "exp", "usertype", "name"]  # Updated required fields
}

AccessTokenSchema = {
    "type": "object",
    "properties": {
        "fresh": {"type": "boolean"},
        "iat": {"type": "integer"},
        "jti": {"type": "string"},
        "type": {"type": "string"},
        "sub": {"type": "string"},  # Changed to integer
        "nbf": {"type": "integer"},
        "csrf": {"type": "string"},
        "exp": {"type": "integer"},
        "usertype": {"type": "string", "enum": ["Teacher", "HOD"]},  # Added as a top-level field
        "name": {"type": "string"}      # Added as a top-level field
    },
    "required": ["fresh", "iat", "jti", "type", "sub", "nbf", "csrf", "exp", "usertype", "name"]  # Updated required fields
}

TeacherAccessTokenSchema = {
    "type": "object",
    "properties": {
        "fresh": {"type": "boolean"},
        "iat": {"type": "integer"},
        "jti": {"type": "string"},
        "type": {"type": "string"},
        "sub": {"type": "string"},  # Changed to integer
        "nbf": {"type": "integer"},
        "csrf": {"type": "string"},
        "exp": {"type": "integer"},
        "usertype": {"type": "string"},  # Added as a top-level field
        "name": {"type": "string"}      # Added as a top-level field
    },
    "required": ["fresh", "iat", "jti", "type", "sub", "nbf", "csrf", "exp", "usertype", "name"]  # Updated required fields
}

StudentAccessTokenSchema = {
    "type": "object",
    "properties": {
        "fresh": {"type": "boolean"},
        "iat": {"type": "integer"},
        "jti": {"type": "string"},
        "type": {"type": "string"},
        "sub": {"type": "string"},  # Changed to integer
        "nbf": {"type": "integer"},
        "csrf": {"type": "string"},
        "exp": {"type": "integer"},
        "usertype": {"type": "string"},  # Added as a top-level field
        "name": {"type": "string"}      # Added as a top-level field
    },
    "required": ["fresh", "iat", "jti", "type", "sub", "nbf", "csrf", "exp", "usertype", "name"]  # Updated required fields
}