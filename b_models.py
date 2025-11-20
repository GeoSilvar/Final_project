from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from .database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"

class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class SpecialNeedsCategory(str, enum.Enum):
    NONE = "none"
    PHYSICAL = "physical"
    LEARNING = "learning"
    VISUAL = "visual"
    HEARING = "hearing"
    AUTISM = "autism"

class CompetencyLevel(str, enum.Enum):
    EMERGING = "emerging"
    DEVELOPING = "developing"
    PROFICIENT = "proficient"
    ADVANCED = "advanced"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(20), unique=True, index=True)
    national_id = Column(String(20), unique=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    student_profile = relationship("Student", back_populates="user", uselist=False)
    teacher_profile = relationship("Teacher", back_populates="user", uselist=False)
    parent_profile = relationship("Parent", back_populates="user", uselist=False)

class Student(Base):
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    admission_number = Column(String(50), unique=True, index=True)
    date_of_birth = Column(DateTime)
    gender = Column(Enum(Gender))
    grade_level = Column(String(50))
    stream = Column(String(50))
    special_needs = Column(Enum(SpecialNeedsCategory), default=SpecialNeedsCategory.NONE)
    special_needs_details = Column(Text)
    emergency_contact = Column(String(20))
    enrollment_date = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="student_profile")
    attendance = relationship("Attendance", back_populates="student")
    assessments = relationship("Assessment", back_populates="student")
    parent_associations = relationship("StudentParent", back_populates="student")

class Teacher(Base):
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    tsc_number = Column(String(50), unique=True, index=True)
    qualification = Column(String(255))
    specialization = Column(String(255))
    date_of_birth = Column(DateTime)
    gender = Column(Enum(Gender))
    employment_date = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="teacher_profile")
    cpd_records = relationship("CPDRecord", back_populates="teacher")
    assessments = relationship("Assessment", back_populates="teacher")

class Parent(Base):
    __tablename__ = "parents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    occupation = Column(String(255))
    
    user = relationship("User", back_populates="parent_profile")
    student_associations = relationship("StudentParent", back_populates="parent")

class StudentParent(Base):
    __tablename__ = "student_parents"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    parent_id = Column(Integer, ForeignKey("parents.id"))
    relationship_type = Column(String(50))  # mother, father, guardian
    
    student = relationship("Student", back_populates="parent_associations")
    parent = relationship("Parent", back_populates="student_associations")

class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(DateTime, default=func.now())
    status = Column(String(20))  # present, absent, late
    remarks = Column(Text)
    
    student = relationship("Student", back_populates="attendance")

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    subject = Column(String(100))
    competency_domain = Column(String(100))
    competency_level = Column(Enum(CompetencyLevel))
    score = Column(Float)
    max_score = Column(Float)
    assessment_date = Column(DateTime, default=func.now())
    comments = Column(Text)
    cbc_strands = Column(JSON)  # Store CBC strands as JSON
    
    student = relationship("Student", back_populates="assessments")
    teacher = relationship("Teacher", back_populates="assessments")

class CPDRecord(Base):
    __tablename__ = "cpd_records"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    activity = Column(String(255))
    hours = Column(Float)
    date_completed = Column(DateTime)
    provider = Column(String(255))
    certificate_url = Column(String(500))
    
    teacher = relationship("Teacher", back_populates="cpd_records")

class FeeTransaction(Base):
    __tablename__ = "fee_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(50))  # invoice, payment
    mpesa_receipt = Column(String(50))
    transaction_date = Column(DateTime, default=func.now())
    status = Column(String(50))  # pending, completed, failed
    description = Column(Text)
    
    student = relationship("Student")