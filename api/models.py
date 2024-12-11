from app import db

class CollegeAdmin(db.Model):
  __tablename__="collegeadmins"
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  college_name=db.Column(db.String(50),nullable=False)
  admin_name=db.Column(db.String(50),nullable=False)
  email=db.Column(db.String(50),nullable=False,unique=True)
  password=db.Column(db.String(50),nullable=False)
  usertype=db.Column(db.String(50),nullable=False)
  
  teachers=db.relationship("Teacher",backref="collegeadmin_ref",lazy=True)
  departments=db.relationship("Department",backref="collegeadmin_ref",lazy=True)
  
  def to_dict(self):
    return{
      "id":self.id,
      "college_name":self.college_name,
      "admin_name":self.admin_name,
      "email":self.email,
      "password":self.password,
      "usertype":self.usertype
    }

class Department(db.Model):
  __tablename__='departments'
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  collegeadmin_id=db.Column(db.Integer,db.ForeignKey("collegeadmins.id"),nullable=False)
  department_name=db.Column(db.String(50),unique=True,nullable=False)
  department_code=db.Column(db.String(50),nullable=False)
  course_available=db.Column(db.String(50),nullable=False)
  num_faculties=db.Column(db.Integer,nullable=False)
  
  # Add foreign key relationship
  teachers=db.relationship("Teacher",backref='department_ref',lazy=True)
  studens=db.relationship("StudentPersonalDetails",backref='department_ref',lazy=True)
  coursesubjects=db.relationship("CourseSubject",backref='department_ref',lazy=True)
  def to_dict(self):
    return{
    "id":self.id,
    "collegeadmin_id":self.collegeadmin_id,
    "department_name":self.department_name,
    "department_code":self.department_code,
    "course_available":self.course_available,
    "num_faculties":self.num_faculties
    } 
    
class Teacher(db.Model):
  __tablename__="teachers"
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  admin_id=db.Column(db.Integer,db.ForeignKey("collegeadmins.id"),nullable=False)
  department_id=db.Column(db.Integer,db.ForeignKey("departments.id"),nullable=False)
  name=db.Column(db.String(50),nullable=False)
  subject_name=db.Column(db.String(50),nullable=False)
  email=db.Column(db.String(50),unique=True,nullable=False)
  password=db.Column(db.String(50),nullable=False)
  usertype=db.Column(db.String(50),nullable=False)
  
  #add foreignKey relationship
  student_personal_details=db.relationship("StudentPersonalDetails",backref="teacher_ref",lazy=True)
  course_subjects=db.relationship("CourseSubject",backref="teachers_ref",lazy=True)
  
  subject_marks=db.relationship("SubjectMark",backref="teachers_ref",lazy=True)
  attendences=db.relationship("Attendance",backref="teacher_ref",lazy=True)
  
  Assessment_assign=db.relationship("AssessmentAssign",backref="teacher_ref",lazy=True)
  Assessment_submit=db.relationship("AssessmentSubmit",backref="teacher_ref",lazy=True)
  
  def to_dict(self):
    return{
      "id":self.id,
      "admin_id":self.admin_id,
      "department_id":self.department_id,
      "name":self.name,
      "subject_name":self.subject_name,
      "email":self.email,
      "password":self.password,
      "usertype":self.usertype
    }
    
