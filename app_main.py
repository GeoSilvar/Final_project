from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from .database import engine, get_db, Base
from .models import User, Student, Teacher, Parent, Assessment, Attendance
from .routers import auth, students, teachers, parents, assessments, fees, analytics
from .config import settings

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Asili SSMS API",
    description="Smart School Management System for Kenyan Education",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(students.router, prefix="/api/v1/students", tags=["students"])
app.include_router(teachers.router, prefix="/api/v1/teachers", tags=["teachers"])
app.include_router(parents.router, prefix="/api/v1/parents", tags=["parents"])
app.include_router(assessments.router, prefix="/api/v1/assessments", tags=["assessments"])
app.include_router(fees.router, prefix="/api/v1/fees", tags=["fees"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

@app.get("/")
async def root():
    return {
        "message": "Asili SSMS API - Quality Education for Kenya",
        "version": "1.0.0",
        "sdg_alignment": "UN SDG 4 - Quality Education"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}