from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager



db=SQLAlchemy()
migrate=Migrate()

def create_app():
  app=Flask(__name__)
  api=Api(app)
  jwt=JWTManager(app)
  
  app.config.from_object("config.Config")
  db.init_app(app)
  
  migrate.init_app(app,db)

  from models import CollegeAdmin,Department,Teacher,StudentPersonalDetails,CourseSubject,Attendance,SubjectMark,AssessmentAssign,AssessmentSubmit
  from resources import CollegeAdminInfo,DepartmentInfo, TeacherInfo, StudentInfo,CourseSubjectInfo, AttendanceInfo, SubjectMarkInfo, AssessmentAssignInfo, AssessmentSubmitInfo
  
  from access_token import AdminLogin,TeacherLogin,StudentLogin
  
  with app.app_context():
    db.create_all()
    # create individual tables
  #  College.__table__.create(db.engine)  
  #  Teacher.__table__.create(db.engine)

  
  api.add_resource(CollegeAdminInfo, "/collegeadmin", "/collegeadmin/<int:id>")
  api.add_resource(AdminLogin,"/admin/login")
  
  api.add_resource(DepartmentInfo,"/department","/department/<int:id>")
  
  api.add_resource(TeacherInfo, "/teacher", "/teacher/<int:id>")
  api.add_resource(TeacherLogin,"/teacher/login")
  
  api.add_resource(StudentInfo, "/student", "/student/<int:id>")
  api.add_resource(StudentLogin,"/student/login")
  
  api.add_resource(CourseSubjectInfo,"/coursesubject","/coursesubject/<int:id>")
  api.add_resource(AttendanceInfo, "/attendance", "/attendance/<int:id>")
  api.add_resource(SubjectMarkInfo, "/subjectmark", "/subjectmark/<int:id>")
  api.add_resource(AssessmentAssignInfo, "/assessmentassign", "/assessmentassign/<int:id>")
  api.add_resource(AssessmentSubmitInfo, "/assessmentsubmit", "/assessmentsubmit/<int:id>")

  return app