class StudentPersonalDetails(db.Model):
    __tablename__ = 'student_personal_details'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    student_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.String(50), nullable=False)
    email=db.Column(db.String(50),nullable=False,unique=True)
    gender = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False, unique=True)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    usertype=db.Column(db.String(50),nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    
    #add foreignKey relationship
    attendances = db.relationship("Attendance", backref="student_personal_details_ref", lazy=True)
    subject_marks = db.relationship("SubjectMark", backref="student_personal_details_ref", lazy=True)
    
    assessment_submits = db.relationship("AssessmentSubmit", backref="student_personal_details_ref", lazy=True)
    assessment_assigns = db.relationship("AssessmentAssign", backref="student_personal_details_ref", lazy=True)
    
    def to_dict(self):
      return{
        "id":self.id,
        "teacher_id":self.teacher_id,
        "student_name":self.student_name,
        "date_of_birth":self.date_of_birth,
        "email":self.email,
        "gender":self.gender,
        "phone_number":self.phone_number,
        "address":self.address,
        "city":self.city,
        "state":self.state,
        "country":self.country,
        "postal_code":self.postal_code,
        "password":self.password,
        "usertype":self.usertype,
        "department_id":self.department_id
      }

class CourseSubject(db.Model):
    __tablename__ = 'course_subject'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    subject_name1 = db.Column(db.String(50), nullable=False)
    subject_name2 = db.Column(db.String(50), nullable=False)
    subject_name3 = db.Column(db.String(50), nullable=False)

    # Relationship 
    attendances = db.relationship("Attendance", backref="course_subject_ref", lazy=True)
    assessment_submits = db.relationship("AssessmentSubmit", backref="course_subject_ref", lazy=True)
    assessment_assigns = db.relationship("AssessmentAssign", backref="course_subject_ref", lazy=True)
 
    def to_dict(self):
      return{
        "id":self.id,
        "teacher_id":self.teacher_id,
        "department_id":self.department_id,
        "subject_name1":self.subject_name1,
        "subject_name2":self.subject_name2,
        "subject_name3":self.subject_name3
      }

class SubjectMark(db.Model):
  __tablename__="subject_marks"
  id=db.Column(db.Integer, primary_key=True,autoincrement=True)
  teacher_id=db.Column(db.Integer,db.ForeignKey("teachers.id"),nullable=False)
  student_id=db.Column(db.Integer,db.ForeignKey("student_personal_details.id"),nullable=False)
  subjectname1_marks=db.Column(db.Integer,nullable=False)
  subjectname2_marks=db.Column(db.Integer,nullable=False)
  subjectname3_marks=db.Column(db.Integer,nullable=False)
  total_marks=db.Column(db.Integer,nullable=False)
  average_percentage=db.Column(db.Float,nullable=False)
  result=db.Column(db.String(50),nullable=False)
  
  def to_dict(self):
    return {
      "id":self.id,
      "teacher_id":self.teacher_id,
      "student_id":self.student_id,
      "subjectname1_maks":self.subjectname1_marks,
      "subjectname2_maks":self.subjectname2_marks,
      "subjectname3_maks":self.subjectname3_marks,
      "total_marks":self.total_marks,
      "average_percentage":self.average_percentage,
      "result":self.result
    }

class Attendance(db.Model):
  __tablename__="attendances"
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  teacher_id=db.Column(db.Integer,db.ForeignKey("teachers.id"),nullable=False)
  student_id=db.Column(db.Integer,db.ForeignKey("student_personal_details.id"),nullable=False)
  subject_id=db.Column(db.Integer,db.ForeignKey("course_subject.id"),nullable=False)
  date=db.Column(db.String(50),nullable=False)
  time=db.Column(db.String(50),nullable=False)
  status=db.Column(db.String(50),nullable=False)
  
  def to_dict(self):
    return{
      "id":self.id,
      "teacher_id":self.teacher_id,
      "student_id":self.student_id,
      "subject_id":self.subject_id,
      "date":self.date,
      "time":self.time,
      "status":self.status
    }

class AssessmentAssign(db.Model):
  __tablename__="assessment_assigns"
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  teacher_id=db.Column(db.Integer,db.ForeignKey("teachers.id"),nullable=False)
  student_id=db.Column(db.Integer,db.ForeignKey("student_personal_details.id"),nullable=False)
  subject_id=db.Column(db.Integer,db.ForeignKey("course_subject.id"),nullable=False)
  issue_date=db.Column(db.String(50),nullable=False)
  due_date=db.Column(db.String(50),nullable=False)
  
  def to_dict(self):
    return{
      "id":self.id,
      "teacher_id":self.teacher_id,
      "student_id":self.student_id,
      "subject_id":self.subject_id,
      "issue_date":self.issue_date,
      "due_date":self.due_date
    }
  
class AssessmentSubmit(db.Model):
  __tablename__='assessment_submits'
  id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  teacher_id=db.Column(db.Integer,db.ForeignKey("teachers.id"),nullable=False)
  student_id=db.Column(db.Integer,db.ForeignKey("student_personal_details.id"),nullable=False)
  subject_id=db.Column(db.Integer,db.ForeignKey("course_subject.id"),nullable=False)
  due_date=db.Column(db.Date,nullable=False)
  
  def to_dict(self):
    return{
      "id":self.id,
      "teacher_id":self.teacher_id,
      "student_id":self.student_id,
      "subject_id":self.subject_id,
      "due_date":self.due_date
    }